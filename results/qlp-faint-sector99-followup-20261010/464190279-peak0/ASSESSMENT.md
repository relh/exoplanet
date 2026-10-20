# TIC 464190279: off-target contamination, source unresolved

Not a likely new planet around the searched target. Sector 99 difference
imaging places the dip 2.448 pixels away, near the close pair TIC 861857428
and TIC 464190342. Their exact variable component and nature remain unresolved.

The native fit is P=1.256625948 days, duration 0.092736 days, depth
17636 ± 565 ppm, formal SNR 31.23, with 12 supported events. The discovery
plot was inspected. Reserved Sectors 9/10 were uncached at freezing but give
negative fixed-phase measurements (−10695 ± 992 / −10249 ± 956 ppm).
Timing spreads 1.049/1.038 days make these inconclusive, not exclusions.
Exploratory off-phase dip SNR 3.92 is selected and uncalibrated.

The inspected difference image shows a compact strong off-target feature:
17 pixel windows, formal peak SNR 243.76, distances 0.076/0.101 pixels to
TIC 861857428/464190342. Unpropagated catalog positions and uncalibrated
moments cannot resolve this close pair. The 643-source cone is preserved.

Both neighbor extractions show a 11824 ± 68 ppm dip at the unchanged target
ephemeris in Sector 99. However, ALL common light-curve columns in those
Sector 99 products are exactly identical despite different TICID headers.
They are the same photometric measurement, not independent confirmation.
In Sector 36 the extractions differ and give 2911 ± 96 ppm for 464190342 and
24870 ± 614 ppm for 861857428. Their overlapping apertures and historical
timing uncertainty still prevent assigning a unique host or binary/planet
classification. No new phase fitting was performed.

Gaia cross-release mappings and source lookups completed for both; neither
has classifier or eclipsing-binary rows. Nine dated local planet/binary
catalog tables also had no exact-TIC matches in the cone. These nonmatches
do not establish novelty or exclude an unlisted binary. Target TESS-SPOC99
returned HTTP 404, not a nondetection. Binned QLP fixed depth is 17391 ± 563 ppm.

Evidence: [pixels](../../tesscut-464190279-s99-20261010/analysis.json),
[Gaia](../../gaia-464190279-neighbors-20261010/results.json),
[catalogs](../../qlp-faint-464190279-catalogs-20261010/results.json),
[extraction equality](../../neighbor-464190342-20261010/extraction-comparison.json),
[neighbor 464190342](../../neighbor-464190342-20261010/results.json),
[neighbor 861857428](../../neighbor-861857428-20261010/results.json),
[reduction](../../qlp-faint-464190279-reduction-20261010/results.json).
Resolved photometry would be needed to identify the exact variable component.

## Sector 90 repeat localization

The subsequently opened Sector 90 pixels use the unchanged Sector 99 fit.
An inspected compact positive feature again lies off-target, 2.620 pixels
from TIC 464190279. Twenty-one pixel windows contribute and formal peak SNR
is 239.36. The moment lies 0.147 pixels from TIC 464190342 and 0.195 pixels
from TIC 861857428. The two epochs strongly support contamination from the
same close pair, but the changing nearest component and uncalibrated moments
cannot resolve the pair. This post-selection source check is not a precise
blinded planet prediction. Sector 90 is now opened for this diagnostic.

[Sector 90 pixels and provenance](../../tesscut-464190279-s90-20261010/analysis.json).
