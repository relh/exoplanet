# TIC 32495864 Sector 97 pixel diagnostic

The raw four-event difference image is dominated by positive field-wide
background (roughly 26–29 flux units). Its formal maximum SNR 313.8, emitted
4.35-pixel moment offset and nearest-source list are **not interpretable as
source attribution**. The image was inspected; the failed check is retained.

An explicitly post-selection spatial-plane sensitivity check excludes the
target and catalog stars brighter than T=17 at radii of two and three pixels.
It uses 77 and 37 background pixels, respectively. Both residual images show
a compact positive excess at pixel (5,5), 0.36 pixel from the target coordinate.
The maximum excess is 2.58 and 2.53 flux units; background residual RMS is
0.119 and 0.110. Both images were inspected.

This supports a residual near the target under these background models, but
is not a calibrated PRF localization, independent epoch, or proof of an
astrophysical transit. Source-dependent instrumental response, blends,
background model errors and the ambiguous broad light-curve shape remain.
The apparent raw off-target moment must not be used to claim contamination.

## Cadence-by-cadence aperture check

A separate same-photon extraction fits a spatial plane to 37 background pixels
at every cadence, using the fixed three-pixel source exclusion mask. At the
unchanged 13.815568663-day timing, aperture radii 1.5 and 2 pixels give depths
681 ± 349 ppm (SNR 1.95, one supported event) and 1,284 ± 433 ppm (SNR 2.96,
two supported events). The four event plots were inspected and show smooth
structure without a robust repeated sharp dip. No ephemeris was refitted.

This weakens the QLP SNR 8.29 signal and shows extraction dependence, but is
not a transit exclusion: the simple background model, different apertures,
lack of detrending and correlated systematics limit comparison. Formal
errors propagate published independent pixel errors only. The prior compact
spatial residual is retained but is insufficient to establish a planet.
A separate least-squares/direct-sum calculation verifies the numerical linear
extraction to floating-point precision. See aperture.json, aperture.png and
aperture-verification.json for provenance and measurements.
