# TIC 29439764: unresolved diagnostic

Training sectors [24, 25]. Native refinement: period 12.917508606 days, duration 0.048000 days, depth 11345 ± 1196 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Sparse noisy event sampling. Alternative to the original-screen period, not evidence for a second planet. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 51: timing_prediction_inconclusive, timing spread 1.2327 days. Sector 78: timing_prediction_inconclusive, timing spread 2.3997 days.

Training off-phase scan's selected maximum has formal SNR 6.54; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source and coverage checks below expose background/quality concerns; reliable host attribution remains incomplete. No secure host, novelty, or credible planet claim; retain for further review.

## Alternate-fit source check

Sector24 stack and both individual raw difference images were visually inspected. Event0 is negative across the entire field; event1 is positive across the entire field. The stack is nearly entirely negative (maximum formal pixel ratio0.010), with scattered relative structure rather than an isolated source. The numerical moment6.048pixels from the target is not a reliable source location. No Gaia attribution was attempted from it.

Raw sector24 events0/1 each have3quality-zero inside exposures and9baseline exposures. Processed counts differ at the window boundary:3/2inside exposures, all5flagged4096, and no quality-zero baseline. The processed source analysis fails the unchanged minimum-two-event gate. Sector25 has only one raw event2, with2quality-zero inside and9baseline exposures, so its source analysis also fails. No sector25 source image is claimed. The prior exact processed sector25 product404 is reused without another fetch; unavailable coverage/products are not nondetections or proof all alternative products are absent.

Classification: unresolved signal with background/quality and sparse-coverage concerns. No unique host, physical cause, planet exclusion or novelty claim. This competing fit uses the same observing epochs and is not independent planet evidence. Provenance, coverage, failures and plotted arrays are checked by `verify_pixels.py` and recorded in `source_review.json`.
