# TIC 74189224: unresolved diagnostic

Training sectors [103, 104]. Native refinement: period 13.125585192 days, duration 0.073600 days, depth 2550 ± 308 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: A central depression amid asymmetric structure and a large folded coverage gap. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 12: timing_prediction_inconclusive, timing spread 4.8672 days. Sector 13: timing_prediction_inconclusive, timing spread 4.7923 days.

Training off-phase scan's selected maximum has formal SNR 3.72; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source/quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Source-image and coverage review

The raw sector 103 stack and all three usable individual event maps across sectors 103/104 were inspected. Each is positive across the field, with stronger off-target features that change between sectors. The sector 103 relative feature is near bright TIC74181772 (T=10.60), close to the stamp edge. Projecting the same catalog position into sector 104 places it at (5.54,10.89), outside the image footprint and away from that event's stronger feature near (1,9). This positional comparison establishes neither the variable source nor a binary identification. Background, edge truncation and blending prevent reliable host attribution; no Gaia inference was made.

Sector 103 events have 32/32 quality-zero inside exposures and 127 baseline exposures each. Sector 104 event 2 has 32 quality-zero inside and 126 baseline exposures; event 3 has all 32 inside exposures flagged 2048 and no quality-zero baseline. Its original aggregate source analysis fails the unchanged two-event gate. The separate individual diagnostic retains event 2 without changing that gate. Both exact requested processed pixel products returned HTTP404, not a nondetection or proof all alternative products are absent.

The 766-row neighboring-star query, pixel provenance, failures and plots are retained and verified by `verify_pixels.py`. An initial plot/view request referenced the absent sector 104 aggregate output and failed; the subsequent separate plot shows only the three usable individual events. Both reserved-sector timing checks remain inconclusive. The signal is an unresolved diagnostic with background/contamination concerns, not a likely new planet candidate.
