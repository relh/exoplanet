# Two other TESS signals: no convincing nominal-clock ZTF agreement

TIC241928959 and TIC422626648 do not show convincing combined ZTF dimming at their unchanged nominal TESS clocks. Neither result excludes the corresponding TESS signal: very few measurements fall in the nominal windows and the propagated clocks are uncertain over most of the ZTF baseline.

| Target | Quality-screened points | Nominal in-window points | Combined depth | Formal error | Formal SNR | Residual-scaled SNR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TIC241928959 | 779 | 5 | 0.476% | 0.426% | 1.12 | 0.66 |
| TIC422626648 | 466 | 3 | −0.162% | 0.687% | −0.24 | −0.15 |

For TIC241928959, the early subset has two nominal in-window points and a negative fitted depth. The later subset has three and a1.581% fitted depth, formal SNR2.94 but residual-scaled1.89. That sparse later value does not supply a secure repeating dip. For TIC422626648 the subsets have two and one nominal in-window observations, neither giving convincing dimming. Negative depths represent fitted brightening, not a physical negative transit.

The original periods, epochs and durations were not changed. Converted times use the previously documented conditional UTC-based HMJD interpretation; results.json also retains the alternative TDB-based calculation. Object-specific median magnitudes define flux normalization using all available observations, followed by separately fitted object baselines. Early/later subsets are descriptive, not a new reserved experiment. No photometric outlier rejection or phase optimization was performed. Forty-one shifted windows are retained as diagnostics, not a calibrated false-alarm distribution.

All six zoomed fold panels were inspected. The plots show sparse coverage rather than a clean repeated depression at either nominal clock. The prior timing audit found no reliably useful in-window observation for these two targets under its conditional gate. Therefore a flat nominal fold cannot reject a true signal whose phase has drifted. The positive TIC196681132 result remains distinct and is not generalized to these stars.

Deterministic2% injected box dips with unequal object baselines recover the imposed amplitude in both data sets. verify.py independently reconstructs95 original, subset, filter, alternative-scale and shifted-window fits using weighted within-group centering; input hashes match. All49 repository tests passed in22.09seconds. No global scientific module changed. The controls test numerical measurement behavior, not survey completeness or absence of astrophysical false positives.

TIC241928959 remains unresolved with target-favoring TESS image fits. TIC422626648 retains the earlier Gaia RV variability concern. Neither is promoted to a credible new planet candidate by this run. Future work needs better-timed independent coverage or an explicitly exploratory timing search whose selection effects are retained.
