# TIC 80387959: transit-timescale correlated-noise audit

**The recurring dimming survives this additional noise diagnostic, but later-sector precision is weaker than the white-noise fit suggests.** The largest time-averaging factors are 1.39 in sector 63 and 1.34 in sector 100. The sector-100 depth/error ratio falls from 5.86 to 4.37, and reaches 2.96 when one event is omitted. These are conditional diagnostic ratios, not calibrated detection significances or exoplanet probabilities. Host attribution remains unresolved; no disposition change is justified.

| Sector | Depth (ppm) | White error (ppm) | Maximum beta | Adjusted error (ppm) | Minimum omitted-event depth/error |
|---|---:|---:|---:|---:|---:|
| 10 | 1038 | 109 | 1.04 | 113 | 7.00 |
| 36 | 813 | 87 | 1.06 | 92 | 7.22 |
| 37 | 904 | 91 | 1.15 | 105 | 6.72 |
| 63 | 807 | 93 | 1.39 | 130 | 5.16 |
| 90 | 613 | 89 | 1.03 | 92 | 5.77 |
| 100 | 582 | 99 | 1.34 | 133 | 2.96 |

All full and single-event-omission depths remain positive. The depth estimates themselves are unchanged from the [joint local-baseline analysis](../strongest-80387959-shape-20261012/ASSESSMENT.md). The present result does not explain the older/newer depth difference or replace the original frozen holdout decisions.

## What the refereed method adds

[Pont, Zucker & Queloz (2006), MNRAS 373, 231–242](https://doi.org/10.1111/j.1365-2966.2006.11012.x), especially sections 2.3–2.6, estimates noise on transit timescales from averages of consecutive measurements. Correlated points do not supply as much independent information as their white-noise errors suggest. This run adapts that idea to our existing weighted local fits; it does **not** reproduce their exact sliding out-of-transit estimator or claim their survey calibration transfers to TESS.

The paper was read through the publisher's web rendering and its [author manuscript](https://arxiv.org/abs/astro-ph/0608597). Direct publisher download returned HTTP 403; that response is preserved in [literature.json](literature.json). The successful PDF URL, retrieval time and SHA-256 are in [literature-arxiv.json](literature-arxiv.json); downloaded documents stay under ignored `data/`.

## Frozen experiment

[plan.json](plan.json) was written before calculation. Only the six previously inspected primary-fit NPZ files were used, with input hashes recorded. P=4.192168718052227 days, BTJD epoch=1575.375831123655, duration=0.092736 days and exposure-integrated box design are unchanged. There is no new observation, clock search, clipping or transit selection.

For each sector, refit the box and separate event intercepts/slopes jointly. Divide residuals into equal-count nonoverlapping bins approximating 0.5, 1 and 2 transit durations, with starting offsets of zero and half a bin. Every event boundary or cadence gap exceeding 1.5 times the sector's median cadence starts a new segment; no bin bridges a gap. Incomplete bins are discarded. All six declared scales/offsets are retained; configurations with fewer than eight bins are marked insufficient. At full-sample level the longest half-offset configuration fails this count rule in sectors 10 and 100. Omission failures also remain in [results.json](results.json).

The comparison denominator is generated from 2,000 deterministic independent Gaussian realizations using the actual per-cadence errors and residual-scatter floor. Each realization refits the identical signal and baseline design. Thus sampling gaps, heteroskedastic errors and covariance induced by baseline removal are included in the **white reference**. Beta is observed RMS of bin means divided by the root-mean-square white expectation; the maximum across all eligible configurations, floored at one, multiplies the original conditional depth error. This maximization is a declared sensitivity envelope, not a fitted stochastic covariance model. All event omissions repeat fitting and the noise audit.

## Verification and limitations

[verify.py](verify.py) independently solves the normal equations, reproduces depth/error and residual-bin arithmetic, checks event/gap boundaries, and derives the white bin variance analytically through the projection matrix. Its 6,266 checks pass; simulation denominators differ from exact expectations by at most 1.39%. [verification.json](verification.json) preserves the outcome.

Deterministic synthetic tests recover zero and both signed 1,000-ppm injections in all six noiseless designs. A 200-replicate sector-90 null experiment gives median maximum beta 1.14 for independent noise and 3.50 for within-segment AR(1) noise with phi=0.85; depth scatter rises from 84 to 291 ppm. This confirms response to the specified correlated process, **not** correct interval coverage for real stellar/systematic noise. The nonzero white maximum reflects finite-bin scatter and maximization. [test_method.py](test_method.py), [synthetic-tests.json](synthetic-tests.json), and [injection-tests.json](injection-tests.json) retain these checks.

Only a few event windows exist per sector. Local baseline removal and fitted-box subtraction can hide long-timescale noise or coherent errors that resemble the selected signal. Short residual stretches cannot calibrate rare artifacts, original target/period selection, shared cross-event systematics, ephemeris uncertainty, pipeline attenuation or contamination. Uniform beta inflation is approximate; it is not a Gaussian-process likelihood, empirical false-alarm probability, or astrophysical false-positive probability. Different products use shared photons. No planet radius or combined planet confidence is inferred.

[noise-diagnostic.png](noise-diagnostic.png) shows the conditional errors before and after inflation.

```sh
OPENBLAS_NUM_THREADS=1 uv run pytest -q results/paper-vetting-80387959-20261012/test_method.py
OPENBLAS_NUM_THREADS=1 uv run python results/paper-vetting-80387959-20261012/verify.py
```
