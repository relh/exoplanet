# Recovery varies substantially across the solar-radius pilot

All36 additional injections completed without errors. The three stars were
chosen before injection at ranks1,8,15 of the16 pilot targets sorted by baseline
best-peak SNR. This tests deliberately contrasting light curves, not a random
sample. The prior lowest-scatter control selected rank16 separately.

| TIC | Baseline best-peak SNR | Injected period recovered in screened top3 | Passed all gates, excluding baseline matches |
|---|---:|---:|---:|
|365441779|5.89|12/12|8/12|
|321684341|9.15|11/12|7/12|
|149176305|110.87|2/12|0/12|

The shared grid uses periods1.37,4.73,13.13days, durations0.04/0.12days and
250/750ppm depths, one phase each, integrated over the median exposure and
inserted before detrending. These are box-signal controls, not Earth-radius
completeness or astrophysical false-positive calibration. Synthetic successes
are not new candidates.

The two weaker-baseline stars yield15 full-screen recoveries across24 probes,
whereas the strongly variable star yields none. This contrast shows why the
previous one-star zero-recovery result cannot characterize the entire pool.
Failures remain informative: some recovered periods fail event-consistency,
secondary-coverage or alternative-detrending gates. A larger injected depth need
not pass every gate. No threshold was loosened to improve these outcomes.

`verify.py` reconciles all36 trial records, matching-period accounting and source
hashes. Reserved light curves remain absent. The unchanged campaign and injection
routines are used; no scientific algorithm was modified. Each trial retains its
full flags, baseline-match accounting and raw-data provenance.

A further discovery batch is justified as an exploratory search, with these
sensitivity limitations explicit. It cannot be interpreted as an Earth-size
occurrence survey or as excluding planets in the rejected stars. Full-screen
candidates still require independent-epoch and source/catalog checks.
