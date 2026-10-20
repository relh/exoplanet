# TIC 18119757: unresolved diagnostic

Training sectors [79, 80]. Native refinement: period 13.990828831 days, duration 0.216000 days, depth 3439 ± 337 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, crowding_or_missing_crowding.

Visually inspected discovery plot: Broad noisy central depression with large gaps in the time series. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 25: timing_prediction_inconclusive, timing spread 3.1656 days. Sector 26: ERROR (ValueError: Fewer than 200 clean cadences); not a nondetection.

Training off-phase scan's selected maximum has formal SNR 4.22; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. The source and quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Source and coverage checks

The sector 80 raw stack and all four individual raw event maps across sectors 79/80 were inspected. Every individual map is negative across the field; sector 79 also has a strong gradient. No consistent isolated source is established. The original sector 79 moment calculation failed with `No positive difference flux`; that failure is retained. A separate individual-map diagnostic displays the data without estimating a source moment. No Gaia host inference was made.

Sector 79 events have 56/16 quality-zero inside exposures, plus 37/77 flagged 2048, with 186 quality-zero baseline exposures each. Sector 80 inside counts are 93/94 and baseline counts 373/374, all quality zero. The exact requested processed pixel products returned HTTP404 for both sectors; this does not establish that all alternatives are absent or that the signal is absent. The 100-row neighboring-star query and all source evidence are retained.

The held sector 26 error was reproduced from its cached, hash-verified FITS product. It contains 1,148 exposures, 406 with valid quality-zero flux/error pairs, but the unchanged 1.5-day preprocessing raises `Fewer than 200 clean cadences`. This is a data-quality/preprocessing limit, not a transient download error and not a nondetection. The sector 25 timing prediction remains inconclusive.

`verify_pixels.py` checks source provenance, exposure counts, individual-map hashes and the held-coverage audit. Background and quality concerns prevent reliable host attribution; this remains an unresolved diagnostic, not a likely planet candidate.
