# TIC 320504102: separate-reduction check is coverage-limited

The already frozen native QLP ephemeris was applied unchanged to discovery
Sectors 83–86. No additional reserved epoch or fitted phase was introduced.

| Sector | QLP depth ± formal error (ppm) | QLP SNR | TESS-SPOC result |
|---|---:|---:|---|
| 83 | 2,813 ± 688 | 4.09 | 1,362 ± 1,526 ppm; only six in-event points |
| 84 | 3,816 ± 545 | 7.00 | No usable fixed-event measurement |
| 85 | 1,139 ± 621 | 1.83 | No usable fixed-event measurement |
| 86 | 458 ± 826 | 0.55 | HTTP 404: product unavailable |

QLP here uses the original ten-minute discovery binning; SPOC uses its native
samples. Available SPOC data provide no qualifying recovery, but their poor
fixed-event coverage prevents a meaningful exclusion. Missing measurements
and unavailable products must not be interpreted as zero eclipse depth.
QLP's selected dip is substantially stronger in Sector 84 than in 85/86,
adding to concerns about the structured discovery residuals.

These reductions share the underlying TESS images, so they would not provide
independent observations even with good coverage. No host attribution or
planet confirmation is established. Keep the screening lead unpromoted and
retain the original timing-inconclusive reserved tests.

[Plan](plan.json), [all measurements and failures](results.json), [script](run.py).
