# TIC 280051317, peak 1: background and quality concerns

Training sectors [67, 68, 69] select seed period 14.32295111 days. Native refinement gives 14.34485330 days, duration 0.181440 days and depth 2019 ± 232 ppm (formal selected fit error). 4 local events meet the individual support threshold. Original flags retained: crowding_or_missing_crowding. The discovery screen admits this signal with unmeasured aperture crowding; that is not planet validation.

Sector 1: timing_prediction_inconclusive, timing spread 6.6414 days; Sector 2: timing_prediction_inconclusive, timing spread 6.5391 days. Inconclusive timing neither confirms nor reliably excludes the proposed ephemeris. Selected off-phase dip SNR 5.55 is an uncalibrated maximum, not a false-alarm probability or binary diagnosis.

The discovery plot was inspected: Broad shallow depression with scatter and phase gap; source/systematics review needed. Initial source and quality checks are below; catalog and full host validation remain incomplete. No host or novelty is established. No credible new planet claim, external submission or contact.


## Source and quality diagnostics

Raw sector 67/68/69 difference images each include two events at the frozen ephemeris. All three plots were visually inspected. Sector 67 shows field-wide positive structure; sector 68 has a field-wide positive gradient with target/neighbor features; sector 69 has a large field-wide positive offset with target/neighbor features. These maps do not establish a repeatable compact variable source. Formal maxima and moments are invalid as host confidence in these background-dominated maps.

All three processed TESS-SPOC pixel files downloaded successfully, but each failed the unchanged minimum-two-image-event requirement. Inspection of the archived quality masks finds every sampled in-event exposure flagged 4096: 156 in sector 67 (78/78), 158 in sector 68 (79/79), and 118 in sector 69 (78/40), 432 total and zero quality-zero exposures. Only sector 68 event 2 has any accepted local baseline exposures (135); the other five event windows have none. The failed image checks are retained rather than relaxed or converted to nondetections.

This strengthens a background/quality artifact concern, not a definitive physical cause or exclusion. The raw images use the same photons as QLP and no full spatial background model; no Gaia host lookup was inferred from invalid centroids. Raw identity/hashes, frozen fit identity, processed quality counts and retained failures pass verify_pixels.py / source_review.json. No credible planet candidate or unique host is established.
