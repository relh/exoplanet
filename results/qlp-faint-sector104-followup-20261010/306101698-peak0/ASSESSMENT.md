# TIC 306101698: unresolved screening lead with contamination concern

**Not a likely new planet candidate.** The original Sector 104 QLP screen
selected a 2.875925-day dip with five supported events, formal S/N 9.14,
and only unmeasured aperture crowding flagged. Native refinement gives
2.870014 days, epoch BTJD 4180.736859, duration 0.1104 days, and a fixed
3,988 ± 381 ppm depth (formal S/N 10.48) with six supported events.
The discovery plot was inspected; its folded dip is visible but does not
establish a planetary shape or host. Exploratory off-phase dip/brightening
strengths are similar (S/N 2.62 versus absolute S/N 2.49).

Reserved QLP sectors 12 and 13 were uncached at the freeze. Fixed depths are
+37 ± 669 ppm and −2,014 ± 559 ppm. Timing spreads of 7.66 and 7.58 days
far exceed half the fitted duration; neither is a precise prediction test.
Their original timing-inconclusive conclusions remain unchanged.

The [same-epoch reduction check](../../qlp-faint-306101698-reduction-20261010/results.json)
retains a positive QLP measurement; the TESS-SPOC Sector 104 product returned
HTTP 404. Missing data do not establish an independent nondetection.

The [Sector 104 pixel difference](../../tesscut-306101698-s104-20261010/analysis.json)
is a compact positive feature (formal peak S/N 12.58; eight event windows)
whose moment lies 1.132 pixels from the target. Nearby faint sources
TIC 1511215710 and TIC 306101707 are 0.084 and 0.187 pixel from that moment,
respectively. This raises an off-target contamination concern, not a unique
host identification: moments/formal errors are uncalibrated, background
subtraction is limited, and catalog coordinates were not motion-propagated.
These are the same observations as the discovery, not independent recoveries.

A [chronological split](../../tesscut-306101698-s104-split-20261010/ASSESSMENT.md)
retains the offset in both four-event groups: 1.062 and 1.211 pixels, with
positive-feature formal S/N 13.19 and 7.22. This strengthens the within-sector
repeatability of the contamination concern, but uses the same selected
ephemeris and fixed image region and is not calibrated independent validation.
An exact-name archive query finds no QLP/TESS-SPOC/SPOC light curves for the
two closest source hypotheses. A [Gaia lookup](../../gaia-306101698-neighbors-20261010/ASSESSMENT.md)
using release-to-release identifier mappings finds no variability classification
or released epoch photometry for either. Neither absence excludes a contaminant.

An [additional Sector 103 pixel test](../../tesscut-306101698-s103-20261010/ASSESSMENT.md)
using the unchanged ephemeris failed: its entire difference image is negative
and dominated by broad background structure. Its numerical centroid and
nearest-source list are not a valid transit localization. It provides no
second-sector support for the suspected offset. Sector 103 is now opened.

The neighbor query initially failed, then succeeded in a separately preserved
retry, returning 718 sources in a 180-arcsecond cone. Nine dated catalog
tables have no exact TIC match in this cone. This does not prove novelty,
exclude uncataloged binaries, or identify the source. The screening lead remains
unpromoted pending repeatable timing and reliable source attribution; all
negative and failed checks are retained.
