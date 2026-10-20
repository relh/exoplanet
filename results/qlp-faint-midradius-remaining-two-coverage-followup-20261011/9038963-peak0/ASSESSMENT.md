# TIC 9038963: unresolved diagnostic

Training sectors [23, 24]. Native refinement: period 13.685118962 days, duration 0.181440 days, depth 4083 ± 493 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Sparse noisy event sampling and a large folded coverage gap. The two selected periods are alternative interpretations of these data, not evidence for two planets. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 50: timing_prediction_inconclusive, timing spread 4.3591 days. Sector 77: timing_prediction_inconclusive, timing spread 8.6059 days.

Training off-phase scan's selected maximum has formal SNR 5.29; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. The source and quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Source and coverage checks

Both corrected raw stacks and all four individual maps were inspected. Sector 23 event -1 is negative across the field, while event 0 is positive with column structure. Both sector 24 events are negative across the field with column structure. These maps do not establish a consistent isolated dimming source, and their image moments do not identify a reliable host. No Gaia inference was made.

Each raw event has nine quality-zero inside exposures. Sector 23 baseline counts are 35/36; sector 24 counts are 36/35. Both processed sector 23 windows are fully flagged: event -1 has eight exposures flagged4096 and one flagged128; event 0 has nine flagged4096. Sector 24 event 1 has nine quality-zero inside exposures, but event 2 has all nine flagged32768. Both processed analyses fail the unchanged two-event gate. Missing usable coverage is not a nondetection.

Initial cutout requests contained an incorrect declination due to a local template-substitution error and returned non-ZIP responses. These attempts are preserved in directories named `incorrect-request` and excluded from scientific interpretation. Corrected cutouts use separate cache paths, and `verify_pixels.py` explicitly checks their requested coordinates against RA222.105939873631, Dec29.9979955655275. The 41-row neighbor query, raw/processed files, failures, coverage and maps are retained.

This 13.685119-day fit remains unresolved with background/quality concerns. The alternative 14.979057-day fit was subsequently checked separately: negative raw field backgrounds, weak processed residuals and sparse coverage also leave its host unresolved. It is not a second planet claim.
