# TIC 154570351, peak 0: unresolved coverage diagnostic

Training sectors [74, 75]. Native refinement: period 14.005430989 days, duration 0.181440 days, depth 3989 ± 404 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, crowding_or_missing_crowding. This follow-up was admitted under the separate coverage-diagnostic policy, not the original full screening gate.

Visually inspected discovery plot: Broad shallow central depression with an uneven bottom and positive shoulder in noisy, gapped data. The displayed plot uses the discovery seed; the native refinement above differs.

Sector 14: timing_prediction_inconclusive, timing spread 2.2045 days. Sector 15: timing_prediction_inconclusive, timing spread 2.1680 days.

Training-only off-phase scan maximum: phase 0.775281, depth 1860 ± 291 ppm, formal SNR 6.40. Selected over phase and duration, not calibrated significance or proof of a secondary eclipse.

Inconclusive timing neither confirms nor reliably rejects recurrence. Further source and catalog checks remain incomplete. No secure host, novelty or credible planet claim.


## Initial source and quality checks

Both raw stacked difference images were visually inspected (two accepted events each). Both are entirely negative across the field: sector74 has relative target/neighbor structure, while sector75 has a broad gradient. Their moments cannot identify a transit host, even where a moment lies close to the target. No Gaia inference was made from these unreliable positions.

Both processed SPOC pixel products downloaded successfully, but their analyses fail the unchanged minimum-two-events check. All313in-event exposures across four predicted windows are flagged:312carry4096 and one carries128. None is quality zero. Sector74 events0/1 each have78flag4096 in-event exposures, with157/156quality-zero baseline exposures. Sector75 event2 has78flag4096 plus one128, with152quality-zero baseline exposures; event3 has78flag4096, with54quality-zero baseline exposures. Missing accepted processed coverage is not a nondetection or an independent rejection of a planet.

Raw products mark78in-event exposures quality zero in each of the four windows; sector75 event2 has one additional128flag. This difference in flags between reductions does not make raw exposures independent confirmation. Raw baseline counts are313/314 and296/231 for sectors74/75. All failures, hashes and counts are retained; no gates were relaxed.

[Source verification](source_review.json), [sector74 processed audit](../../spoc-pixels-154570351-s74-20261011/coverage.json), [sector75 processed audit](../../spoc-pixels-154570351-s75-20261011/coverage.json). Classification: unresolved signal with strong background/quality concerns, exact physical cause and host unknown. Reserved timing remains inconclusive. No secure new planet candidate.
