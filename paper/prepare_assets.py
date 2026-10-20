"""Copy archived figures and index evidence. No downloads or scientific analysis."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASELINE = "0537d585d"
FIGURES = {
    "803-holdout.png": "results/followup-80387959-qlp90-100-20261009/heldout-folds.png",
    "803-shape.png": "results/strongest-80387959-shape-20261012/diagnostic.png",
    "402-events.png": "results/strongest-402358350-baselines-20261012/event-shapes.png",
    "402-widths.png": "results/strongest-402358350-baselines-20261012/width-matrix.png",
    "402-holdout.png": "results/heldout-402358350-s81-20261011/comparison.png",
    "host-eclipses.png": "results/paper-host-vetting-20261012/required-eclipses.png",
    "host-instability.png": "results/prf-80387959-event-stability-20261011/stability.png",
    "host-control.png": "results/prf-137151335-20261011/prf-comparison.png",
    "803-noise.png": "results/paper-vetting-80387959-20261012/noise-diagnostic.png",
    "402-noise.png": "results/paper-vetting-402358350-20261012/noise-sensitivity.png",
    "pulsator-tests.png": "results/extension-402358350-5546257-20261012/pulsator-tests.png",
    "triceratops-convergence.png": "dashboard/dist/triceratops-convergence.png",
    "803-resolved.png": "results/resolved-followup-803-20261013/skymapper-fixed-clock.png",
    "402-resolved.png": "results/resolved-followup-402-20261013/ztf-diagnostic.png",
    "241-physical.png": "results/physical-241928959-20261012/fits.png",
    "469-seasons.png": "results/season-out-469309982-20261011/folds.png",
    "469-961-new.png": "results/new-epochs-469309982-96166003-20261012/fixed-clocks.png",
    "961-clocks.png": "results/same-clock-96166003-20261012/comparison.png",
    "554-gaia.png": "results/extension-402358350-5546257-20261012/gaia-candidate-clocks.png",
    "554-new.png": "results/new-epochs-5546257-20261012/fixed-clocks.png",
    "controls-known.png": "results/solar-radius-positive-controls-20261011/control-folds.png",
    "controls-pointing.png": "results/pointing-correction-controls-20261012/controls.png",
    "controls-aperture.png": "results/strongest-host-identifiability-20261012/controls.png",
    "803-paired.png": "results/strongest-80387959-shape-20261012/paired-products/comparison.png",
}
REPORTS = [
    ("Scope and evidence index", "CHECKED-RESULTS.md"),
    ("Search completion", "results/scoped-completion-20261012/ASSESSMENT.md"),
    ("Solar selection", "results/solar-radius-pilot-selection-20261011/ASSESSMENT.md"),
    ("Solar ledger", "results/solar-radius-lead-audit-20261011/ASSESSMENT.md"),
    ("Weak-seed review", "results/weak-seed-audit-20261011/ASSESSMENT.md"),
    ("Faint QLP expansion", "results/qlp-faint-expanded-20261010/ASSESSMENT.md"),
    ("Reserved-data exception", "results/solar-radius-ranks3920-4432-20261011/ASSESSMENT.md"),
    ("Known-host controls", "results/solar-radius-positive-controls-20261011/ASSESSMENT.md"),
    ("Shallow injections", "results/solar-radius-shallow-injections-20261011/ASSESSMENT.md"),
    ("803 frozen prediction", "results/followup-80387959-qlp90-100-20261009/heldout.json"),
    ("803 native profiles", "results/strongest-80387959-shape-20261012/ASSESSMENT.md"),
    ("402 frozen sector 81", "results/heldout-402358350-s81-20261011/ASSESSMENT.md"),
    ("402 local baselines", "results/strongest-402358350-baselines-20261012/ASSESSMENT.md"),
    ("803 noise audit", "results/paper-vetting-80387959-20261012/ASSESSMENT.md"),
    ("402 noise audit", "results/paper-vetting-402358350-20261012/ASSESSMENT.md"),
    ("Neighbor light budgets", "results/paper-host-vetting-20261012/ASSESSMENT.md"),
    ("Image control failure", "results/prf-137151335-20261011/ASSESSMENT.md"),
    ("Source instability", "results/prf-80387959-event-stability-20261011/ASSESSMENT.md"),
    ("Pointing controls", "results/pointing-correction-controls-20261012/ASSESSMENT.md"),
    ("Aperture controls", "results/strongest-host-identifiability-20261012/ASSESSMENT.md"),
    ("TRICERATOPS results", "results/triceratops-20261013/ASSESSMENT.md"),
    ("TRICERATOPS review", "results/triceratops-review-20261013/ASSESSMENT.md"),
    ("Resolved SkyMapper", "results/resolved-followup-803-20261013/ASSESSMENT.md"),
    ("Resolved ZTF", "results/resolved-followup-402-20261013/ASSESSMENT.md"),
    ("241 physical fits", "results/physical-241928959-20261012/ASSESSMENT.md"),
    ("469 season tests", "results/season-out-469309982-20261011/ASSESSMENT.md"),
    ("469/961 new epochs", "results/new-epochs-469309982-96166003-20261012/ASSESSMENT.md"),
    ("961 clock comparison", "results/same-clock-96166003-20261012/ASSESSMENT.md"),
    ("554 new epochs", "results/new-epochs-5546257-20261012/ASSESSMENT.md"),
    ("Pulsator and Gaia tests", "results/extension-402358350-5546257-20261012/ASSESSMENT.md"),
    ("554 catalog alias", "results/contaminant-clock-5546257-20261012/ASSESSMENT.md"),
    ("Six local baselines", "results/event-baseline-six-20261012/ASSESSMENT.md"),
    ("Companion metadata", "results/companion-constraints-shortlist-20261012/ASSESSMENT.md"),
    ("803 spectroscopy", "results/web-80387959-20261012/ASSESSMENT.md"),
    ("Follow-up planning", "results/followup-planning-20261013/ASSESSMENT.md"),
    ("Observing access", "results/observing-access-20261013/ASSESSMENT.md"),
]
EXTRA = [
    "results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json",
    "results/followup-469309982-20261011/frozen.json",
    "results/expanded-96166003-20261012/frozen-for59.json",
    "results/source-check-5546257-20261011/frozen.json",
    "results/solar-radius-lead-audit-20261011/audit.json",
    "results/weak-seed-audit-20261011/audit.json",
    "results/companion-constraints-shortlist-20261012/summary.json",
    "results/followup-planning-20261013/targets.json",
    "results/followup-planning-20261013/neighbors.csv",
    "docs/privacy-edits.json", "docs/release-history-redactions.json",
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    m = json.loads((HERE / "evidence-manifest.json").read_text())
    for row in m["figures"]:
        assert digest(HERE / row["paper_path"]) == row["sha256"], row["paper_path"]
    checked = 0
    if (ROOT / "results").is_dir():
        for row in m["source_records"]:
            assert digest(ROOT / row["path"]) == row["sha256"], row["path"]
            checked += 1
    print(f"Verified {len(m['figures'])} figure copies and {checked} repository source records.")

def prepare():
    assert (ROOT / "results").is_dir(), "Run asset preparation inside the research repository"
    baseline = subprocess.check_output(["git", "rev-parse", BASELINE], cwd=ROOT, text=True).strip()
    (HERE / "figures").mkdir(exist_ok=True)
    figures = []
    for name, source in FIGURES.items():
        target = HERE / "figures" / name
        shutil.copyfile(ROOT / source, target)
        figures.append({"paper_path": f"figures/{name}", "source_path": source, "sha256": digest(target)})
    paths = set(EXTRA) | set(FIGURES.values()) | {p for _, p in REPORTS}
    for _, report in REPORTS:
        folder = (ROOT / report).parent
        if report.startswith("results/"):
            for pattern in ["*.json", "*.py"]:
                paths.update(p.relative_to(ROOT).as_posix() for p in folder.glob(pattern))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / "src/exoplanet").glob("*.py"))
    records = [{"path": p, "sha256": digest(ROOT / p)} for p in sorted(paths)]
    manifest = {
        "manuscript_date": "2026-10-20", "scientific_cutoff": "2026-10-13",
        "author": "Richard Higgins", "contact": "richard@relh.net",
        "repository": "https://github.com/relh/exoplanet", "evidence_commit": baseline,
        "new_observing_epochs_opened": False, "new_candidate_analysis_performed": False,
        "scope": "Byte-identical archived figure copies and selected evidence/source hashes; no claim of independent scientific validation.",
        "figures": figures, "source_records": records,
    }
    (HERE / "evidence-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = [r"\footnotesize", r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.055\textwidth}>{\raggedright\arraybackslash}p{0.23\textwidth}>{\raggedright\arraybackslash}p{0.66\textwidth}@{}}", r"\toprule ID & Evidence & Repository path \\", r"\midrule\endhead"]
    for i, (label, path) in enumerate(REPORTS, 1):
        url = f"https://github.com/relh/exoplanet/blob/{baseline}/{path}"
        lines.append(f"E{i:02} & {label} & \\href{{{url}}}{{\\nolinkurl{{{path}}}}} \\\\")
    lines += [r"\bottomrule", r"\end{longtable}", r"\normalsize"]
    (HERE / "evidence-index.tex").write_text("\n".join(lines) + "\n")
    verify()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the saved copies without rewriting them")
    if parser.parse_args().check:
        verify()
    else:
        prepare()
