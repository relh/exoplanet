# TIC 160438697: mixed or weak separate-reduction evidence

The frozen native QLP ephemeris was applied unchanged to the original discovery
sectors. QLP uses ten-minute bins, SPOC native samples; coverage differs. These
reductions share TESS images and are not independent observations.

| Reduction | Sector | Depth ± formal error (ppm) | Formal SNR |
|---|---|---:|---:|
| qlp | 73 | No usable event measurement | — |
| qlp | 74 | No usable event measurement | — |
| qlp | 75 | 3476 ± 753 | 4.62 |
| qlp | 76 | 4171 ± 635 | 6.57 |
| qlp | combined_available | 3760 ± 477 | 7.88 |
| spoc | 73 | -1281 ± 743 | -1.72 |
| spoc | 74 | No usable event measurement | — |
| spoc | 75 | No usable event measurement | — |
| spoc | 76 | 3410 ± 927 | 3.68 |
| spoc | combined_available | 432 ± 571 | 0.76 |

Missing event coverage is not a zero depth or exclusion. SPOC Sector 76 gives weak positive evidence, while Sector 73 is negative.
No matched-exposure comparison or source attribution is established here.
The original reserved timing failures remain. Keep this lead unpromoted.

[Plan](plan.json), [measurements](results.json), [script](run.py).
