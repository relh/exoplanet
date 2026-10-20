# TIC 9823113: unresolved diagnostic

Training sectors [79, 80]. Native refinement: period 15.615862845 days, duration 0.133056 days, depth 4604 ± 419 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Broad shallow depression with changing scatter. Two selected periods are alternative interpretations, not two planets. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 25: timing_prediction_inconclusive, timing spread 1.8301 days. Sector 26: ERROR (ValueError: Fewer than 200 clean cadences); not a nondetection.

Training off-phase scan's selected maximum has formal SNR 5.55; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source and quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Alternative-fit source review

The original downloads were reused with this fit's frozen 15.615863-day ephemeris. The raw sector 80 stack and both individual maps were inspected. Both individual maps are positive across the field; event 2 has a strong column pattern and event 3 has different relative structure near the target and neighbor. No consistent isolated dimming source or reliable host moment is established. No Gaia attribution was made.

Both sector 79 windows again have all 57 inside exposures flagged2048, with0/115 quality-zero baseline exposures; the unchanged aggregate image gate fails. Sector80 events have58 quality-zero inside exposures each and229/230 baseline exposures. Original exact-product HTTP404 errors for processed pixels remain applicable and were retained without another download attempt. Missing usable data or products are not nondetections.

The prior held-sector26 audit also applies: the same cached product has406 valid quality-zero flux/error pairs, but unchanged preprocessing yields fewer than200 clean cadences. No new independent validation is claimed.

An exposure-overlap audit finds that the two period fits share58 of their116 quality-zero inside exposures in sector80, in the window BTJD3504.990434–3505.122376. Shared data are not independent confirmations or evidence for two planets. This overlap does not establish equality of the full event baselines or periods. `verify_pixels.py` checks provenance and coverage; neither fit currently qualifies as a likely new planet candidate.
