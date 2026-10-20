# Same-epoch SPOC/QLP comparison: no consistent QLP depth suppression

**The paired check does not support a universal “QLP is shallower” explanation for the later depth difference.** With matched cadences and the same local-baseline/clock procedure, QLP is slightly shallower in sector36 but deeper in sector37. Neither difference alone is decisive under the conditional error model. This also does not demonstrate astrophysical evolution: the later sectors have different extraction, dilution, sampling and systematic errors.

| Same-epoch subset | Matched cadences | TESS-SPOC depth, ppm | QLP depth, ppm | Paired SPOC−QLP depth, ppm |
|---|---:|---:|---:|---:|
| Sector36 | 2,604 | 890 ±96 | 844 ±104 | +47 ±76 |
| Sector37 | 2,745 | 803 ±103 | 966 ±121 | −163 ±96 |

These are shared photons, not independent observations. The final column fits the normalized per-cadence difference directly, rather than assuming independence and adding the two products' variances. Its uncertainty describes white residual scatter in that difference; correlated reduction artifacts remain possible. Event omissions give +10 to+94 ppm for sector36 and−279 to−49 ppm for sector37.

**Sampling is another material effect.** The [parent analysis](../ASSESSMENT.md) on each product's own valid cadences found SPOC depths813 and904 ppm in sectors36/37. On the common-quality subsets these become890 and803 ppm. The selection changes measured depth as well as uncertainty, so cross-epoch depth comparisons must account for actual accepted samples.

This two-sector check cannot calibrate QLP90/100. The [official QLP page](https://archive.stsci.edu/hlsp/qlp) states that TGLC-based extraction is used beginning with sector94. Sector100 therefore has an additional extraction distinction from sector90 and these older paired products. A transit-host/dilution conclusion remains unjustified.

## Frozen comparison and verification

A separate [plan](plan.json) was frozen after the parent comparison and before these fits. This follow-up was chosen retrospectively in response to the apparent cross-product/epoch depth difference. It preserves hashes of the parent result and four cached raw inputs. Unique nearest timestamps were matched within8.64 seconds; actual maximum offsets are1.959 and1.981 seconds. Both products use approximately10-minute native cadence. Each uses its own median cadence for box integration at the common midpoint timestamp, with identical original clock, event selection and joint event intercept/slope baselines. No period, duration, aperture or phase optimization was added. The immutable plan's phrase “no ... depth ... optimization” was imprecise: depth is estimated by the explicitly declared linear fit; there is no search over nonlinear transit shape or tuning toward an expected depth.

The 2,604 and 2,745 matched points are the full quality-selected overlaps, not all points entering the local fit. Five primary events survive in sector36 and four in sector37. Native quality-zero finite positive flux/error selection is required in both products; normalized flux uses each product's median over the matched sample. All selections and matched indices are retained.

[verify.py](verify.py) independently checks four raw hashes, unique matching and offsets, normalized data reconstruction, six normal-equation fits/covariances and every event omission. [verification.json](verification.json) passes; [comparison.png](comparison.png) was inspected. [Implementation notes](implementation-notes.md) retain an initial path-type error before fitting and its correction.

```sh
OPENBLAS_NUM_THREADS=1 uv run python results/strongest-80387959-shape-20261012/paired-products/verify.py
```

No new observations were opened. Candidate assessment remains unchanged.
