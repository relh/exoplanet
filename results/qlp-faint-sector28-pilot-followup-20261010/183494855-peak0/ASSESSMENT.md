# TIC 183494855: likely off-target contamination near TIC 183494856

Native QLP Sector 28 has seven supported dips at refined period 3.065659656
days, duration 0.1056 days and epoch BTJD 2063.209753545. The fixed-depth
measurement is 4,812 ± 328 ppm (formal SNR 14.68). The discovery plot was visually
inspected: the folded dip is apparent, but its shape alone does not establish
its source or planetary nature. The original crowding flag remains.

Reserved Sectors 1 and 13 give −1,307 ± 453 and −2,356 ± 491 ppm at unchanged
timing. Prediction spreads of 0.7913 and 0.4571 days are much wider than the
transit duration, so these are inconclusive timing checks, not clean exclusions.
The exploratory secondary scan selects 1,349 ± 317 ppm at phase 0.5914, but
similar selected brightening and uneven event strengths prevent interpreting
that uncalibrated scan as binary confirmation.

Same-epoch SPOC28 gives only 290 ± 305 ppm (SNR 0.95), substantially weaker
than QLP28. These reductions use the same photons and are not independent
observations. The strong processing dependence warrants a pixel source check.

The TESScut difference image was visually inspected and shows a compact positive
source away from the target: eight generic pixel windows, formal peak SNR 248.53,
moment 3.367 pixels from the target and 0.060 pixels from TIC 183494856 (T=14.81).
The fainter TIC 183496337 (T=16.36) lies 0.510 pixels from the moment. The pixel
window count need not equal the seven QLP supported events because the sampling
and quality masks differ. This is convincing off-target evidence, but not a
calibrated PRF confidence interval or unique component/class identification.
Raw background and catalog motion are not fully modeled.

A Gaia lookup maps two neighbors with TIC Gaia identifiers to two DR3 sources;
no classifier or eclipsing-binary rows were returned. TIC 183496337 has no TIC
Gaia identifier and remains unassessed by that mapping method. The initial
missing-identifier error was retained before the explicit missing-ID handling.
Catalog nonmatches do not establish novelty or rule out variability. QLP archive
queries for TIC 183494856 contain no Sector 28 or 1 products; the resulting
missing-product errors are retained, not counted as null light-curve results.

Disposition: likely off-target contamination near TIC 183494856, with a nearby
fainter blend unresolved. No new planet candidate is promoted. Sector 27 remains
unopened as target photometry. No external submission or contact.

Artifacts with raw URLs and hashes:
- `results/qlp-faint-183494855-reduction-20261010`
- `results/neighbors-183494855-20261010`
- `results/tesscut-183494855-s28-20261010`
- `results/gaia-183494855-neighbors-20261010`
- `results/neighbor-183494856-20261010`
