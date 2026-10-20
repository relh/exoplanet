# TIC96166003: discovery timing is insufficient for a precise distant test

The discovery-only profile admits enough period/epoch uncertainty that projections to both unopened sectors19 and59 are imprecise. A nominal-clock non-recovery there would not exclude this signal. The original discovery clock and both detrending profiles are retained; no additional or reserved target observations were opened.

| Detrending | Refined period(d) | Box duration(d) | Depth(ppm) | Accepted period range(d) | Approximate spread at19 /59(d) |
|---|---|---|---|---|---|
|1.5d primary|0.954748838|0.072|281.77|0.954652424–0.955492598|0.550 /0.373|
|2.5d sensitivity|0.954738508|0.072|260.79|0.954538794–0.955575238|0.620 /0.418|

Each spread is much larger than half-duration0.036d. These are conditional maximum propagated offsets plus a heuristic epoch floor, not posterior credible intervals. Sector19 is earlier than discovery and has the longer extrapolation. Period/epoch covariance is retained through all165/288 accepted pairs rather than independent interval endpoints.

## Method and limitations

[plan.json](plan.json) predates the fits. Each window uses2049 period points across the original selected family, spacing0.00000344333d, with durations0.048/0.060/0.072d and BLS oversample50. The accepted profile uses delta log likelihood≤4.5. Neither accepted period profile touches the searched period boundaries. **Both best durations are at the upper duration-grid endpoint**, a shape-model limitation not represented by `search_boundary_hit`, which checks period only. No duration confidence interval or physical-shape inference is justified. Profile plots were visually inspected; the primary profile has several separated threshold-crossing islands, all retained.

[verification.json](verification.json) reconstructs the two raw discovery reductions and independently rebuilds both full period/duration grids using the same Astropy BLS implementation. It checks all profile pairs, original and refined fixed-clock depth arithmetic, hypothetical timing propagation, chronology and absence of19/59 light-curve caches. This is reproducibility of selected-family box/white-error calculations, not independent search selection, correlated-noise calibration or validation.

[sector-projections.json](sector-projections.json) uses only published calendar endpoints: [NASA sector19 summary](https://heasarc.gsfc.nasa.gov/docs/tess/sector19_summary.html) gives2019-11-28 to2019-12-23; [sector59 summary](https://heasarc.gsfc.nasa.gov/docs/tess/sector59_summary.html) gives2022-11-26 to2022-12-23. Raw pages and retrieval/hash provenance are saved. UTC calendar endpoints converted to JD−2457000 are illustrative, not actual barycentric target cadence times. Actual cleaned timestamps must determine a future gate. Independent propagation arithmetic reproduces all four reported spreads.

The earlier [discovery review](../review-96166003-20261011/ASSESSMENT.md) and weak near-target image signal remain relevant. This timing test does not improve source attribution. Before any new-data test the terminal parent audit and cache/history preflight remain mandatory. [prospective-protocol.json](prospective-protocol.json) preserves an unchanged-clock test with explicit timing-inconclusive outcome; it authorizes no automatic data opening. A separately planned multi-sector training search may be more informative, but any data used to choose a clock cannot also count as a blind confirmation of that clock.

Reproduce with `uv run python results/timing-96166003-discovery-20261011/verify.py`. No shared scientific source changed. A setup attempt initially used a mistyped input path and failed before any plan or observation access; the corrected script then froze and ran normally.
