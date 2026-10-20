# TIC 219846123: weak separate-reduction evidence

The frozen native QLP ephemeris is unchanged. QLP uses ten-minute bins and
SPOC native samples; their coverage differs and both reductions share images.

| Reduction | Sector | Depth ± formal error (ppm) | Formal SNR |
|---|---|---:|---:|
| qlp | 83 | 1350 ± 1404 | 0.96 |
| qlp | 84 | 7967 ± 1510 | 5.28 |
| qlp | 85 | 2956 ± 1123 | 2.63 |
| qlp | 86 | 6899 ± 1909 | 3.61 |
| qlp | combined_available | 4774 ± 697 | 6.85 |
| spoc | 83 | 2558 ± 1163 | 2.20 |
| spoc | 84 | No usable event measurement | — |
| spoc | 85 | No usable event measurement | — |
| spoc | 86 | HTTP 404: product unavailable | — |
| spoc | combined_available | 2558 ± 1163 | 2.20 |

There is no qualifying SPOC recovery. Sector 83's positive measurement is weak;
other epochs lack usable fixed-event coverage or the product is unavailable.
This neither establishes independent recurrence nor a decisive exclusion.
Missing data are not zero depths. Keep the original flags and do not promote.

[Plan](plan.json), [results and failures](results.json), [script](run.py).
