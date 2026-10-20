# TIC241928959: alternating-depth check is inconclusive

The fixed-clock odd/even depth comparison does not show a significant difference, but only one usable odd-family event remains. This is insufficient to exclude an eclipsing binary. Do not interpret equal fitted depths as validation of a planet.

With the1.5-day detrending window, the even/odd depths are1.21898% and1.12829%, differing by0.09069percentage points or0.46 times the combined formal uncertainty. There are four even-family events and one odd-family event. With the2.5-day window, depths are1.19375% and1.13889%, differing by0.05486percentage points or0.27 formal sigma; three even-family events and one odd-family event remain. The two detrendings reuse observations and are not independent checks.

The existing3.532593-day period, epoch and duration were retained without retiming. Nearest-cycle parity partitions the data, then each family is measured at twice the period using the existing fixed_measure implementation. Per-family event indices in results.json refer to that doubled period: the first window's even indices0/1/2/3 correspond to original cycles0/2/4/6, and its odd index0 to original cycle1. Longer detrending removes the original even cycle2 from the usable measurement. No observed absence is inferred for excluded cycles.

The single odd event cannot supply an event-scatter uncertainty. Those combined uncertainties and significance values are therefore null. The initial copied reporting script attempted arithmetic with the missing uncertainty and stopped; initial-run.py and initial-plan.json preserve that failed attempt. The corrected script retains null explicitly. No scientific measurement function or historical result changed.

All four plotted panels were inspected and all four measurements reconstructed from hashed input data. Both families contain a dip, with substantially fewer usable points in the odd family. The existing secondary.json in the original review reports an exploratory selected dip SNR3.13 over1878 trials and a stronger selected brightening of magnitude SNR5.09; those are not calibrated binary evidence. This analysis does not independently recover that secondary feature or introduce a new secondary search.

The image-response evidence favors the target region over its catalog neighbor, but this alternating-depth check provides no physical classification. Independent observations or stronger binary diagnostics are still needed. No new planet candidate is promoted.
