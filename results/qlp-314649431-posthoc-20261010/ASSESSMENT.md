# TIC 314649431: off-target eclipsing source resolved by ZTF

Rejected as a planet around TIC314649431. A post-hoc refinement of all four already
opened QLP epochs15/56/82/83 gives P1.14381435d and~754ppm fitted depth. That fit
is not independent validation; the original timing-inconclusive15/56 tests remain.
No selected QLP reserve remains. Measurements at the refined ephemeris are positive
in all four sectors, but this does not determine the host.

Requested TESS-SPOC pixel products82/56 returned404; both errors are retained.
A public11x11 TESScut sector56 stamp yields23events with off-target flux loss,
peak formal pixel SNR64.3 and moment offset3.00pixels. Raw FFI background beyond
the local temporal baseline was not modeled. Moments are not calibrated PRF
astrometry, and this uses the same TESS observations as QLP.

Independent ZTF photometry at the already-fixed TESS ephemeris identifies neighbor
TIC314649408, 64.5arcsec from the target: r-band OID689213300034147 has
0.4055 ±0.0045mag eclipse depth across30distinct events; g-band OID689113300024376
has0.4239 ±0.0155mag across30events. Two additional object series support the dip.
No ZTF period/phase optimization was performed. Nearest-TIC matches are within
0.33arcsec; proper motions were not propagated. Formal errors omit red noise.
The ground-resolved deep eclipses plus off-target TESS flux loss strongly support
contamination, not a planet around the target. No companion masses are claimed.

See ../tesscut-314649431-s56-20261010/analysis.json and difference.png, and
../ztf-314649431-contaminants-20261010/analysis.json and fixed-phase.png.
Dated TOI/confirmed/CTOI/EB, Villanova/Kostov2025/DTARPS exact-TIC checks across471
neighbors found no match, which does not establish novelty or exclude aliases.
URL/SHA provenance, scripts and original negative evidence are retained.
