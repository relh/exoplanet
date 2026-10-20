# Secondary-signal and QLP checks, 2026-10-09

No likely new planet established in these checks. Original searches and failed
checks remain immutable; every additional search adds trials.

## QLP exposure-model companions

The companion rescreen now explicitly supports QLP input and validates the
collection. It preserves each target's missing-error policy and records the
reloaded input evidence. Missing QLP crowding is deferred to pixel checks, not
interpreted as evidence of isolation.

All 113 successful newer QLP searches received companion selection checks in
five `model-campaign-newer-qlp-*` runs. None produced a review priority. This
means no eligible peak survived those companion cuts, not that every possible
planet was fitted or ruled out.

## Residual searches

Masking a dominant transit before searching for additional planets is illustrated
in the [official Lightkurve tutorial](https://lightkurve.github.io/lightkurve/tutorials/3-science-examples/exoplanets-identifying-transiting-planet-signals.html).
Our exploratory implementation masks the current observed best feature only
when its formal S/N is at least 8. The total mask width is twice its fitted
duration. At most two rounds were used here, with a cumulative 20% removal cap
and at least 200 retained points. The usual detrending, inverted-light-curve and
event checks run again. Masking does not classify the removed feature.

- Of the 41 previously missed periods in the 96-injection grid, nine reappeared
  among residual peaks. **None became a new full-screen pass.** The original
  33 full passes remain unchanged. This conditional audit is not completeness.
  Truth selects and scores the audit cases; masks and fits use observed peaks.
- In the known L98-59 system, masking c at 3.69068 days recovered known b at
  2.25314 days (581 ppm, S/N 15.75). Masking b as well recovered known d at
  7.45085 days (945 ppm, S/N 11.61). Both passed the screen. These are positive
  controls, not discoveries. GJ 357 had no screened residual after masking b.
- A selection was saved before searching 20 real targets from the first four
  completed batches. Eligibility required a dominant S/N >=8, no original
  follow-up priority, and estimated first-mask fraction <=10%; eligible targets
  were ordered by measured scatter floor, then TIC. All 20 completed with no
  errors and no residual review priority. See `residual-real-selection-20261009`
  and `residual-real-20261009` for policy, inputs, hashes and results.

The alternate-detrending check still compares the global best with each candidate,
which can penalize secondary signals. The injection failures expose this limit;
the criteria were not loosened to produce detections.

## Technical checks

Transient GET connection/timeout failures now receive at most three attempts;
successful download evidence retains the failed attempts. HTTP errors are not
retried or cached as data. This does not erase the original batch-six DNS errors,
which require a separately recorded retry selection.

Difference figures now explicitly mark the catalog target separately from the
brightest source. Neither a global difference maximum nor the brightest image
source alone establishes the origin of a dip. Proper motion is not propagated,
edge-clipped moments are biased, and positive/negative dipoles need inspection.

Validation: 28 tests passed, including recovery of a synthetic second transit
after masking a stronger first transit, and transient-download retry behavior.
