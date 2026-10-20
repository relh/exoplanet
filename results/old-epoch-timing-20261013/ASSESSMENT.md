# Timing feasibility for early survey observations

**Both signals fail their original timing gate at all four tested early epochs.** A narrow-window non-detection at a saved nominal clock would therefore be inconclusive. This metadata-only calculation does not establish survey coverage, inspect flux, or change either candidate's classification.

## Propagated timing envelopes

Calendar labels specify nominal midnight **TDB**, used only to select a nearby reference event; they are not observer UTC exposure times. The table gives the full selected-profile midpoint envelope, including three times each saved heuristic epoch floor. These envelopes are **not confidence intervals**. Durations are not added to these widths.

| Reference epoch | TIC 80387959 frozen profile | TIC 402358350 expanded profiles | TIC 402358350 historical profiles |
|---|---:|---:|---:|
| 2004-01-01 | 3.26 h | 37.87 h | 225.20 h |
| 2006-01-01 | 2.98 h | 33.80 h | 199.90 h |
| 2008-01-01 | 2.71 h | 29.72 h | 174.59 h |
| 2009-01-01 | 2.57 h | 27.62 h | 161.54 h |

For TIC 80387959, the maximum absolute profile displacement plus floor is 1.53–1.95 hours, exceeding its original 1.113-hour half-duration threshold. For TIC 402358350, the expanded primary clock gives 9.93–13.35 hours against a 1.728-hour threshold; the expanded sensitivity and historical rows also fail. All 20 row/epoch comparisons fail; none was omitted or replaced by a more favorable clock.

These failures do not make a long survey light curve useless. Adequately sampled observations could reveal repeated eclipses or constrain timing across the retained profile family. Such an experiment needs its own frozen coverage, precision, dilution, time-convention and decision rules. A clock fitted to the survey observations would be an exploratory recovery, not a successful unchanged prediction. Any null result would require demonstrated sensitivity across the relevant timing hypotheses, not only the nominal phase.

## Cycle convention and limitations

The calculation uses every retained row and period/epoch pair from [the existing timing packet](../followup-planning-20261013/targets.json): one TIC 80387959 row with five profile pairs; two expanded TIC 402358350 rows with 10 and 25 pairs; and two historical rows with 134 and 139 pairs.

For each date, the nearest event is chosen once using the target's expanded primary clock (the frozen clock for TIC 80387959). Other row epochs are aligned at that primary reference epoch; every profile epoch is first aligned to its own row reference. The same integer event index is propagated backward. Predictions are **not wrapped toward the early date or primary prediction**, which could hide accumulated disagreement. An independent nearest-row cycle is retained only as a diagnostic. At 2009-01-01 the historical primary TIC 402358350 clock chooses a different nearest calendar-date event; its row still uses the common reference-aligned event. Thus independently rounding each clock to the early date would produce a misleading comparison.

The historical TIC 402358350 envelope is less than one period at these four events, but some endpoint offsets exceed half a period. This broad disagreement must not be compressed modulo the period. The selected likelihood profiles and heuristic floors omit red noise, model mismatch, transit-timing variation, and uncertainty outside the retained family. The four representative dates are not a guarantee for every observing date. Exact future sample times must be assessed separately, including barycentric and time-scale conventions.

## Reproduction and provenance

[plan.json](plan.json) and its SHA-256 were frozen before running the calculation. [calculate.py](calculate.py) reads only the existing metadata packet and writes [rows.csv](rows.csv), [results.json](results.json), and [provenance.json](provenance.json). No network request, photometry access, refit, or import of the historical packet builder occurred.

[verify.py](verify.py) independently reproduces every propagated endpoint and original gate using decimal arithmetic and Gregorian calendar differences, without importing the calculation or Astropy. All **1,588 checks pass**; [verification.json](verification.json) records the result. This verifies arithmetic and provenance, not physical timing accuracy or candidate validity.

Run from the repository root:

```sh
uv run python results/old-epoch-timing-20261013/calculate.py
uv run python results/old-epoch-timing-20261013/verify.py
```
