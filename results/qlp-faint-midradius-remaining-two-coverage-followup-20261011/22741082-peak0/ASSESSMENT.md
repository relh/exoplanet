# TIC 22741082: unresolved diagnostic

Training sectors [49, 50]. Native refinement: period 15.546693821 days, duration 0.181440 days, depth 4318 ± 349 ppm (formal selected-fit error), 3 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: A broad noisy depression with a large folded coverage gap. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 23: timing_prediction_inconclusive, timing spread 1.1391 days. Sector 76: timing_prediction_inconclusive, timing spread 1.1456 days.

Training off-phase scan's selected maximum has formal SNR 7.65; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source and quality checks below expose background concerns; reliable host attribution remains incomplete. No secure host, novelty, or credible planet claim; retain for further review.

## Image-source and quality check

Both raw stacks, all four individual raw event maps and the processed sector50 stack were visually inspected. Raw sector49event0 is positive across the field with column structure, event1negative across the field; sector50event2positive and event3negative over the illuminated field, with an edge discontinuity. Relative target features do not establish an isolated source. Raw formal moments at4.971/6.024pixels offset are not valid host locations in these backgrounds. The processed sector50stack has weak mixed residuals (maximum formal pixel ratio2.03), without reliable source localization. No Gaia attribution was attempted.

All raw predicted windows have26quality-zero inside exposures. Raw baseline counts are105/64 in sector49 and104/105 in sector50. Processed sector49event0hasall26inside exposures flagged4096 and8quality-zero baseline exposures; event1has26quality-zero inside and53baseline. The source analysis fails the unchanged minimum-two-event gate. Processed sector50has26quality-zero inside both events, baseline86/105, allowing a stack but not proving a source. Missing usable coverage is not a nondetection. Four image events passing coverage do not imply four supported photometric transits; the native fit supports three.

Classification: unresolved with background/quality concerns. Same observing epochs as QLP, no independent recurrence claim. No unique host, physical cause, planet exclusion or novelty claim. Provenance, frozen fit, coverage, failed processed check and plotted arrays are verified by `verify_pixels.py`/`source_review.json`.
