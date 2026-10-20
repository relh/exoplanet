# TIC469309982: retrospective leave-season-out prediction

Three observing-season groups (sectors9/10,36/37,63/64) were omitted in turn at two predeclared detrending windows. All six sectors had already been inspected. This is a conditional retrospective robustness check, not independent holdout confirmation. The original discovery seed from9/10 fixes the local search neighborhood for every fold, including the fold that omits9/10. No blind rediscovery is claimed.

Only the 1.5-day-window prediction of sectors36/37 meets the existing strict timing and recovery conditions. The other five folds are timing-inconclusive. These results preserve evidence of repeated dimming but do not support a statement of three independently confirmed observing seasons or establish a planet.

| Detrending window (d) | Excluded sectors | Depth ± formal error (ppm) | Formal SNR | Supported events | Timing spread (d) | Outcome |
|---|---|---|---|---|---|---|
| 1.5 | 9,10 | 78.1 ± 21.6 | 3.61 | 1 | 0.1334 | Timing-inconclusive |
| 1.5 | 36,37 | 129.7 ± 22.6 | 5.74 | 4 | 0.0525 | Conditional recovery |
| 1.5 | 63,64 | 47.3 ± 19.1 | 2.47 | 3 | 0.1235 | Timing-inconclusive |
| 2.5 | 9,10 | 114.7 ± 23.8 | 4.82 | 3 | 0.1210 | Timing-inconclusive |
| 2.5 | 36,37 | 136.7 ± 23.5 | 5.81 | 5 | 1.5706 | Timing-inconclusive |
| 2.5 | 63,64 | 99.2 ± 19.2 | 5.16 | 4 | 0.1569 | Timing-inconclusive |

All fitted durations are0.144day, so the precision threshold is0.072day. Positive formal SNR alone does not override timing ambiguity. In the2.5-day omission36/37 fold, separated allowed period-profile solutions expand the propagated spread to1.5706days despite a strong nominal dip. The full saved profile is retained; no favorable branch was selected. The central season is an interpolation test; omitted earliest/latest seasons require extrapolation.

The plan, source hashes, original seed, two windows, all three folds and six raw product hashes/URLs were saved before analysis. Each fit uses only the four remaining sectors and is saved before evaluating excluded-sector flux. Preprocessing is performed separately per sector. No omitted-data period, phase or duration optimization is performed. An unchanged original seed-clock measurement is also saved for every fold as a reference, not an alternative chosen for significance.

The six-panel plot was visually inspected. It shows negative features near the train-only predictions, but their asymmetry and offsets, neighboring variations and timing uncertainty remain visible. Source attribution, the possible secondary and red-noise concerns are unchanged. No new data were downloaded.

Verification reconstructs all six raw/preprocessed data pairs and training fits, independently recalculates eighteen fixed-clock total/event measurement sets (training, excluded and original-seed reference), and checks timing propagation, rules, hashes, disjoint groups and freeze-before-score chronology. Training refits reuse Astropy BLS and the existing refinement implementation, so this is arithmetic/provenance verification, not an independent physical model.

Formal errors and profile thresholds are conditional on the box model and do not include all red noise or model mismatch. Folds overlap, the two reductions share photons, the seed and analysis selection were informed by previously viewed data, and none of the six outcomes is an independent planet probability. The previously recorded nominal sector64 and subsequent sector63 tests are retained and not reclassified by this retrospective analysis.

Files: `plan.json`, `results.json`, six `*-training.json` records and six cached processed arrays, `run.py`, `verify.py`, `verification.json`, `plot.py`, `folds.png`.
