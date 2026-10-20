# TIC96166003: mixed sector59 measurements, all timing-inconclusive

Sector59 was opened after the coordinator reviewed and committed the fixed prediction plan. The primary expanded clock gives positive dimming, but the secondary expanded clock and both original discovery clocks do not. All four predictions have timing spreads exceeding their half-duration criteria. This is mixed evidence, not a robust independent recovery or a sensitivity-qualified planet exclusion.

| Frozen timing family | Window(d) | Depth ± formal error(ppm) | Formal SNR | Supported events | Timing spread(d) | Outcome |
|---|---|---|---|---|---|---|
|19/43/44 expanded **primary**|1.5|264.9±51.9|5.10|3|1.34665|Timing-inconclusive|
|43/44 original|1.5|−167.0±47.1|−3.55|0|0.37204|Timing-inconclusive|
|19/43/44 expanded sensitivity|2.5|−72.4±62.4|−1.16|0|0.15476|Timing-inconclusive|
|43/44 original|2.5|−163.5±50.6|−3.23|0|0.41754|Timing-inconclusive|

The primary expected formal SNR was4.57. Its positive nominal SNR5.10 and three supported events are retained, but cannot override the1.35-day prediction envelope. The expanded sensitivity clock differs from the primary; its negative depth is not simply a same-clock detrending comparison. Negative depths denote fitted brightening relative to the chosen baseline, not a physical negative transit. No stronger alternative or profile maximum replaced the primary.

The inspected plot shows a primary negative feature near the predicted center amid surrounding structure. The other frozen clocks align different variations. All measurements use the same59 photons and do not form independent tests of planet probability. The full accepted timing islands were preserved; no apparently favorable branch was removed to make the prediction precise. Previous source ambiguity, weak19 fixed predictions, selected-family assumptions and duration-grid endpoint concerns remain.

`PREPARATION.md` preserves the prepared state; the unchanged `plan.json` and executable retain the protocol committed before opening. The independent verifier reconstructs all four unchanged clocks, raw identity/hash and reductions, weighted total/event measurements, propagated spreads, expected sensitivity and decision rules. Frozen input/source hashes and freeze-before-download chronology pass. Arithmetic reproduction does not calibrate correlated noise or establish a host or planet.

Sector59 is now deliberately opened; all listed sectors19/43/44/59 have been examined. Future timing searches or selection of a different alias would be retrospective and must preserve these outcomes. Earlier cache-absence verifiers describe their historical pre-opening stages and must not be blindly rerun as current tests. No new fit, clock optimization, selected omission or additional observation was performed in this experiment.
