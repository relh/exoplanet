# TIC 233096878: mixed or weak separate-reduction evidence

The frozen native QLP ephemeris was applied unchanged to the original discovery
sectors. QLP uses ten-minute bins, SPOC native samples; coverage differs. These
reductions share TESS images and are not independent observations.

| Reduction | Sector | Depth ± formal error (ppm) | Formal SNR |
|---|---|---:|---:|
| qlp | 78 | 1936 ± 798 | 2.43 |
| qlp | 79 | 4155 ± 538 | 7.72 |
| qlp | 80 | 4622 ± 789 | 5.86 |
| qlp | 81 | No usable event measurement | — |
| qlp | combined_available | 3702 ± 387 | 9.56 |
| spoc | 78 | -890 ± 603 | -1.48 |
| spoc | 79 | 860 ± 449 | 1.92 |
| spoc | 80 | No usable event measurement | — |
| spoc | 81 | No usable event measurement | — |
| spoc | combined_available | 261 ± 360 | 0.72 |

Missing event coverage is not a zero depth or exclusion. SPOC does not provide a qualifying recovery: Sector 78 is negative and Sector 79 weak.
No matched-exposure comparison or source attribution is established here.
The original reserved timing failures remain. Keep this lead unpromoted.

[Plan](plan.json), [measurements](results.json), [script](run.py).
