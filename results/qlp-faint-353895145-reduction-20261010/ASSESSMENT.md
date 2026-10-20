# TIC 353895145: weak SPOC support with limited coverage

The frozen native QLP ephemeris was applied unchanged to discovery sectors.
QLP uses ten-minute bins, SPOC native samples. Both reductions share the same
images, and differing exposure coverage remains unresolved.

| Reduction | Sector | Depth ± formal error (ppm) | Formal SNR |
|---|---|---:|---:|
| qlp | 83 | 5931 ± 966 | 6.14 |
| qlp | 84 | 4104 ± 1175 | 3.49 |
| qlp | 85 | 3957 ± 2400 | 1.65 |
| qlp | 86 | 6081 ± 3698 | 1.64 |
| qlp | combined_available | 5266 ± 698 | 7.54 |
| spoc | 83 | 1763 ± 860 | 2.05 |
| spoc | 84 | No usable event measurement | — |
| spoc | 85 | No usable event measurement | — |
| spoc | 86 | HTTP 404: product unavailable | — |
| spoc | combined_available | 1763 ± 860 | 2.05 |

SPOC gives no qualifying recovery. Its only fixed measurement is weak and
shallower than QLP, but differing coverage prevents interpreting this as a
matched-sample discrepancy or exclusion. Missing measurements are not zero
depths. Original detrending and timing failures remain. No promotion.

[Plan](plan.json), [results and failures](results.json), [script](run.py).
