# TIC 356743185: unresolved transit-like signal

Training sectors [74, 75]. Native refinement: period 13.809278635 days, duration 0.133056 days, depth 1851 ± 200 ppm (formal selected-fit error), 4 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: A shallow central depression is visible in substantial scatter, with nearby structure. Four supported training events; source checks pending. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 14: timing_prediction_inconclusive, timing spread 3.4994 days. Sector 20: timing_prediction_inconclusive, timing spread 3.1518 days.

Inconclusive timing neither confirms nor reliably rejects recurrence. The source checks below supersede the initial pending status; additional validation remains incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.285544, depth 1407 ± 369 ppm, formal SNR 3.82, 2 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.

## Source and quality checks

All three available difference plots were visually inspected. Raw sectors 74 and 75 each include two events: sector74 is entirely negative across the cutout, while sector75 is positive across the field with a distant edge maximum. Neither gives a reliable compact dimming-source position; moment offsets must not be used for host attribution.

The processed TESS-SPOC sector74 file downloaded successfully but the existing image-event gate failed. A separate frozen-ephemeris coverage audit finds 57 and 58 in-event exposures, all with quality4096 and none with quality zero. Local out-of-event windows have 9 and 27 quality-zero exposures. Thus no clean in-event exposures are available for either predicted eclipse in that product. This is missing usable evidence, not a transit nondetection.

Processed sector75 yields two image events, but the difference map is weak and mixed, with maximum formal pixel SNR2.60; it provides no calibrated source identification. The three images and flagged sector74 exposures raise an artifact/background concern. Same-sector products share photons; no separate-epoch confirmation follows. Source hashes, processed-file provenance and the retained gate failure are checked in `verify_pixels.py` / `source_review.json`; the sector74 coverage audit is in `../../spoc-pixels-356743185-s74-20261011/`. No host, planetary origin or novelty established.
