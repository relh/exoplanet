"""Bounded public-data pilot. All rankings are exploratory, never discoveries."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests
from astropy.io import fits
from .search import flatten, scan, diagnostics, triage
from .integrity import verify_hdus

TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERIES = {
    "toi": "select tid,toi,toipfx,pl_orbper,tfopwg_disp from toi",
    "confirmed": "select distinct tic_id,pl_name,pl_orbper from ps where tic_id is not null",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def fetch(url, path, params=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = path.with_suffix(path.suffix + ".json")
    if path.exists() and meta.exists():
        info = json.loads(meta.read_text())
        if sha(path) != info["sha256"]:
            raise ValueError(f"Cache checksum mismatch: {path}")
        return info
    r = requests.get(url, params=params, timeout=(20, 120))
    r.raise_for_status()
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_bytes(r.content)
    tmp.replace(path)
    info = {"url": r.url, "retrieved_utc": now(), "sha256": sha(path), "bytes": path.stat().st_size}
    save_json(meta, info)
    return info


def catalogs(root, output):
    known, evidence = {}, {}
    for name, query in QUERIES.items():
        path = root / "catalogs" / f"{name}.csv"
        evidence[name] = fetch(TAP, path, {"query": query, "format": "csv"})
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        key = "tid" if name == "toi" else "tic_id"
        if not rows or key not in rows[0]:
            raise ValueError(f"Invalid or empty catalog: {name}")
        for row in rows:
            tic = int(row[key].replace("TIC", "").strip())
            known.setdefault(tic, []).append({"catalog": name, **row})
        shutil.copyfile(path, output / f"catalog_{name}.csv")
    return known, evidence


def read_curve(path):
    with fits.open(path, checksum=False) as hdus:
        integrity = verify_hdus(path, hdus)
        h, d = hdus[0].header, hdus[1].data
        metadata = {k.lower(): h.get(k) for k in
                    ("TICID", "SECTOR", "TESSMAG", "RADIUS", "TEFF", "RA_OBJ", "DEC_OBJ")}
        metadata["fits_integrity"] = integrity
        metadata["crowdsap"] = hdus[1].header.get("CROWDSAP")
        columns = {k: np.array(d[k], dtype=float) for k in ("TIME", "PDCSAP_FLUX", "PDCSAP_FLUX_ERR")}
        t, f, e = (columns[k] for k in columns)
        keep = (d["QUALITY"] == 0) & np.isfinite(t) & np.isfinite(f) & np.isfinite(e) & (f > 0) & (e > 0)
        t, f, e = t[keep], f[keep], e[keep]
        if len(t)==0:
            raise ValueError('No finite positive quality-zero SPOC flux/error pairs')
        order = np.argsort(t)
        t, f, e = t[order], f[order], e[order]
        unique = np.r_[True, np.diff(t) > 0]
        return t[unique], f[unique], e[unique], metadata


def plot_curve(path, destination, row):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    t, f, e, _ = read_curve(path)
    t, y, dy = flatten(t, f, e)
    best = row["best"]
    phase = (t - best["transit_time"] + best["period"] / 2) % best["period"] - best["period"] / 2
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), constrained_layout=True)
    axes[0].plot(t, (y - 1) * 1e6, ".", ms=2)
    axes[0].set(xlabel="Time (BTJD = BJD TDB - 2457000)", ylabel="Relative flux (ppm)")
    axes[1].plot(phase * 24, (y - 1) * 1e6, ".", ms=2, alpha=.4)
    edges = np.linspace(-3 * best["duration"], 3 * best["duration"], 41)
    centers, means = [], []
    for left, right in zip(edges[:-1], edges[1:]):
        mask = (phase >= left) & (phase < right)
        if mask.any():
            centers.append((left + right) / 2 * 24)
            means.append(np.average(y[mask] - 1, weights=1 / dy[mask]**2) * 1e6)
    axes[1].plot(centers, means, "o-", color="black", ms=3)
    axes[1].set(xlabel="Hours from fitted transit", ylabel="Relative flux (ppm)",
                xlim=(-3 * best["duration"] * 24, 3 * best["duration"] * 24))
    fig.suptitle(f'TIC {row["tic"]}: exploratory peak, P={best["period"]:.5f} d\n' + ", ".join(row["flags"]))
    fig.savefig(destination, dpi=130)
    plt.close(fig)


def process(item, root, sector):
    tic, url = item
    path = root / "lightcurves" / f"s{sector:04d}-{tic}.fits"
    row = {"tic": tic, "sector": sector, "status": "error", "source_url": url}
    try:
        row["source"] = fetch(url, path)
        t, f, e, meta = read_curve(path)
        row["star"] = meta
        if int(meta["ticid"]) != tic or int(meta["sector"]) != sector:
            raise ValueError("FITS identity mismatch")
        t1, y, dy = flatten(t, f, e)
        _, _, best = scan(t1, y, dy)
        diag = diagnostics(t1, y, dy, best)
        flags = triage(best, diag)
        if any(h["checksum"] != "verified" for h in meta["fits_integrity"]):
            flags.append("missing_fits_checksum")
        # Independent detrending window, still the same image-processing product.
        t2, y2, dy2 = flatten(t, f, e, window=2.5)
        alternative = scan(t2, y2, dy2)[2]
        if abs(alternative["period"] / best["period"] - 1) > .02:
            flags.append("detrending_period_unstable")
        if meta["crowdsap"] is None or meta["crowdsap"] < .8:
            flags.append("crowding_or_missing_crowding")
        radius = meta["radius"]
        implied_radius = float(np.sqrt(best["depth"]) * radius * 109.076) if radius and radius > 0 else None
        row.update(status="screened", n_points=len(t1), best=best, diagnostics=diag,
            alternative_window_best=alternative, flags=flags,
            radius_earth_if_on_target=implied_radius,
            disposition="needs_followup" if not flags else "flagged",
            novelty="No TIC match in saved TOI/confirmed snapshots; other catalogs and literature unchecked")
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
    print(f'TIC {tic}: {row.get("disposition", row["status"])} {row.get("flags", row.get("error", ""))}', flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sector", type=int, default=14)
    parser.add_argument("--limit", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20261009)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.limit <= 1000 or not 1 <= args.workers <= 8 or args.sector < 1:
        parser.error("Require limit 1..1000, workers 1..8, sector >=1")
    args.output.mkdir(parents=True, exist_ok=False)
    known, catalog_evidence = catalogs(args.data, args.output)
    manifest = args.data / "manifests" / f"sector{args.sector}.sh"
    url = f"https://archive.stsci.edu/hlsps/tess-spoc/download_scripts/hlsp_tess-spoc_tess_phot_s{args.sector:04d}_tess_v1_dl-lc.sh"
    source = fetch(url, manifest)
    # Parse URLs only. Never run a downloaded shell script.
    targets = {}
    for url in re.findall(r"'(https://[^']+_lc\.fits)'", manifest.read_text()):
        m = re.search(r"phot_(\d+)-s(\d+)", url)
        if m and int(m[2]) == args.sector:
            targets[int(m[1])] = url
    if not targets:
        raise ValueError("No light-curve URLs in manifest")
    eligible = sorted(set(targets) - set(known))
    rng = np.random.default_rng(args.seed)
    selected = [int(t) for t in rng.choice(eligible, size=min(args.limit, len(eligible)), replace=False)]
    run = {"started_utc": now(), "configuration": {k: str(v) if isinstance(v, Path) else v for k,v in vars(args).items()},
        "software": {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "astropy", "requests", "matplotlib")},
        "source_sha256": {p.name: sha(p) for p in Path(__file__).parent.glob("*.py")},
        "manifest": source, "catalogs": catalog_evidence, "total_manifest_targets": len(targets),
        "excluded_known_targets": len(targets) - len(eligible), "selected_tics": selected,
        "selection": "Uniform without replacement from sorted manifest TIC IDs after TOI/confirmed TIC exclusion; no proximity or stellar-size selection",
        "search": {"min_period_days": .7, "max_period_days": "min(10, cleaned_baseline/2.5)",
            "durations_days": [.06, .09, .13, .18, .24], "windows_days": [1.5, 2.5],
            "quality": "QUALITY == 0", "null_control": "One sign-inverted search; not a calibrated false-alarm probability"}}
    save_json(args.output / "run.json", run)
    results = []
    with ThreadPoolExecutor(args.workers) as pool:
        for row in pool.map(lambda tic: process((tic, targets[tic]), args.data, args.sector), selected):
            results.append(row)
            save_json(args.output / "results.json", results)
    good = sorted([r for r in results if r["status"] == "screened"], key=lambda r: r["best"]["depth_snr"], reverse=True)
    plot_rows = {r["tic"]: r for r in good[:5] + [r for r in good if r["disposition"] == "needs_followup"]}
    for row in plot_rows.values():
        plot_curve(args.data / "lightcurves" / f's{args.sector:04d}-{row["tic"]}.fits', args.output / f'tic-{row["tic"]}.png', row)
    run["finished_utc"] = now()
    run["screened"] = len(good)
    run["errors"] = len(results) - len(good)
    run["needs_followup"] = sum(r["disposition"] == "needs_followup" for r in good)
    save_json(args.output / "run.json", run)
    with (args.output / "ranking.csv").open("w") as stream:
        writer = csv.writer(stream)
        writer.writerow(["tic", "period_days", "depth_ppm", "formal_snr", "supported_events", "flags"])
        for r in good:
            writer.writerow([r["tic"], r["best"]["period"], r["best"]["depth"] * 1e6,
                r["best"]["depth_snr"], r["diagnostics"]["supported_events"], ";".join(r["flags"])])
    print(json.dumps({k:run[k] for k in ("screened", "errors", "needs_followup")}), flush=True)

if __name__ == "__main__":
    main()
