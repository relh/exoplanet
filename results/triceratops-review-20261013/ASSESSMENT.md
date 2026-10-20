# Independent review of the TRICERATOPS calculation

## Scope

This review covers the planned single-sector calculations for TIC 80387959
(sector 36) and TIC 402358350 (sector 54). It does not provide independent
observations, validate either signal, or establish novelty. The completed bounded experiment passes the independent numerical checks
described below. These checks verify arithmetic and provenance, not planet
validation.

The reviewed inputs are already inspected observations. Their selection and
frozen ephemerides must remain explicit: these runs do not jointly evaluate all
available sectors or incorporate the previous timing and image tests as
independent likelihood terms.

## Input and implementation requirements

- Use native SAP with `dilution_corrected=False` in both `calc_depths` and
  `calc_probs`. Depth is a fractional flux decrement, despite the obsolete
  hosted API documentation's ppm label. The v1.1.0 release changed the default
  to corrected photometry.
- Keep the intended target in the first catalog row, with string identifiers.
  The package uses row position to distinguish target from neighbors.
- Use the original aperture mask and a consistent coordinate origin for its
  pixels and catalog positions. Explicit exposure integration is necessary;
  these observations are not two-minute exposures.
- Record catalog rows, missing-parameter estimates, and the package's
  depth-based host eligibility. Its Gaussian aperture model can exclude a
  neighbor nominally without establishing an observational exclusion. The
  previous neighbor-brightness audit retained uncertain alternatives.
- Require a usable background stellar population. The implementation silently
  omits field-star scenarios if that query fails; a normalized table alone
  does not establish that all scenario families were evaluated.
- Retain complete scenario tables, log-evidences, warnings, seeds and the
  `FPP_degenerate` flag. All-negative-infinite evidences or other numerical
  anomalies are failures, not astrophysical classifications.
- Compare repeated Monte Carlo seeds and increasing draw counts. Numerical
  scatter does not measure uncertainties in stellar parameters, baseline
  removal, ephemerides, dilution, or the omitted noise processes.

The current preparation subtracts previously fitted event baselines from SAP
and rescales by their average level. That is a conditional likelihood input:
baseline uncertainty and covariance are not marginalized by TRICERATOPS.
Scalar error inflation explores sensitivity without constructing a correlated
noise likelihood. The frozen clock must not be silently optimized to improve
these fits.

## Interpretation of the numbers

In this implementation, `1-FPP` is the sum of TP, PTP and DTP: planet scenarios
on the target with the included dilution alternatives. NFPP sums all resolved
neighbor scenarios, including planets orbiting those neighbors. Therefore
`1-FPP` is not the probability that a planet exists somewhere in the aperture,
and NFPP is not the probability of an eclipsing binary. An any-host planet sum
must explicitly include STP, BTP and NTP as well.

The model compares astrophysical transit and eclipse scenarios. It does not
include a general instrumental-artifact or stochastic-variable-star model.
Neither candidate can be validated solely by crossing a numerical FPP
threshold in these exploratory inputs. In particular, the unresolved source
and the previous TIC 402358350 timing failure remain material evidence.

## Sources inspected

- [Pinned v1.1.0 implementation](https://raw.githubusercontent.com/stevengiacalone/triceratops/v1.1.0/triceratops/triceratops.py).
- [Release changes](https://github.com/stevengiacalone/triceratops/releases/tag/v1.1.0).
- [Official tutorial](https://triceratops.readthedocs.io/en/latest/tutorials/example.html), including repeated Monte Carlo calculations.
- [Method paper](https://arxiv.org/abs/2002.00691).
- [Earlier feasibility assessment](../probability-feasibility-20261011/ASSESSMENT.md),
  [neighbor audit](../paper-host-vetting-20261012/ASSESSMENT.md), and the
  [80387959](../paper-vetting-80387959-20261012/ASSESSMENT.md) and
  [402358350](../paper-vetting-402358350-20261012/ASSESSMENT.md) noise audits.

Source review also found that the package plotting helper does not pass the
calculation's exposure integration parameters to its display models. A plotted
fit should be regenerated with the actual integration settings or labeled to
avoid implying that its curve reproduces the likelihood calculation.

## Independent input verification

[verify_inputs.py](verify_inputs.py) passes 5,357 checks recorded in
[input-verification.json](input-verification.json). The verifier reconstructs
the weighted baseline with normal equations, each event's baseline subtraction,
fractional depth and scalar noise, the unchanged clock in days, original FITS
aperture and WCS coordinates, Gaussian aperture integrals, and every source's
nominal eligibility. Sector 36 contains 482 samples from six events; sector 54
contains 230 samples from two events. Both have a 600-second cadence and
594 seconds of accumulated integration; the median-cadence approximation
differs from the FITS cadence by less than 0.01 second.

### Catalog duplicate identified

The raw catalog preparation contains a definite duplicate around TIC
402358350. TIC 402358335 and TIC 1918682525 have identical coordinates,
T magnitude and Gaia identifier. The latter is marked `DUPLICATE` with
`duplicate_id=402358335`. Both are initially eligible hosts. Retaining both
counts their light twice and creates two competing source entries with very
different estimated radii. The duplicate entries together contribute about
0.253% of the modeled total aperture light, predominantly this pair.

The raw-catalog runs should remain as evidence, with a deduplicated calculation
that removes only explicit duplicates whose retained counterpart is verified.
This correction must be distinguished from excluding a physically distinct
neighbor. Other uncertain `SPLIT` sources and nominal depth-based exclusions
remain separate model limitations.

The correction is now implemented and independently verified against the
original JSON catalogs: one duplicate is removed around TIC 80387959 and 21
around TIC 402358350. Every removed row has an explicit duplicate flag, its
specified counterpart remains present, and coordinates, magnitude and exact
Gaia identifier agree. The corrected inputs contain 347 and 2,268 catalog
rows, with 14 and 30 eligible hosts, respectively. Exact Gaia identifiers
were also checked for every retained row; preserving them as strings avoids
loss of integer precision during CSV import. These metadata corrections do
not change the time-series samples or clock.

Original input tables and numerical outputs are retained under
`../triceratops-20261013/original-catalog/`. The numerical verifier selects
only the explicit `summary.json` adopted-run list and checks that none comes
from that superseded directory. The dashboard exporter uses the same list
for its probability display and convergence figure.

## Thresholds and the principal TIC 402358350 neighbor

The [published method](https://arxiv.org/abs/2002.00691) defines numerical
validation criteria of FPP < 0.015 and NFPP < 0.001. Its less restrictive
“likely planet” class still requires NFPP < 0.001, alongside FPP < 0.5.
A high target-planet weight alone is therefore insufficient even for that
classification. These thresholds were evaluated in the paper's tested setup;
applying the numbers here is a comparison, not a substitute for convergence,
adequate inputs and observational vetting.

TIC 1918682563 remains an eligible host in the corrected TIC 402358350 model.
Its modeled aperture-light fraction is 0.0023079508, giving a required
intrinsic decrement of 25.23%. This is consistent with the earlier
[brightness audit](../paper-host-vetting-20261012/ASSESSMENT.md): an optimistic
all-throughput requirement of 20.59–23.08%, or 24.76–28.86% with equal target
and neighbor throughput. The two methods use different aperture assumptions;
neither measures an eclipse on that star.

Its NTP, NEB and NEBx2P scenarios are all included. Across the three
100,000-draw nominal runs their combined weight is 0.0437–0.0479%.
That small conditional weight reflects the adopted likelihoods and priors,
not an observational exclusion or a contradiction of the brightness budget.
The neighbor's temperature, radius and mass are photometric estimates held
fixed in each run. Resolved observations could still change the source
assessment.

The numerical entries are retained in the
[corrected catalog](../triceratops-20261013/402358350-stars.csv) and the
[seed 13](../triceratops-20261013/402358350-N100000-seed13-noise1-none-scenarios.csv),
[seed 29](../triceratops-20261013/402358350-N100000-seed29-noise1-none-scenarios.csv)
and [seed 47](../triceratops-20261013/402358350-N100000-seed47-noise1-none-scenarios.csv)
scenario tables.


## Completed numerical review

[verify_outputs.py](verify_outputs.py) passes **761 checks across all 17
completed runs**, recorded in [output-verification.json](output-verification.json).
The checks cover the exact bounded run identities; recorded light-curve,
stellar-table and plan hashes; cached background hashes; every eligible host
and scenario family; finite log-evidence accounting; normalization directly
from log evidences; all reported probability sums; and the summary's seed
ranges, medians, million-draw values and threshold comparisons. None of the
17 runs reports warnings or a degenerate calculation.

The adopted summary contains the eight nominal candidate calculations; noise
sensitivity and diagnostic controls remain separate. Original-catalog
outputs do not enter those summaries. All three hash-recorded TIC 80387959
replays reproduce the earlier corrected-catalog scenario CSV files byte for
byte and their reported metrics exactly. Two earlier TIC 402358350 runs
record four core input hashes rather than the later five: the added fifth
hash is the correction-plan document. Their actual corrected stellar tables,
light curves, input metadata and original plan are contemporaneously hashed
and match the adopted files.

| Candidate | Million-draw target-primary weight | FPP | NFPP |
|---|---:|---:|---:|
| TIC 80387959 | 92.4284% | 7.5716% | 4.2862% |
| TIC 402358350 | 97.6834% | 2.3166% | 0.3959% |

Both candidates fail the published joint numerical validation thresholds
and the nearby-source threshold for the paper's “likely planet” category.
Three 100,000-draw seeds span 92.2334–92.7963% and 97.3632–97.8000%,
respectively. One million-draw seed per candidate does not satisfy the
original convergence requirement. These ranges do not measure physical
uncertainty.

Doubling the scalar noise changes target-primary weights to 91.9765% and
93.7369%, respectively; a scalar multiplier does not model temporal
correlation. The constant-flux controls set every sample to unity, removing
both the dip and scatter. They still receive target-primary weights of
44.1543% and 23.3766%; inverted flux receives 41.9880% and 15.9104%.
Their retained periods and observed-depth host eligibility make these
computational diagnostics, not false-alarm experiments. The restricted
Kepler-93 b control yields 82.8783% target-primary weight and fails the
validation thresholds despite the planet's independently established status.
This configuration has not been calibrated against a population of known
planets and false positives.

The reviewed webpage exporter requires a complete 17-run summary and the
completed independent verification before publication. It selects the eight
nominal runs for its candidate figures, reports the model and convergence
limitations beside the table, and retains controls in an expandable section.
Neither candidate should be promoted or assigned calibrated discovery odds
from these results. TIC 402358350's higher model weight does not resolve its
previous timing failure or establish that it is the stronger overall lead.
