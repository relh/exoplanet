# TIC 459258444: known eclipsing-binary contamination

This is not a new planet candidate around the searched target. The Sector 100
signal is strongly attributable to neighboring known eclipsing binary
TIC 459258383 (Gaia DR3 5353479651327362944).

The frozen native fit has period 2.917941695 days, duration 0.144 days, and
fixed-measurement depth 10084 ± 672 ppm, formal SNR 15.00, with five supported
events. Reserved Sectors 10/36 were uncached at freezing: 518 ± 1232 and
9454 ± 916 ppm. The latter is positive, but 4.63/3.33-day propagated timing
spreads make both prediction tests inconclusive. It is not a precise blinded
recurrence. Exploratory secondary SNR 2.80 is not independently calibrated.

Sector 100 difference imaging is compact and positive, 3.035 pixels from
the target and 0.109 pixels from TIC 459258383. Nine pixel windows contribute;
formal peak SNR is 186.13. The plot was inspected. A fainter source
TIC 936349859 is also nearby (0.224 pixels from the moment), so the centroid
alone does not prove exact attribution. Moments are not calibrated PRF
uncertainties and catalog positions were not proper-motion propagated.

A complete Gaia DR2-to-DR3 mapping identifies TIC 459258383 in both the
classifier (ECL) and eclipsing-binary table. Its catalog period is 2.915830937
days, within the discovery fit's profile range; model primary/secondary depths
are 0.188/0.028 mag. No Gaia-to-TESS epoch conversion was attempted.

The neighbor's separate QLP extraction at the unchanged target ephemeris
shows a 11.602 ± 0.086% primary dip and 0.968 ± 0.093% half-phase dip in
Sector 100. This uses the same image epoch, not independent photons, but
strongly supports the catalog binary as the contaminant. Sector 36 gives
1.649 ± 0.122% at primary and 4.776 ± 0.130% at half-phase; accumulated period
uncertainty makes those labels unreliable as physical primary/secondary
identifications. Both measurements, including that limitation, are retained.

Evidence: [pixel localization](../../tesscut-459258444-s100-20261010/analysis.json),
[Gaia period comparison](../../gaia-459258444-neighbors-20261010/period-comparison.json),
[neighbor photometry](../../neighbor-459258383-20261010/results.json), and
this directory's frozen, held-out and secondary artifacts. Raw sources and
hashes are preserved in their manifests. No new planet or binary discovery.
