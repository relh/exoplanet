# TIC241928959: no convincing dip at half-phase

A fixed half-phase check finds no convincing secondary eclipse at the original
3.532592898-day clock. The primary timing was not reoptimized. We tested the
primary duration0.032days and twice that duration, under the two predeclared
1.5/2.5-day detrending windows.

| Detrending window | Test duration | Depth | Formal error | Formal SNR | Measured events |
|---|---|---|---|---|---|
| 1.5d | 0.032d | 205ppm | 785ppm | 0.26 | 5 |
| 1.5d | 0.064d | 592ppm | 554ppm | 1.07 | 5 |
| 2.5d | 0.032d | 393ppm | 875ppm | 0.45 | 4 |
| 2.5d | 0.064d | 582ppm | 620ppm | 0.94 | 4 |

This is not a binary exclusion or a calibrated upper limit. A faint secondary,
an eccentric eclipse away from half-phase, or a different duration can evade
this check. Formal errors omit correlated noise and detrending uncertainty.
The windows use overlapping observations and do not provide independent evidence.
No wider phase search was performed. The target remains unresolved, without
convincing independent photometric confirmation.

`plan.json` records settings and input/code hashes before the run. `results.json`
retains full event measurements and raw provenance. `verify.py` independently
reconstructs all four weighted depth/error calculations and checks raw hashes.
Eight additive-signal controls pass on the already flattened data; these verify
arithmetic, not recovery through detrending. Phase plots were inspected.

The existing test suite passed49 tests in30.54s.
