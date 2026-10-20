# TIC 420110652, peak 1: diagnostic only

Training sectors [73, 74] select seed period 14.95138514 days. Native refinement gives 14.95114093 days, duration 0.032000 days and depth 7571 ± 857 ppm (formal selected fit error). 2 local events meet the individual support threshold. Original flags retained: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding. This did not pass the full discovery screen and is retained only under the coverage-diagnostic policy.

Sector 19: timing_prediction_inconclusive, timing spread 1.1696 days; Sector 20: timing_prediction_inconclusive, timing spread 1.1466 days. Inconclusive timing neither confirms nor reliably excludes the proposed ephemeris. Selected off-phase dip SNR 4.39 is an uncalibrated maximum, not a false-alarm probability or binary diagnosis.

The discovery plot was inspected: Narrow two-event diagnostic with noisy, sparsely populated bins; alternative peak in same star, not a second planet claim. The source checks below do not establish an isolated source. No host or novelty is established. No credible new planet claim, external submission or contact.

Both peaks belong to the same star and are alternative hypotheses. Do not count them as two planets or two searched stars.

## Source and quality review

The frozen 14.951141-day fit was checked separately using the existing sector 73/74 raw and processed pixel downloads. The sector 74 stack and both individual raw difference images were inspected: event 1 has weak mixed residuals, while event 2 is negative across the whole field. Their stack is entirely negative. The reported image moment is not valid host attribution. No consistent isolated dimming source is established.

Sector 73 has only one raw event (13 quality-zero inside exposures, 56 baseline); sector 74 has two (13 inside and 56 baseline each). All processed inside exposures carry quality flag 4096: 14 in sector 73 and 14 per event in sector 74, with zero quality-zero baseline exposures. Both processed image analyses and the raw sector 73 analysis fail the unchanged two-event gate. Missing usable coverage is not a nondetection. All failures are preserved.

Source provenance, input hashes, exposure counts and individual-image provenance are checked by `verify_pixels.py`. The target remains a low-priority unresolved diagnostic, with background/quality and sparse-coverage concerns. Neither competing period qualifies as a likely new planet candidate.
