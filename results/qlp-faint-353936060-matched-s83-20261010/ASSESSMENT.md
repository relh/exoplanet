# TIC 353936060: compatible, noisy matched-exposure depths

This post-hoc check retains the previously frozen ephemeris and uses only
already opened Sector 83. Native samples were uniquely paired within a
predeclared five-second tolerance: 5074 pairs, with offsets 0.0037–4.9999 seconds.
The tolerance limits coverage; this is not a complete alignment of all samples.

For 94 common in-event samples, the fixed-window measurements are:

| Reduction | Depth ± formal error (ppm) | Formal SNR |
|---|---:|---:|
| QLP | 2081 ± 1177 | 1.77 |
| SPOC PDCSAP | 2115 ± 1020 | 2.07 |
| SPOC raw SAP | 2291 ± 968 | 2.37 |

QLP's unmatched subset retains 93 in-event samples, measuring 1975 ± 378 ppm
(SNR 5.22). Full QLP has two measured events; full SPOC has one. Full SPOC PDC
and SAP measure 1496 ± 381 and 1463 ± 361 ppm. Although full and common SPOC
have the same number of in-event points, matching changes the out-of-event
baseline samples and their uncertainty; their aggregate depths need not agree
exactly. The original detrending is retained before selecting common samples.

Compatible depths provide limited same-image processing support, not independent
validation or attribution. The noisier common subset cannot establish a clean
transit. All original diagnostic flags and inconclusive reserved timing remain.

[Plan](plan.json), [complete measurements](results.json), [script](run.py).
