# TIC 79111355, peak 0: diagnostic only

Training sectors [94, 95] select seed period 18.75606736 days. Native refinement gives period 18.84215452 days, duration 0.216000 days and depth 3696 ± 331 ppm (formal selected fit error). 2 individual events meet the support threshold. Retained discovery flags: fewer_than_3_supported_events, crowding_or_missing_crowding. Admitted only under a diagnostic follow-up policy; original failed gates are not waived.

Sector 1: timing_prediction_inconclusive, spread 13.8860 days; Sector 27: timing_prediction_inconclusive, spread 10.1182 days. Inconclusive prediction neither confirms nor reliably excludes the proposed signal. Off-phase selected dip SNR 3.58 is an uncalibrated maximum, not a false-alarm probability or binary classification.

The discovery plot was inspected: Two-event depression with asymmetric scattered structure. The coverage and individual-image checks below leave host attribution unresolved. Host attribution and novelty are unestablished. No credible new planet claim or external submission.

## Pixel availability and coverage audit

The unchanged raw-image analysis requires at least two accepted events in each sector. Each of sectors 94 and 95 has only one predicted event, so both runs fail that gate. No source image was produced or visually reviewed, and no host attribution can be made from this audit.

Sector 94 has 93 inside exposures: 32 with quality zero and 61 carrying flag 128, with 313 quality-zero baseline exposures. Sector 95 has 93 quality-zero inside and 373 baseline exposures. The exact requested TESS-SPOC target-pixel products returned HTTP 404 for both sectors. These errors establish only that those requested products were unavailable; they do not establish that every alternative product is absent.

Raw downloads, the 62-row neighboring-star query, analysis scripts, coverage counts and all failures are retained. `verify_pixels.py` checks their provenance and outcomes. Missing products and too few within-sector events are not nondetections. The initial coverage audit did not inspect individual events; the separate diagnostic below subsequently did so. No selection gate was relaxed. Held-sector timing remains inconclusive; the signal remains an unresolved diagnostic, not a likely new planet candidate.

## Separate individual-event diagnostic

The per-event map calculation was factored into `individual_difference_events`, preserving its exposure requirements and leaving the original aggregate two-event gate unchanged. Separate sector 94/95 maps are retained in `results/individual-pixels-79111355-20261011`; no cross-sector pixel coaddition was performed.

Both maps were visually inspected. Sector 94 has target-adjacent positive structure together with negative residuals immediately around it. Sector 95 is positive across the whole field, dominated by a background change rather than a clearly isolated dimming source. These two maps do not establish consistent source localization. The near-target sector 94 moment is not host proof; no Gaia attribution follows from it. The signal remains unresolved with background/source-systematics concerns.

Validation: all 49 tests passed, including a deterministic single-event neighboring-star eclipse injection that recovers the injected source and confirms the aggregate gate still rejects one event. Flagging the injected event excludes it. The existing two-event TIC149919534 sector75 difference, error and individual arrays were reproduced exactly after the refactor. These checks validate the calculation, not real-source confidence. Original coverage failures and exact-product HTTP404 errors remain intact.
