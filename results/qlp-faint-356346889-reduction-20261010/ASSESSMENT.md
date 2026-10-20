# TIC 356346889: no qualifying SPOC recovery

Original training epochs were measured at the unchanged native QLP ephemeris.
QLP uses ten-minute bins, SPOC native samples. These reductions share the same
images; their coverage differs.

| Reduction | Sector | Depth ± formal error (ppm) | Formal SNR |
|---|---|---:|---:|
| qlp | 78 | 2129 ± 553 | 3.85 |
| qlp | 79 | 1158 ± 345 | 3.36 |
| qlp | 80 | 1934 ± 317 | 6.10 |
| qlp | 81 | 1695 ± 533 | 3.18 |
| qlp | combined_available | 1695 ± 199 | 8.52 |
| spoc | 78 | No usable measurement | — |
| spoc | 79 | No usable measurement | — |
| spoc | 80 | -344 ± 408 | -0.84 |
| spoc | 81 | No usable measurement | — |
| spoc | combined_available | -344 ± 408 | -0.84 |

SPOC Sector 80 is negative at the fixed event times; other sectors have inadequate
fixed-event coverage. Missing measurements are not zero depths. A
[matched-exposure attempt](../qlp-faint-356346889-matched-s80-20261010/coverage.json)
found zero pairs within the predeclared five-second tolerance (minimum nearest
offset 19.25 seconds). Its original empty-array error is preserved. No common
sample depth comparison was produced, and the tolerance was not widened.
This leaves coverage as a possible contributor to the reduction discrepancy.

The diagnostic lead remains unpromoted. [Plan](plan.json), [results](results.json),
[script](run.py).
