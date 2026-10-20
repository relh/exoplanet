# Event-baseline and omission checks across all six candidates

**The retained positive dips survive fitting a separate baseline for each event. No candidate changes disposition.** This retrospective check addresses a specific failure mode: combining all in-transit samples against one pooled baseline can be biased when different events have different flux offsets or sampling. Here, the positive primary measurements change by at most 13 ppm. The unresolved timing and source problems remain.

| TIC | Existing data checked | Event-matched depth ± formal error (ppm) | Depth after deleting each event in turn (ppm) |
|---|---|---:|---:|
| 80387959 | Sector 90; 5 events | 608 ± 99 | 546–662 |
| 80387959 | Sector 100; 3 events | 650 ± 114 | 557–766 |
| 402358350 | Sector 81; 2 events; expanded primary clock | 635 ± 72 | 557–719 |
| 241928959 | Sector 92; 5 selected discovery events | 11,992 ± 786 | 11,729–12,442 |
| 469309982 | Sector 64; 9 events; original nominal clock | 76 ± 26 | 60–90 |
| 96166003 | Sector 59; 21 events; expanded primary clock | 263 ± 52 | 244–285 |
| 5546257 | Sector 62; 11 events | 387 ± 30 | 377–401 |

Positive omission estimates are a robustness observation, not independent detections or preserved significance. In the two-event case, each omission leaves just one event. For 241928959 these are the discovery-selected observations, not a new recurrence test.

## Complete comparisons and limitations

The [frozen plan](plan.json) identifies every input and all 15 nominal measurements to retain. [Results](results.json) include all alternative clocks from the selected reports, individual event measurements, precision shares, conditional heterogeneity statistics and every omission. No period-profile maximum was selected.

For 96166003 the other three timing hypotheses remain negative (event-matched depths −168, −70 and −149 ppm). The primary's robust positive depth therefore does not select the correct clock. For 469309982 the sector-63 comparison chosen after inspecting sector 64 remains weak, 82 ± 28 ppm, and falls to 21 ppm when one event is removed; its original-clock alternative is 13 ± 28 ppm, with omissions spanning −19 to +49 ppm. Both unfavorable results are retained. The four sector-81 hypotheses for 402358350 remain positive but timing-inconclusive.

For each complete event, the archived depth is its weighted outside-minus-inside mean. An inverse-variance mean of these depths equals a common-depth model with separate event intercepts. This comparison uses the existing phase masks and requires the original minimum of two inside and five outside samples per event. It does not introduce a slope, change detrending, or recover events lacking a baseline. The pooled estimate can include samples from incomplete events, so changes can reflect both baseline weighting and event eligibility.

Formal uncertainties assume independent errors. Correlated stellar/instrumental noise, timing uncertainty, and source blending are not removed by separate intercepts. Deleting an event is a sensitivity check, not a new holdout or a false-alarm calibration. No planet probability follows, and none of the previously failed timing gates is overridden.

## Verification

[verify.py](verify.py) checks input hashes and exact archived event records, independently solves each weighted least-squares mean and every omission, and checks a deterministic synthetic example with unequal sampling and different event baselines. The synthetic example demonstrates the possible pooling bias and recovery of the injected depth by separate intercepts; it is not an astrophysical injection/recovery experiment. [Verification](verification.json) passes for all 15 measurements.

No raw observations, shared scientific algorithms, original measurements or historical reports were changed. The verification starts from previously verified saved event summaries; it does not independently repeat their raw-flux reductions.
