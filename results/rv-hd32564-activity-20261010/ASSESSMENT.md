# HD 32564: activity-conditioned prediction and period-bound sensitivity

The three shorter reported RV components remain supported by these limited
checks. The weaker approximately 49-day component is model-sensitive. This is
continued analysis of an external lead, not a new discovery or validation.

The common complete sample has 192 pre-upgrade spectra forming 180 nights in
both SERVAL and DRS reductions. Four omitted-year tests (2010–2013) compare no
activity terms, H-alpha alone, R'HK alone, and six simultaneous indicators
(H-alpha, R'HK, BIS, FWHM, dLW, CRX). All fits include an offset, trend, circular
sinusoids and fixed 2 m/s nightly jitter. Predictor means/scales, linear
coefficients and periods are fitted only on training years. Held-year activity
measurements are observed covariates, so this is conditional prediction rather
than a forecast without observing that year.

The first experiment used the previous +/-0.1% period neighborhoods. All 128
component checks improved prediction, but some fitted periods reached their
bounds. A separately retained post-hoc +/-1% experiment addresses that constraint.
No full-model fit reaches the wider boundary. The three shorter components
improve prediction in every wider experiment. The approximately 49-day component
fails in the 2012 DRS test with no activity terms, H-alpha alone, or R'HK alone:
held-year chi-square improvements are -4.96, -4.19, and -2.59 respectively.

With all six indicators, the wider experiment gives these omitted-year
chi-square improvement ranges; positive values favor retaining the component:

| Period (days) | SERVAL | DRS |
|---|---|---|
| 2.55663 | 53.40–149.42 | 55.53–172.72 |
| 11.06327 | 26.59–104.76 | 33.31–149.65 |
| 23.61185 | 26.27–63.39 | 24.30–70.01 |
| 49.10219 | 4.85–20.16 | 2.52–17.43 |

The all-indicator results do not override the weaker component's failures in
other models. These improvements are not false-alarm probabilities or marginal
likelihoods. Both RV reductions use the same spectra, period families were known
from the already-opened dataset, and activity terms are linear and simultaneous.
Indicator errors, lagged relationships, correlated activity noise, eccentricity,
and comprehensive aliases remain unmodeled. Adding six indicators sometimes
worsens predictive RMS. No assertion that stellar activity has been excluded.

The indicators and archive are described by [Perdelwitz et al.](https://arxiv.org/abs/2311.12438).
Data URL/SHA provenance is in ../user-posts-20261010/hd32564-source.json. Plans,
nightly arrays, every fitted model and negative outcome are retained in this
folder and ../rv-hd32564-activity-wide-20261010/. The model passed deterministic
unseen-data and activity-only tests; the full suite passed 48 tests. A summary
serialization error is recorded in audit-error.json; fits were unaffected.
