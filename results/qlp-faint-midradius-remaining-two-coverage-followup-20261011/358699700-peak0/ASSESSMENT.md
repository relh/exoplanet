# TIC 358699700: unresolved diagnostic

Training sectors [80, 81]. Native refinement: period 12.291004013 days, duration 0.133056 days, depth 8805 ± 721 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, crowding_or_missing_crowding.

Visually inspected discovery plot: Broad noisy depression; alternative to peak2, not evidence for a second planet. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 40: timing_prediction_inconclusive, timing spread 4.3318 days. Sector 53: timing_prediction_inconclusive, timing spread 2.9722 days.

Training off-phase scan's selected maximum has formal SNR 8.98; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source checks below favor neighboring-source contamination; exact variable identification remains unresolved. No secure host, novelty, or credible planet claim; retain for further review.

## Alternate-fit source check

The sector81 stack and both individual raw difference images were visually inspected. Both events show a compact positive feature near the same TIC358699657/faint-blend group as the competing16.417682-day fit, about3.067pixels from the target. Classification: likely neighboring-source contamination. No unique variable, calibrated PRF confidence or true period is established.

Sector81 has57quality-zero inside exposures for each event and229/230baseline exposures. Sector80 has only one predicted window, all58inside exposures flagged2048 and zero quality-zero baseline; its analysis fails the unchanged minimum-two-event gate. No sector80 source image or nondetection claim. The original exact processed-product404 checks remain applicable to these same sectors; no redundant fetch was made.

The competing fits' last native event centers are3524.633019261556 and3524.6577078193955BTJD (about2133seconds apart); their transit windows overlap. Earlier supported centers differ:3508.215337520509 versus3512.3667038060844BTJD. These fits reuse observing epochs and an overlapping dip, not independent evidence for two planets.

The previously queried neighbor group has no Gaia classifier or eclipsing-binary rows, which does not exclude an uncatalogued variable; its uncertain faint-source crossmatch remains retained. No additional Gaia query or unique-source attribution is claimed. See `results/gaia-358699700-neighbors-20261011/verification.json`. Source hashes, coverage, original processed failures and plotted arrays are verified by `verify_pixels.py` and recorded in `source_review.json`.
