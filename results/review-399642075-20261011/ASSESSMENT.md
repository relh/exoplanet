# TIC 399642075: nearby eclipsing-variable period match

The discovery search in sectors 37–38 finds 206 ppm dips at 2.28866665 days (formal SNR 15.25; 17 of 19 measured events supported). The alternative detrending window gives 202 ppm. These pass the current screening gates, but source attribution is unresolved.

The successful 60-arcsecond VSX query returns Gaia DR3 5231593599046170112, classified E, with period 2.2882 days. Its rounded catalog coordinates are 23.72 arcseconds from this target. The period difference is 0.00046665 days, or 0.0204%. This is a strong eclipsing-neighbor contamination warning, so deprioritize the signal as a new-planet lead pending pixel/source checks. We have not identified the target itself as this eclipsing variable.

The neighbor has listed G magnitudes 17.59–17.71, whereas the target has T magnitude 8.63. Different bandpasses, uncertain eclipse sampling and aperture throughput prevent a quantitative dilution explanation from these numbers alone; the neighbor has not been demonstrated to supply the measured 206 ppm signal. The catalog also lists two nearby pulsator candidates. A matching period alone does not establish the physical source.

The raw query, rows, URL and SHA-256 are retained in results.json. verify.py reproduces separation and period arithmetic and checks the raw catalog hash. The discovery plot was inspected. Sector 65 remains reserved and unopened at this review. No independent recurrence or new planet is claimed.

Subsequent pixel/PRF analysis strengthens an off-target source interpretation; see ../prf-399642075-20261011/ASSESSMENT.md. This supersedes the initial on-target size interpretation.
