# TIC 29439764: unresolved diagnostic

Training sectors [24, 25]. Native refinement: period 12.528370979 days, duration 0.092736 days, depth 10048 ± 883 ppm (formal selected-fit error), 3 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Sparse noisy central depression. Alternative to the coverage-diagnostic period, not evidence for a second planet. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 51: timing_prediction_inconclusive, timing spread 1.1032 days. Sector 78: timing_prediction_inconclusive, timing spread 2.1499 days.

Training off-phase scan's selected maximum has formal SNR 6.80; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Image and quality checks below expose background and coverage concerns; reliable host/catalog attribution remains incomplete. No secure host, novelty, or credible planet claim; retain for further review.

## Image-source and coverage check

The sector24 raw stack and both individual difference images were visually inspected. All are negative across the whole field, with relative target/neighbor structure and gradients. The formal moment3.195pixels from the target is not a reliable host location in these backgrounds. No Gaia attribution was attempted from that moment.

Raw sector24 events0/1 have4/5quality-zero inside exposures and18baseline exposures each. Its processed product downloaded successfully, but all9inside exposures are flagged4096 and both baselines have zero quality-zero exposures; the processed image check fails the unchanged minimum-two-events requirement. Sector25 raw data contain only event4, with5quality-zero inside and18baseline exposures; its source analysis also fails the minimum-two-event gate. No sector25 image is claimed. Its exact processed target-pixel product returnedHTTP404; missing usable coverage or products are not nondetections or proof all other products are absent.

Classification: unresolved signal with background/quality and sparse-coverage concerns. No unique host, physical-cause certainty or planet exclusion. Same observing epochs as the QLP discovery, not independent recurrence. The competing coverage fit was subsequently checked separately and also remains limited by background/quality and sparse coverage; see its assessment. `verify_pixels.py` verifies provenance, frozen ephemeris, coverage, failed checks and plotted arrays; `source_review.json` records the assessment.
