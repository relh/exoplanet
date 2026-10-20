# TIC 383941028: off-target signal, not promoted

The native Sector 100 fit has period 1.516252788 days, duration 0.072 days,
and depth 8215 ± 850 ppm (formal SNR 9.67), with four supported events.
The discovery plot shows a localized dip, but it does not identify its host.
Reserved Sectors 12/13 were uncached at freezing and measure 231 ± 645 and
−862 ± 777 ppm. Propagated timing spreads of 7.47/7.38 days make these checks
inconclusive, not transit exclusions. The selected secondary dip is SNR 2.46,
weaker than the selected brightening magnitude 3.01; controls are uncalibrated.

Sector 100 difference imaging has a compact positive feature 1.766 pixels
from the catalog target, with 17 contributing pixel windows and formal peak
SNR 32.57. The image was inspected; other negative residuals are present.
The nearest catalog sources to its moment are TIC 1104265824 (T=18.60,
0.213 pixels) and TIC 383941039 (T=15.67, 0.328 pixels). This raises a strong
contamination concern, but a single uncalibrated moment cannot uniquely
identify the variable source. The 307-source cone and raw pixel provenance
are archived. Catalog positions were not proper-motion propagated.

Neither selected neighbor has an exact-name QLP/TESS-SPOC/SPOC observation
in the archived availability query. Gaia cross-release mapping and source
queries completed for both; neither has classifier or eclipsing-binary rows.
These absences do not exclude variability. No planet or novelty claim is made;
source-resolved photometry is still needed for exact attribution.

Evidence: [pixels](../../tesscut-383941028-s100-20261010/analysis.json),
[Gaia queries](../../gaia-383941028-neighbors-20261010/results.json),
[neighbor availability](../../qlp-faint-383941028-localized-neighbor-coverage-20261010/results.json),
and the frozen/held-out/secondary artifacts in this directory.

## Sector 101 source check

A subsequently opened Sector 101 cutout, using the unchanged Sector 100
fit, repeats a compact positive off-target feature. Sixteen pixel windows
contribute, formal peak SNR 12.83, target offset 1.411 pixels. Its moment is
0.080 pixels from TIC 383941039, versus 0.454 pixels from TIC 1104265824.
The image was inspected: a compact positive feature is present amid negative
background/residual structure, so its formal errors are not a calibrated
astrometric confidence. The two sectors favor nearby contamination, with
TIC 383941039 a plausible source; moment shifts and crowding prevent a unique
host claim. This is a post-selection localization check, not a preregistered
planet validation. Sector 101 is now opened and cannot later be called blind.

[Sector 101 evidence](../../tesscut-383941028-s101-20261010/analysis.json)
includes source hash, checksum verification and the unchanged fit hash.
