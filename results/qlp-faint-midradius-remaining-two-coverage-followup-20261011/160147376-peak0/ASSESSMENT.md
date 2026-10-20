# TIC 160147376, peak 0: diagnostic only

Training sectors [73, 74] select seed period 15.35906398 days. Native refinement gives period 15.36079952 days, duration 0.039680 days and depth 6866 ± 773 ppm (formal selected fit error). 2 individual events meet the support threshold. Retained discovery flags: fewer_than_3_supported_events, crowding_or_missing_crowding. Admitted only under a diagnostic follow-up policy; original failed gates are not waived.

Sector 19: timing_prediction_inconclusive, spread 0.9128 days; Sector 20: timing_prediction_inconclusive, spread 0.9036 days. Inconclusive prediction neither confirms nor reliably excludes the proposed signal. Off-phase selected dip SNR 5.38 is an uncalibrated maximum, not a false-alarm probability or binary classification.

The discovery plot was inspected: Two-event feature with sparse in-event bins and large changes in scatter. Source and quality checks below expose background/coverage concerns; reliable host attribution remains incomplete. Host attribution and novelty are unestablished. No credible new planet claim or external submission.

Peaks 0 and 1 are alternative hypotheses in the same star, not two planets or two searched targets.

## Alternate-fit source check

Using this fit's unchanged frozen ephemeris, sector73 contains only one predicted image event: raw/processed each have 15 quality-zero inside exposures plus two flagged32; baseline quality-zero counts are 33/34. Both image analyses fail the minimum-two-events gate. No sector73 source image is claimed.

Sector74 raw images cover two events, with 18/17 quality-zero inside and 68/69 baseline exposures. The stack and both individual images were visually inspected: event1 is negative across the whole field, event2 positive across the whole field. Relative target and neighboring features coexist with background structure. The formal stack moment offset of 3.243 pixels is not a reliable host location. Processed sector74 events each have all17 inside exposures flagged4096 and no quality-zero baseline, so the processed source check also fails. Missing usable coverage is not a nondetection.

Classification: unresolved with background and quality/coverage concerns; no secure host or physical-cause attribution. No Gaia attribution from invalid moments, gate relaxation or planet exclusion. These are the same observing epochs as the competing fit, not independent planet evidence. `verify_pixels.py` verifies the raw/processed file identity, frozen fit, coverage, failures and plotted arrays; `source_review.json` records the review.
