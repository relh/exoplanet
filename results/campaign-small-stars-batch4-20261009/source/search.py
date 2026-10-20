"""Single-sector BLS screening with deliberately conservative diagnostics."""
import numpy as np
from scipy.ndimage import median_filter
from astropy.timeseries import BoxLeastSquares, LombScargle


def flatten(time, flux, error, window=1.5):
    """Median detrend contiguous pieces; trim edges, retain downward outliers.

    Flux/errors must already be finite, positive, time sorted and quality filtered.
    No interpolation across gaps >0.3 days. Errors include a robust scatter floor.
    """
    time, flux, error = (np.asarray(a, dtype=float) for a in (time, flux, error))
    pieces = np.split(np.arange(len(time)), np.where(np.diff(time) > 0.3)[0] + 1)
    out = []
    for idx in pieces:
        if len(idx) < 30:
            continue
        t, f, e = time[idx], flux[idx], error[idx]
        cadence = np.median(np.diff(t))
        width = max(3, int(window / cadence) // 2 * 2 + 1)
        if len(t) < width:
            continue
        trend = median_filter(f, size=width, mode="reflect")
        y, dy = f / trend, e / trend
        scatter = 1.4826 * np.median(np.abs(np.diff(y) - np.median(np.diff(y)))) / np.sqrt(2)
        dy = np.maximum(dy, scatter)
        keep = (t > t[0] + window / 2) & (t < t[-1] - window / 2)
        # Remove only extreme positive excursions, preserving genuine deep dips.
        keep &= (y < np.median(y) + 8 * max(scatter, 1e-8)) & (trend > 0)
        out.append((t[keep], y[keep], dy[keep]))
    if not out:
        raise ValueError("No sufficiently long contiguous data segment")
    t, y, dy = (np.concatenate([p[k] for p in out]) for k in range(3))
    if len(t) < 200:
        raise ValueError("Fewer than 200 clean cadences")
    return t, y, dy


def scan(t, y, dy):
    max_period = min(10.0, np.ptp(t) / 2.5)
    if max_period <= 0.7:
        raise ValueError("Insufficient baseline")
    bls = BoxLeastSquares(t, y, dy)
    power = bls.autopower([0.06, 0.09, 0.13, 0.18, 0.24],
        minimum_period=0.7, maximum_period=max_period,
        frequency_factor=0.8, objective="likelihood")
    i = np.argmax(power.power)
    best = {k: float(power[k][i]) for k in
            ("period", "duration", "transit_time", "depth", "depth_err", "depth_snr", "power")}
    return bls, power, best


def depth_measure(y, dy, inside, outside):
    if inside.sum() < 2 or outside.sum() < 5:
        return None
    w = 1 / dy**2
    depth = np.average(y[outside], weights=w[outside]) - np.average(y[inside], weights=w[inside])
    error = np.sqrt(1 / w[inside].sum() + 1 / w[outside].sum())
    return {"depth": float(depth), "error": float(error), "snr": float(depth / error),
            "n": int(inside.sum())}


def diagnostics(t, y, dy, best, searcher=scan, shared=None):
    p, epoch, duration = best["period"], best["transit_time"], best["duration"]
    phase = (t - epoch + p / 2) % p - p / 2
    event = np.rint((t - epoch) / p).astype(int)
    inside = np.abs(phase) < duration / 2
    outside = (np.abs(phase) > duration) & (np.abs(phase) < min(3 * duration, p / 2))
    events = []
    for n in np.unique(event[inside]):
        d = depth_measure(y, dy, inside & (event == n), outside & (event == n))
        if d is not None:
            events.append({"event": int(n), "time": float(epoch + n * p), **d})
    odd = depth_measure(y, dy, inside & (event % 2 == 1), outside)
    even = depth_measure(y, dy, inside & (event % 2 == 0), outside)
    mismatch = None if odd is None or even is None else abs(odd["depth"] - even["depth"]) / np.hypot(odd["error"], even["error"])
    secondary_phase = (t - epoch + p) % p - p / 2
    secondary = depth_measure(y, dy, np.abs(secondary_phase) < duration / 2,
        (np.abs(secondary_phase) > duration) & (np.abs(secondary_phase) < min(3 * duration, p / 2)))
    if shared is None:
        inverse = searcher(t, 2 - y, dy)[2]
        # A sinusoid can masquerade as repeated box-shaped dips. This likelihood
        # comparison is a heuristic, not calibrated model odds.
        ls = LombScargle(t, y, dy, normalization="psd")
        frequency, power = ls.autopower(minimum_frequency=0.1,
            maximum_frequency=min(10, 0.5 / np.median(np.diff(t))), samples_per_peak=10)
        j = np.argmax(power)
        sinusoid = {"period": float(1 / frequency[j]), "delta_log_likelihood": float(power[j])}
    else:
        inverse = dict(shared["inverted"])
        sinusoid = dict(shared["sinusoid"])
    sinusoid["power_ratio_to_box"] = sinusoid["delta_log_likelihood"] / best["power"]
    return {"sinusoid": sinusoid, "events": events, "supported_events": sum(d["snr"] >= 2 for d in events),
        "odd_even_sigma": mismatch, "secondary": secondary, "inverted": inverse,
        "inverted_power_ratio": inverse["power"] / best["power"]}


def triage(best, diag):
    flags = []
    if diag["sinusoid"]["power_ratio_to_box"] > 1: flags.append("sinusoidal_variability_preferred")
    if best["depth_snr"] < 8: flags.append("low_formal_snr")
    if diag["supported_events"] < 3: flags.append("fewer_than_3_supported_events")
    if diag["odd_even_sigma"] is None: flags.append("odd_even_unmeasurable")
    elif diag["odd_even_sigma"] > 3: flags.append("odd_even_mismatch")
    if diag["secondary"] is None: flags.append("secondary_unmeasurable")
    elif diag["secondary"]["snr"] > 3: flags.append("secondary_eclipse_or_variability")
    if diag["inverted_power_ratio"] >= 0.8: flags.append("comparable_inverted_signal")
    if best["duration"] / best["period"] > 0.15: flags.append("large_duty_cycle")
    return flags
