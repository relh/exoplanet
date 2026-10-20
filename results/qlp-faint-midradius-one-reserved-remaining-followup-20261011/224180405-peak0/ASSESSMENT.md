# TIC 224180405: initial review

Clear rounded central dip with positive shoulders and a large observing gap. The strong recurring signal still requires source attribution and a binary check.

Discovery plot visually reviewed. Refined period 1.102650071 days, depth 0.00823676, duration 0.092736 days, training sectors [81], supported events 15. Original flags retained: ['crowding_or_missing_crowding'].

Reserved sector 54: timing_prediction_inconclusive; timing spread 0.243940 days. This neither confirms nor excludes the signal. Source checks and catalog checks remain pending; no credible new planet or novelty claim.


## Initial source images

The raw sector81 stack and all22 usable individual event images were visually reviewed at the frozen clock. Every map shows a compact relative positive feature near pixel(6,3), well separated from the target near(5.2,5.5). Events9,10,22 also contain large field-wide offsets, but the displaced relative feature persists. The stack moment lies2.867pixels from the target and0.194pixels from TIC224180336 (T=13.5615). Several faint neighbors are close to that position, so a unique host is not established by a moment. The images strongly favor neighboring-source contamination over a planet around TIC224180405. Formal pixel SNR171 is not a host probability.

Raw events-1 through23 are available except6/7/8, each of which has40 inside samples fully flagged (2048/18432/2048 respectively). All22 retained events have40 quality-zero inside samples and at least80 local baseline samples. The22 raw image windows are not22 independent transit detections; clean QLP supports15 events. Original gates and clock are unchanged. Raw FITS SHA256:7fb1b3c2525f5e4a8b240a2c6a6d3e48c8c492e225006e600f8228bfaf1f9ca1.

The exact attempted processed SPOC pixel URL returns404; this does not exclude all other products. The TIC cone has1211 entries. These raw images use the same photons as QLP, and the reserved-sector timing test remains inconclusive. The exploratory secondary scan found a selected SNR3.40 dip near phase0.531 across61 trials; that uncalibrated statistic does not independently classify a binary. An exact-TIC web search returned no results and supplies no novelty evidence.


## Catalog context and disposition

All134 TIC entries within3pixels of the difference moment have Gaia DR2 identifiers.149 neighborhood mappings lead to133 unique DR3 sources, all returned by the source query. Both target and TIC224180336 have unique DR2-to-DR3 matches (4287465641716822528 and4287465706122297344). No queried DR3 source has a returned variability-classifier or eclipsing-binary row. The raw CSV and saved JSON agree; ambiguous mappings are retained. This catalog absence does not exclude a blended eclipse.

Initial source inspection is complete. Neighbor contamination is strongly favored; the unique variable host and physical cause remain unresolved. No credible new planet is claimed. Frozen clock, original flags, secondary-scan limitations and inconclusive reserved test remain intact.
