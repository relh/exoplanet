# TIC 181272177: likely neighboring-source contamination

Training sectors [88, 89]. Native refinement: period 1.976920379 days, duration 0.133056 days, depth 3124 ± 111 ppm (formal selected-fit error), 24 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Broad central depression with pronounced positive shoulders on both sides. This shape raises variability or processing concerns; source checks pending. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 8: timing_prediction_inconclusive, timing spread 0.9387 days. Sector 35: timing_prediction_inconclusive, timing spread 0.6313 days.

Inconclusive timing neither confirms nor reliably rejects recurrence. The source checks below supersede the initial pending status; full quality and host validation remains incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.758333, depth 653 ± 174 ppm, formal SNR 3.74, 2 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.

## Source check

Raw sector-88 and sector-89 difference images contain 14 and 15 events at the frozen ephemeris. Both plots were visually inspected: each shows a compact positive source displaced from the target toward the same neighboring group. Diagnostic offsets from the target are 2.335 and 2.142 pixels. TIC 181272135 is nearest to the moments (0.051 and 0.178 pixels); TIC 181272134 and other fainter neighbors remain unresolved. This supports likely neighboring-source contamination without uniquely identifying the variable.

Both exact TESS-SPOC processed-product requests returned HTTP 404; those failures are retained and are not nondetections. The raw images share photons with QLP, use local temporal subtraction without a complete background model, and provide no calibrated PRF astrometric confidence. Source provenance is checked in `verify_pixels.py` and `source_review.json`.

Gaia DR2-to-DR3 lookup maps seven selected TIC sources to seven DR3 sources. The closest neighbor TIC 181272135 maps to DR3 5528839352073186176, classified ECL and listed in the eclipsing-binary table with period 3.954239366 days. Half that period, 1.977119683 days, differs from the QLP period by 17.22 seconds. The spatial agreement and approximate half-period match strongly support contamination by a cataloged eclipsing binary, without a calibrated joint confidence or exclusion of other blended variables. A joint epoch/model comparison remains undone. The target itself is classified SOLAR_LIKE. Catalog provenance is retained in `../../gaia-181272177-neighbors-20261011/`.
