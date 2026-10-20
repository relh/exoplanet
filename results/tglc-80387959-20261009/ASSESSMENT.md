# Additional extraction and blend check

The [MAST TGLC product](https://archive.stsci.edu/hlsp/tglc) models neighboring stars
using Gaia positions and an effective point-spread function. Its sector 12–55
products are not all indexed by the observation API. We obtained indexed Sector 10
URLs for the target and neighbor 80387965, then used the documented filename
convention and SPOC detector metadata for 36/37. All six downloads succeeded;
FITS TIC/Gaia/sector identity, time reference and integrity were checked. No new
observing sector was opened.

The already-frozen ephemeris is used throughout. Require both quality flags zero,
finite positive flux, and compare raw/calibrated PSF/aperture with two flattening
windows. Files contain no per-cadence errors; adjacent-difference MAD and the
existing scatter floor are explicitly recorded. Formal S/N is conditional.

Calibrated PSF, 1.5-day window:

| Star | Sector 10 depth / S/N | Sector 36 depth / S/N | Sector 37 depth / S/N |
| --- | --- | --- | --- |
| Target 80387959 | 104ppm / 0.33 | 710ppm / 4.68 | 864ppm / 5.52 |
| Neighbor 80387965 | 183ppm / 0.04 | 10,724ppm / 3.59 | 10,897ppm / 4.59 |

Aperture extractions show the dip in both stars, including Sector 10; all 48
column/window measurements are retained. These are the same observations as
SPOC/QLP, not additional independent recoveries.

Outside the candidate event, the target/neighbor calibrated-PSF light curves have
Pearson correlations 0.875/0.717/0.837 in 10/36/37. Their relative-amplitude slopes
are 11.1/14.4/12.7. The eclipse relative-depth ratios in 36/37 are 15.1/12.6. Thus
shared extraction structure can explain why both light curves carry a similar
signal in different fractional units. Correlation does not prove which source
varies; no regression subtraction was used to force a host assignment.

Conclusion: TGLC supports the recurring dip but does not uniquely identify its
host. Do not count the neighbor signal as an independently resolved eclipse,
or claim that the target's PSF extraction has ruled out contamination. A fit
using independently calibrated detector-response models is the next available
pixel-level test; it also needs injection and model-mismatch checks.
