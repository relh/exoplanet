# TIC 148001520: unresolved transit-like signal

Training sectors [87, 88]. Native refinement: period 4.355527686 days, duration 0.092736 days, depth 2797 ± 290 ppm (formal selected-fit error), 9 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Shallow central depression visible amid substantial scatter. Nine supported native training events; source checks pending. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 6: timing_prediction_inconclusive, timing spread 2.5708 days. Sector 7: timing_prediction_inconclusive, timing spread 2.5458 days.

Inconclusive timing neither confirms nor reliably rejects recurrence. The source checks below supersede the initial pending status; additional validation remains incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.094987, depth 1358 ± 442 ppm, formal SNR 3.07, 3 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.

## Source checks

Raw sector87 and sector88 maps contain five and seven image events at the frozen ephemeris. Both plots were visually inspected. Each has a field-wide positive difference plus an enhancement displaced from the target. Uncorrected moment offsets are0.978 and1.315pixels, toward faint TIC738285152 and TIC148001522. These numbers are diagnostic only: the uniform background contribution can bias moments, and no calibrated PRF confidence is available. The feature is not sufficient to assign a contaminating star or confirm the target as host.

Both exact processed TESS-SPOC pixel requests returned HTTP404; errors and URLs are retained, not interpreted as nondetections or absence of all possible products. Source provenance passed `verify_pixels.py` / `source_review.json`. The wider-cutout background check below extends this initial test. The raw maps share photons with QLP; independent-sector timing remains inconclusive. No secure source, novelty or credible planet claim.

## Wider background check

The 31-by-31 cutouts reuse the same five/seven events and frozen ephemeris. The unchanged weighted spatial-plane diagnostic excludes catalog sources brighter than Tmag17 plus the target, with both two- and three-pixel masks. Sector87 has211/25 background pixels; sector88 has244/42. Both masks fit successfully in both sectors. All four wide difference/background plots and the corrected local four-panel view were visually inspected.

The feature near the target persists after both background corrections. Using the existing local moment helper at the original raw-map peak anchors gives target offsets0.969/0.973pixels in sector87 and1.323/1.322pixels in sector88 for the two mask radii. The closest listed source remains faint TIC738285152, with TIC148001522 and other unresolved neighbors nearby. The corrected image peaks and local moments favor further investigation of contamination; they do not provide calibrated astrometric confidence or distinguish the individual components. Sector87 also contains a stronger residual at the cutout edge, so its global maximum is not used to locate this signal.

The offset survives these two spatial background choices, strengthening the contamination concern. These are the same photons and a post-selection diagnostic; source-dependent systematics can survive a plane fit. No secure host or planet claim. Scripts, raw hashes, both mask results and validation are retained in `wide-background-plan.json`, `corrected_moments.py`, `corrected-moments.json`, `verify_background.py` and `background_review.json`.

Gaia maps the four selected TIC entries to four DR3 sources. TIC148001522 maps to DR3 5577004622855797504, classified ECL and listed with binary period0.290771761days. This is different from the QLP4.355527686-day period; a matching-period source identification has not been established. The cataloged binary lies in the unresolved offset group, while the closest moment entry is the fainter TIC738285152. The spatial and variability evidence strengthen contamination as a concern, without selecting a unique component or proving an alias. Catalog query and verification are retained in `../../gaia-148001520-neighbors-20261011/`.
