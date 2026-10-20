# TIC 220440079: known eclipsing-binary contamination

Native Sector 99 fit: period 2.979187935 days, duration 0.133056 days,
fixed-measurement depth 4536 ± 394 ppm, formal SNR 11.51, five supported
events. The discovery plot was inspected and shows a localized depression
with adjacent positive structure. It does not establish a planetary origin.

Sectors 9/10 were uncached when the ephemeris was frozen. Their fixed-phase
measurements are 1411 ± 478 and 992 ± 679 ppm. Propagated timing spreads
2.91/2.88 days vastly exceed the fitted duration, so neither is a precise
prediction test or a transit exclusion. The exploratory secondary dip has
selected SNR 2.17, not a calibrated detection significance.

Pixel localization and Gaia identity now strongly support contamination from
known eclipsing binary TIC 220439648. This is not a new planet candidate.
All frozen, held-out, secondary, and discovery artifacts remain preserved.

## Source checks

Sector 99 difference imaging gives a compact positive feature 2.003 pixels
from the target, only 0.108 pixels from TIC 220439648. Six pixel windows
contribute, formal peak SNR 40.28. The image was inspected. Moments and formal
pixel errors are not calibrated PRF confidence, and catalog positions were
not proper-motion propagated. The complete cone contains 671 sources.

Gaia cross-release mapping identifies TIC 220439648 as DR3
5365226249425653120. Its variability tables contain an eclipsing-binary model
with period 2.980808539 days and primary/secondary depths 0.0960/0.0107 mag.
The spatial coincidence and closely matching period strongly support known
binary contamination. No Gaia-to-TESS epoch/phase conversion was attempted.

Exact-name photometry queries found no QLP/SPOC product for this binary or
faint neighbor TIC 864816940. Brighter nearby TIC 220446768 has six QLP sectors;
its extraction at the unchanged target ephemeris measures 6760 ± 286 ppm in
Sector 99 and 915 ± 386 ppm in Sector 36. This is also blended photometry:
the difference-image moment is 0.538 pixels from that brighter neighbor,
further than from the Gaia binary. These measurements do not establish the
brighter star as host. Historical fixed-phase weakness is not an exclusion.

The requested same-epoch TESS-SPOC file returned HTTP 404; this is missing
data rather than a nondetection. The QLP binned reduction reproduces the dip
at 4485 ± 396 ppm using the frozen ephemeris.

Evidence: [pixels](../../tesscut-220440079-s99-20261010/analysis.json),
[Gaia period comparison](../../gaia-220440079-neighbors-20261010/period-comparison.json),
[neighbor photometry](../../neighbor-220446768-20261010/results.json),
[reduction check](../../qlp-faint-220440079-reduction-20261010/results.json).
Raw source URLs and hashes are preserved in the associated manifests.
