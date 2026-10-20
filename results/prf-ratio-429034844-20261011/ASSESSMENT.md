# TIC429034844: brightness-ratio constraints reduce the neighbor preference

The previous unconstrained scene registration assigned essentially zero flux to TIC429034844 and2039 units to its much fainter close neighbor611135702. This was a mathematical blend degeneracy, not a credible measurement of their separate brightnesses. Its associated large difference-image chi-square contrast therefore needs model sensitivity checks.

This run ties the two scene templates with a fixed neighbor/target flux ratio, while retaining an independently fitted third star, planar background and common two-dimensional registration. All five ratios were recorded before evaluation: one quarter, one half, one, two and four times the catalog T-band ratio0.0615857. This deliberately broad grid is a sensitivity range, not a catalog error interval or calibrated prior. The previously computed43-event sector70 difference stack, joint short clock, mission PRF and formal errors were unchanged.

| Ratio factor | Scene squared residual | Target chi-square | Neighbor chi-square |
|---:|---:|---:|---:|
|0.25|1881.87|357.79|299.22|
|0.5|1889.69|358.28|298.75|
|1|1908.14|364.57|295.58|
|2|1941.31|385.77|286.97|
|4|1990.50|425.84|275.32|

At the catalog ratio, the registration is(−0.116490,0.051979) pixels, compared with(−0.018245,0.083172) for the unconstrained fit. The neighbor remains preferred, but its chi-square advantage falls from626.29 to69.00. All five ratio cases favor the neighbor. The scene squared residual uses uniform weights and is not a likelihood or confidence interval; the difference-image statistic still assumes diagonal formal errors. Neither provides a calibrated probability of either host.

Five noiseless matched-model synthetic scenes, one for each ratio, recover their known registration within1e−5 pixel. These validate the numerical calculation, not instrument-model accuracy. The existing suite also passed49 tests. The source-fitting module itself is unchanged; this diagnostic changes the constraint on scene fluxes.

Disposition: neighbor contamination remains favored conditionally, but the original strength was sensitive to an unphysical flux decomposition. Unique source attribution remains unresolved. PRF shape error, additional scene sources, flux/color uncertainty, detector registration and the absence of independent epochs in this source fit remain limitations. Do not promote the signal to a likely planet or claim a validated neighbor eclipse. More repetitions of matched-template controls cannot calibrate those missing uncertainties.

[Recorded ratios and inputs](plan.json) · [Full results and controls](results.json) · [Reproducible calculation](run.py) · [Verification](verification.json).
