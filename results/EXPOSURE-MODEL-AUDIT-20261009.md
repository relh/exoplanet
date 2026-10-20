# Exposure-aware event diagnostics, 2026-10-09

**No likely new planet candidate is established.** This update investigates a
specific failure exposed by real-data injections, then revisits relevant old
screening decisions without overwriting the original searches.

## Why revisit event depths?

For TIC 351654581, a known injected 1.37-day, 0.12-day-duration, 750-ppm transit
was recovered at formal S/N 91 yet flagged for odd/even and event inconsistency.
At the coarse discovery ephemeris, odd/even disagreement was 5.83 sigma and
conditional event-consistency p was 0.0000545. Measuring at the known injected
period/duration reduced these to 2.36 sigma and p=0.466. The true timing was used
only to diagnose the software, never to fit real candidates.

A finer instantaneous box fit reduced the odd/even issue but did not fix the
consistency issue. This justified testing a model that accounts for finite
exposure and fits duration continuously. It does not justify simply relaxing
thresholds until injections pass.

## Diagnostic model and validation

`transit_model.py` computes exact overlap of a box transit with each inferred
exposure (median cadence within a contiguous segment). It refines period, epoch
and duration locally around a discovery peak. A separate linear baseline is
profiled out for each fixed event window. Event amplitudes are then measured
using the same fitted shape; odd and even events share the timing solution.
Both event and odd/even errors use the already-measured duration-binned beta.

This changes several things together—exposure integration, timing/duration
refinement, local baselines and odd/even error inflation. The improvement cannot
be attributed uniquely to one component. It remains a box approximation with
conditional formal errors, not a limb-darkened physical fit or a calibrated
false-positive statistic. Boundary fits and failed optimizations are flagged.
Tiny windows truncated by gaps are excluded from fitting; the first audit failed
on one such window, and its original source/results are retained as `failed`.

Of the **55 previously recovered injected periods**, the revised pair of checks
would retain **36**, versus 33 before, while preserving all 33 original passes.
Other screening flags were unchanged. This is **36/96** total injection probes,
not a new period search or survey completeness. One strong uniform injection
still has odd/even disagreement around 3.29 sigma, demonstrating unresolved
underlying-data/noise limitations. The initial audit, corrected audit and
known-truth experiment are separately preserved.

Synthetic tests verify finite-cadence depth/period recovery, retain strong
odd/even differences for genuinely alternating eclipses, and handle a window
truncated to one point. Both known-planet controls, L98-59 c and GJ 357 b, still
pass. **24 tests pass.** This limited validation does not establish reliable
classification for every eclipsing system or correlated-noise pattern.

## Rescreening completed discovery batches

Immutable companion results in `model-rescreen-batch1-20261009/` and
`model-rescreen-batch2-20261009/` inspect original passes and near-passes whose
flags can be affected by these diagnostics. No new period search was run and
no validation data were opened by this step. All original source hashes and
flags remain available. Existing rejected/blended signals remain rejected on
their independent evidence, even if their event-shape checks pass.

The only additional review priority was **TIC 317594826**:

- Original period 17.29215 days, depth 385 ppm, formal BLS S/N 9.44; odd/even
  mismatch 3.034 sigma, just over the old threshold.
- Exposure-model period 17.29370 days, depth 418 ppm; conditional depth S/N 6.26
  and odd/even 1.752 sigma. This remains a marginal signal.
- QLP Sector 18 supports two unequal events (~195 and 751 ppm, default aperture).
  Sector 19 has no usable event coverage, so it is not a non-detection.
- Sector 18 pixels show strong adjacent positive and negative residuals near the
  bright star. The positive-flux moment alone is not a trustworthy on-target
  localization. An exploratory median-image/gradient decomposition fits very
  poorly (chi-square ~4291 for 26 dof); its apparent amplitude is not evidence
  for a transit and its formal error cannot be taken at face value.
- Older Sectors 24/25/52 were added to training, then an ephemeris was frozen
  before opening later Sectors 58/59/73. Predicted timing spread remains roughly
  0.79–1.08 days, far larger than half the fitted duration. All three tests are
  timing-inconclusive. Low fixed-phase S/N is not a decisive failed prediction.

TIC 317594826 is **not promoted**. No unique astrophysical or instrumental cause
is established. The new checks recovered a review opportunity, not a discovery.
Its later sectors 58/59/73 are now inspected data and cannot be called untouched
in subsequent work.

## Continuing scope

Batches covering ranks 1,001–3,000 remain active; do not count them as completed
surveys. Revisit their finished records with the exposure-aware diagnostics,
then pixel-vet any new review priorities. The remaining sensitivity losses in
variable/systematic-dominated light curves still motivate better residual
searches and broader controls. No external submissions have been made.
