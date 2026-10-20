# TIC43676101: compact discovery signal with a nearby known variable

**Superseded by source evidence:** [discovery images and PRF fits](../prf-43676101-20261012/ASSESSMENT.md) strongly localize the dimming near neighbor43676071, so deprioritize a planet on43676101. The initial photometric assessment below is retained.

The initial assessment recommended retaining this2.14777-day signal for source checks and frozen additional-sector testing. Its compact dip and depth are stable under alternate detrending, with positive detections in both discovery sectors. A nearby rotational variable creates a concrete contamination concern, but is **not** the target. Internal APC is suitable pending localization and later checks; this is not a likely-planet probability or a discovery.

Only discovery sectors52/53 were read. Added26/79 and reserved80 remain unopened, with light-curve caches absent. The terminal campaign evidence and complete cache/history preflight must be checked before new observations and a timing protocol frozen beforehand.

## Measurements

Original BLS P2.1477693228d, duration0.132d, depth480.23ppm, formal SNR13.02. The alternate global search yields2.1477648110d and470.46ppm. At the unchanged original clock, local-baseline totals are519.06±39.98ppm and506.77±40.89ppm for1.5/2.5d detrending. BLS and local baselines differ by construction.

| Detrending | Sector52 depth±error(ppm) / SNR | Sector53 depth±error(ppm) / SNR |
|---|---|---|
|1.5d|644.10±64.60 /9.97|441.44±50.90 /8.67|
|2.5d|660.78±66.90 /9.88|416.76±51.67 /8.07|

Ten events are measurable in each reduction, nine/eight individually supported at formal SNR≥2. The sector-depth differences are about2.46/2.89 formal sigma under independent white errors; retain this possible variability/dilution concern despite passing aggregate screening. Half-phase depth67.82±38.49ppm is not a significant secondary detection. Neither formal errors nor secondary non-detection exclude blends or binaries.

[discovery.png](discovery.png) was visually inspected. The folded dip is compact in both reductions, rather than the broad trough seen in some rotational false alarms. Modest surrounding folded structure and the sector depth difference remain limitations.

## Identity and catalogs

Exact target identity is Gaia DR3 4548837457047295232. The sole VSX60arcsec result is **different** Gaia DR3 4548837388327816704, labeled ROT at an approximately28arcsec separation using rounded VSX coordinates. No catalog period is supplied. It must not be described as target rotation or proven contamination without source evidence. NASA TOI/confirmed exact-TIC queries succeeded with no rows, a limited nonmatch that establishes no novelty.

[verification.json](verification.json) checks raw/source/catalog hashes and exact identity, reconstructs both reductions and independently reproduces20 event depths/errors. [sectors.json](sectors.json) separately checks four sector totals. Shared detrending and selected-period significance are not independently calibrated; no host probabilities are derived. Reproduce with `uv run python results/review-43676101-20261012/verify.py` and sibling `sectors.py`.

Next: localize discovery difference flux relative to the nearby variable before opening additional observations. Preserve the original clock, both detrendings and depth asymmetry in any subsequent review.
