# ZTF requests and timing limitations

The three position queries completed on process82108 with read timeouts for every target. The worker exited0 after recording these errors. No light curves were downloaded; this is not evidence of absent observations. Do not restart this completed worker. `audit.py` distinguishes download errors, invalid schemas, empty tables and usable objects, and report source separations/quality counts without claiming a transit recovery.

Before external data analysis, existing frozen TESS timing estimates were propagated to hypothetical lookback times using the established conditional heuristic. At365days before the reference, spreads are0.1411days for422626648,0.1470days for241928959 and0.03647days for196681132. Their half-durations are0.01984,0.016 and0.016days respectively. All exceed the narrow-window precision criterion. At30days, only196681132 meets it. These are not full physical timing posteriors and do not yet use actual ZTF timestamps.

A missing dip at a narrow extrapolated window therefore cannot exclude these signals at year-scale lookbacks. Future comparisons need actual timestamp conversion and timing-range coverage, not a silent refit followed by a claim of blind prediction. No independent recovery, planet exclusion or novelty is established. Existing clocks and hashes remain fixed.
