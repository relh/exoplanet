# HD 32564: selected sampling-alias comparisons

The three shorter reported periods predict the omitted years better in aggregate
than each tested alias. The approximately 49-day component remains ambiguous.
This is a limited, retrospective diagnostic of an external lead, not validation.

We compared one replaced component at a time using |f +/- f_sampling| for solar
and sidereal daily sampling and yearly sampling. Each model refits the remaining
components, an offset, a trend, and either no activity terms or all six linear
activity terms. Training-only period neighborhoods use fractional width
min(0.02, 0.45*period/training_baseline). This keeps local fits near the intended
frequency family. Four omitted years, two reductions, two activity choices and
24 aliases yield 384 comparisons, all completed without errors.

Below are summed held-year chi-square differences (alias minus reported model)
for the closest tested alias with all six activity terms. Positive values favor
the reported model. These sums are not calibrated significances.

| Reported period (days) | Closest alias seed (days) | SERVAL | DRS |
|---|---|---|---|
| 2.55663 | 1.63506 | 42.45 | 27.00 |
| 11.06327 | 1.09607 | 19.80 | 15.89 |
| 23.61185 | 1.04125 | 17.20 | 11.65 |
| 49.10219 | 1.01794 | 5.13 | -0.34 |

Some individual omitted years favor aliases, including among the shorter-period
signals. The 49-day model does not clearly beat its daily alias in DRS with
activity terms; its combined difference is slightly negative. This supplements
the separate negative omitted-year component tests and reinforces its
model-sensitive status. The SERVAL and DRS reductions share the same spectra.

Two alternative fits reach their permitted boundaries (the 23.6-day yearly alias
in SERVAL/all-activity/2013 and the 49-day yearly alias in DRS/all-activity/2010).
All parent fits are interior. Boundary results and every year-level reversal
are retained; no assertion that all aliases have been excluded. The experiment
uses local optimization and single-component substitutions, not all combinations,
eccentric harmonics, Gaussian-process activity or a full generative window test.
Period families were already known from the complete archive, so this is not
blind evidence. Held activity values are observed covariates.

[Sampling aliases in RV data](https://arxiv.org/abs/1005.4050) motivate the tested
frequency alternatives; our omitted-year comparison is not a reproduction of
that paper's complete method. Plans, input hashes, models, window amplitudes,
per-year differences and aggregate audit are saved here. The per-period bounds
extension passed the full 48-test suite, including unseen-data RV prediction.
