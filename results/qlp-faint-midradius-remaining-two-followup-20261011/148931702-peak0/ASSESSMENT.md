# TIC 148931702: unresolved diagnostic

Training sectors [74, 75]. Native refinement: period 13.848450039 days, duration 0.133056 days, depth 3696 ± 433 ppm (formal selected-fit error), 4 supported events. Original flags: alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: A noisy central depression with asymmetric neighboring structure; scatter varies strongly with time. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 14: timing_prediction_inconclusive, timing spread 1.8682 days. Sector 15: timing_prediction_inconclusive, timing spread 1.8376 days.

Training off-phase scan's selected maximum has formal SNR 5.27; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source diagnostics below expose background concerns; further source modeling and catalog attribution remain incomplete. No secure host, novelty, or credible planet claim; retain for further review.

## Image-source check

Both sector74/75 raw stacks and all four individual difference images were visually inspected. Sector74 events0/1 and sector75 event2 are negative across the entire field; sector75 event3 shows a positive field-wide gradient. Relative target-region features do not establish a consistently isolated source. The sector74 near-target moment (0.175 pixels) and sector75 offset moment (3.951 pixels) are not reliable host localizations in these backgrounds. No Gaia host attribution was attempted from these moments.

All predicted in-event raw exposures have quality zero: 58/58 in sector74 and 57/57 in sector75; each local baseline has 230 quality-zero exposures. Passing quality flags does not guarantee a clean background. Exact checked SPOC target-pixel products returned HTTP404 in both sectors; this is missing-product evidence, not a nondetection or proof that every alternative product is absent.

Classification: unresolved signal with background/source-systematics concern. Same-epoch raw images do not supply independent recurrence evidence. No secure host, physical cause, planet exclusion, or novelty claim. Frozen ephemeris and event gates were unchanged; source hashes, coverage and failures are verified by `verify_pixels.py` and recorded in `source_review.json`.
