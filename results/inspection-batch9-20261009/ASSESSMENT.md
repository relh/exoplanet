# TIC 399450592: repeating signal, source unresolved

This is a higher-priority unresolved lead, **not yet a likely planet**. The
parent batch-nine search remains active. This directory preserves the completed
target's discovery evidence independently of that evolving batch.

## Photometric evidence

- Original Sectors 24/25: P=1.7422009 days, depth 649 ppm, formal S/N 10.73.
  Alternative detrending gives 640 ppm at nearly the same period. Odd/even
  mismatch is 0.98 sigma. QLP gives 602 ppm (S/N 6.36) in Sector 24 and 389 ppm
  (S/N 2.70) in Sector 25.
- Sectors 18 and 52 were explicitly added to training before freezing the first
  later-sector prediction. The combined training fit has P=1.7428541 days and
  30 supported events. Sector 58 was then opened at the immutable prediction:
  depth 514 ppm, S/N 7.98, timing spread 0.03253 days, with formal expected
  S/N 9.58. It passes the existing recovery criterion. This establishes repeated
  photometric structure, not its source or planetary nature.
- Zero of 48 block controls exceeded the discovery maximum. This is a limited
  correlation diagnostic, not a survey false-alarm probability.
- Median-normalized SAP and PDCSAP folds were inspected without running-median
  detrending. The dip remains visible in Sectors 24 and 58; Sector 25 SAP has
  stronger baseline structure. All inspected observations were already open.

## Unresolved localization

Sector 24 and 25 difference moments lie 0.75 and 1.24 pixels from the header
target, toward the faint neighbor TIC 399450579 (Tmag 16.47). The Sector 24
moment is about 1.68 arcsec from that neighbor. But Sector 58 instead shifts
westward, 0.71 pixels from the target, and does **not** reproduce the same sky
position. Images include negative residuals and do not provide calibrated
astrometric uncertainties. Neither on-target origin nor a unique contaminant
is established. An on-target pixel-injection/PRF localization check is needed.

Gaia DR3 variability-classifier and eclipsing-binary queries return no rows for
the target or TIC 399450579's Gaia source. That does not exclude an eclipsing
neighbor. The exact-TIC web search also returned no result; no novelty claim
follows. Full alias/positional catalog and literature vetting remains necessary
if the localization survives.

## Conditional physical fits

The new `physical_fit` module uses an exposure-integrated circular transit model
from [batman](https://lkreidberg.github.io/batman/docs/html/tutorial.html), profiling
local linear baselines. Six post-recovery fits use already-opened Sectors
18/24/25/52/58: three fixed quadratic limb-darkening choices, with/without a
Gaussian log-scaled-axis constraint derived from TIC mass/radius errors.

Under the stellar constraint and an undiluted on-target interpretation, the
fits imply 1.83–1.90 Earth radii and roughly 1.9-hour durations. This range is
model sensitivity, **not a confidence interval or radius measurement**. Free
geometry is degenerate; the weak-limb-darkening unconstrained fit hits the
minimum scaled-axis boundary and yields a different radius. Eccentricity,
dilution, uncertain stellar properties and image contamination remain unresolved.
These fits were made after recovery and are not a new blind prediction.

The fitting code and dependencies are snapshotted in `physical-399450592-20261009`.
All 30 tests pass, including synthetic parameter recovery with finite exposures
and local trends. `setuptools` supplies the legacy `distutils` import required
by the installed batman package under Python 3.12; the initial import failure
was resolved before the successful test run.

Sector 78 remains unopened. Do not promote or submit this signal before resolving
the image-source ambiguity and completing the remaining validation.


## Empirical pixel-injection comparison (2026-10-09)

Contamination is now favored. Fixed target-centered positive-flux moments were
measured identically for observed events and 39 shifted-phase injections per
sector. Original event cadences were excluded from controls. An empirical image
template was injected at the target and separately translated to TIC 399450579.
The latter assumes a common local PSF; neither supplies calibrated source
probabilities or astrometric confidence regions.

Offsets from target-control medians are 0.690, 0.678 and 0.675 pixels in Sectors
24/25/58; 0/39, 0/39 and 1/39 controls have larger radial offsets. Against neighbor
controls they are 0.188, 0.107 and 0.716 pixels, with 23/39, 32/39 and 1/39 larger.
The neighbor hypothesis matches both discovery sectors much better; Sector 58
is poorly matched by either. These conditional counts are not false-alarm
probabilities. The comparison figure and hashed summary are alongside this
assessment; full images and code snapshots are in pixel-controls and
pixel-neighbor-controls directories.

Downgraded to unresolved likely contamination. A specific eclipsing neighbor is
not confirmed. Sector 78 remains unopened. Deterministic target/displaced-source
tests pass; full suite: 31 tests.


## Resolved ground-based counterpart

ZTF now strongly supports an eclipsing contaminant at TIC 399450579. Separate
neighbor photometry dims at the original frozen TESS period/phase in g/r/i,
with ~0.107/0.112/0.073-mag fixed-window depths. Its astrometry matches the
neighbor within 0.08 arcsec. Approximate two-star dilution yields 367–556 ppm,
comparable to TESS, subject to bandpass/aperture assumptions. Combined with
24/25 image offsets, this is strong positive contamination evidence. The target
ZTF nondetection cannot rule out a shallow target transit by itself. No likely
planet around TIC 399450592 is established. See the hashed ZTF analysis and
figure in ../ztf-399450592-neighborhood-20261009. Sector 78 remains unopened.
