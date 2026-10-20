# Reserved-sector tests: timing predictions are inconclusive

Discovery-only refinements were saved before either reserved product was fetched.
Both products were successfully measured at those fixed predictions.

| TIC | Reserved sector | Refined period | Timing spread | Duration | Measured depth | Formal SNR |
|---|---|---|---|---|---|---|
|396160833|79|13.500444d|2.558d|0.1584d|15ppm|0.56|
|34576133|85|9.377743d|1.986d|0.2160d|226ppm|7.70|

The prediction spreads greatly exceed half the fitted durations, so the existing
predeclared timing gate calls both **inconclusive**. The spreads are conditional
profile estimates with a heuristic epoch floor, not physical timing posteriors.
Neither refinement hits its period-search boundary, but that does not overcome
the long extrapolation from the short discovery baseline.

TIC396160833's small nominal-depth measurement is not an exclusion. TIC34576133's
positive nominal measurement is not confirmation: timing is uncertain, its shape
is broad, and the separate exact-identity check identifies it as known rotational
variable BW Ari. Expected nominal formal SNRs of5.98/25.43 do not override these
limitations. Phase controls are dependent and not false-alarm probabilities.

`verify.py` reconstructs both measurements and prediction spreads, checks raw
hashes/FITS identities and verifies freeze timestamps precede download timestamps.
The discovery-batch assertion that reserved files were absent describes its
pre-follow-up audit; these two products are now intentionally opened. Remaining
previously unused epochs cannot be called reserved under a new post-inspection
choice without explicitly documenting the changed design.

No source-attribution or physical planet validation follows from this check.
For TIC396160833, additional earlier discovery epochs could improve the clock,
but this sector79 test must remain recorded as already inspected.
