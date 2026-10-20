# TIC96166003: weak compact discovery signal remains unresolved

The0.955162-day signal persists under alternate detrending and appears in both discovery sectors. It warrants source/localization and frozen later testing, but is weaker than a validated planet candidate: the original formal SNR is8.40 and the unchanged-clock local measurement falls to6.94 with alternate detrending. Internal APC, with low confidence pending further checks, is appropriate if listed; these terms are not calibrated probabilities.

Only already-opened discovery43/44 were read. Added19 and reserved59 remain unopened, with their light-curve caches absent. The live parent batch must complete its terminal audit before either is opened, and timing/decision choices must be frozen first.

## Evidence

Original BLS period0.9551620376d, duration0.06d, depth293.77ppm. Local-baseline measurements at this exact unchanged clock are280.86±37.84ppm (SNR7.42) and277.43±39.97ppm (SNR6.94) for1.5/2.5d detrending. Forty/thirty-six measurable events yield eight/seven with individual formal SNR≥2. The alternate global search's best period0.9550329621d and276.04ppm are retained as sensitivity evidence, not adopted as a new clock.

| Detrending | Sector43 depth±error(ppm) / SNR | Sector44 depth±error(ppm) / SNR |
|---|---|---|
|1.5d|331.97±54.26 /6.12|232.13±52.80 /4.40|
|2.5d|298.17±57.49 /5.19|257.52±55.65 /4.63|

Neither sector alone confirms a planet. The depth differences are modest relative to formal errors; source contamination and correlated effects remain viable. The original half-phase diagnostic is2.43±37.62ppm, without a detected secondary. Sparse low-SNR individual dips, a secondary non-detection and beta1 do not validate the signal.

[discovery.png](discovery.png) was visually inspected: the folded dip is compact and stable in depth, with surrounding low-level structure and large scatter in individual cadences. Because the period is shorter than the original ±0.6d plotting span, duplicated folded-phase bins outside±P/2 are naturally empty; the displayed data cover one orbital cycle and are not separate confirmation.

## Catalogs and verification

Exact SIMBAD target identity is Gaia DR3 161856980718462208. VSX60arcsec and exact-TIC NASA TOI/confirmed-planet searches returned no rows successfully. This is a limited nonmatch, not a novelty claim or complete binary census.

[verification.json](verification.json) checks raw/source/catalog hashes and exact identity, reconstructs both discovery reductions and independently recomputes76 event depths/errors. [sectors.json](sectors.json) independently reproduces each sector's fixed-clock depth and error from precision sums. Shared preprocessing is not independently reimplemented; no global significance/FPP or source validation is claimed. Run `uv run python results/review-96166003-20261011/verify.py` and `uv run python results/review-96166003-20261011/sectors.py`.

Next: inspect discovery source localization before spending new observations. If source evidence permits, predeclare the timing family and outcomes for a later test after the batch audit. No shared scientific source or docs changed.

## Subsequent discovery-image evidence

Subsequent preliminary discovery difference images are near the target but weak (image SNR4.86/3.74, offsets0.65/0.39pixel). They do not securely identify the host; retain ambiguity. See [sector43](../pixels-96166003-s43-20261011/), [sector44](../pixels-96166003-s44-20261011/). No added or reserved sector was opened by this review.
