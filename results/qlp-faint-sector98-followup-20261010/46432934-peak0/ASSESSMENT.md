# TIC 46432934: contamination from a known neighboring planet

**Not a new planet candidate.** The strong 1.4404-day screening signal points
to neighboring TIC 46432937, host of the already confirmed TIC 46432937 b
(TOI 7716). The known neighbor is 39.77 arcseconds from the searched star.

The Sector 98 QLP search selected an approximately 3.38% dip at 1.440479 days,
with 18 supported events and only missing aperture-crowding information flagged.
Native refinement gives 1.440393 days, a 0.032-day box duration, and a fixed
depth of 3.969% with formal S/N 64.23. The discovery plot shows repeated deep
dips. A training-only secondary scan is weak (selected S/N 2.34), comparable
to the strongest brightening (absolute S/N 2.58).

The first reserved QLP sectors, 6 and 32, were not cached when the prediction
was frozen. Their fixed measurements are negative, but timing spreads of
0.124 and 0.090 days exceed the half-duration of 0.016 days. Both remain
timing-inconclusive; they must not be rewritten as precise failed predictions.
The same-epoch [reduction check](../../qlp-faint-46432934-reduction-20261010/results.json)
retains the QLP dip and a TESS-SPOC HTTP 404, which is not a nondetection.

The [Sector 98 pixel diagnostic](../../tesscut-46432934-s98-20261010/analysis.json)
has a compact positive difference image with formal peak S/N 167, based on
40 locally measurable events in the pixel data. Its moment lies 1.949 pixels
from the searched target and only 0.061 pixel from TIC 46432937. These pixel
events are not additional independent transit observations. Visual inspection
shows the difference concentrated on the neighbor. Moments and formal errors
are not calibrated PRF confidence bounds; catalog positions were not motion
propagated, and local temporal subtraction does not model every background term.

A complete 180-arcsecond TIC cone contains 102 sources. Nine dated catalog
tables identify TIC 46432937 as a known planet host with a matching period.
The [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/overview/TIC%2046432937)
lists the published period as 1.440445270 days. Catalog identity, period, and
pixel location together strongly support contamination from this known system.
A [fresh archive query](../../qlp-faint-46432934-known-neighbor-20261010/results.json)
places the selected epoch only 0.000974 day (1.40 minutes) from the published
ephemeris prediction. This is a post-selection identification comparison,
not a new independent prediction test or a calibrated timing-confidence claim.
The target's conditional planet-radius estimate is therefore not meaningful.
Original discovery, timing failures, catalog matches, and pixel evidence are
retained. This is a recovered known-neighbor signal, not our discovery.
