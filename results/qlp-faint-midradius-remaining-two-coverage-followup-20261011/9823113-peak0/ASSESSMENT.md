# TIC 9823113: unresolved diagnostic

Training sectors [79, 80]. Native refinement: period 15.062542728 days, duration 0.133056 days, depth 4749 ± 421 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, crowding_or_missing_crowding.

Visually inspected discovery plot: Broad noisy asymmetric depression. Two selected periods are alternative interpretations, not two planets. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 25: timing_prediction_inconclusive, timing spread 4.4208 days. Sector 26: ERROR (ValueError: Fewer than 200 clean cadences); not a nondetection.

Training off-phase scan's selected maximum has formal SNR 7.74; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source and quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Source and held-coverage audit

The sector 80 raw stack and both individual maps were inspected. Event 2 is negative across the field, while event 3 is positive across the field; their stack is entirely negative. Relative structure around the target and nearby star does not establish a consistent isolated source. No reliable host moment or Gaia attribution follows from these maps.

Both sector 79 predicted raw windows have all 57 inside exposures flagged2048, with no quality-zero baseline exposures. Its aggregate source analysis fails the unchanged two-event gate and produces no source image. Sector 80 has 58 quality-zero inside and 230 baseline exposures per event. Exact requested processed pixel products returned HTTP404 for both sectors; missing products or usable coverage are not nondetections, and other products may exist.

The held-sector 26 preprocessing failure was reproduced from the cached hash-verified product: 1,148 exposures include406 valid quality-zero flux/error pairs, but unchanged1.5-day preprocessing still raises `Fewer than 200 clean cadences`. This is not a transient download failure. Sector25 timing remains inconclusive.

The84-row neighboring-star query, files, counts, scripts, maps and failures are retained and checked by `verify_pixels.py`. This15.062543-day fit remains unresolved with background/quality concerns. The alternative 15.615863-day fit was subsequently checked and also remains unresolved with background/quality concerns. The fits share 58 inside exposures in sector 80 and are competing interpretations of one star.
