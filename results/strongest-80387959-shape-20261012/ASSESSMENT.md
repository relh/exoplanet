# TIC 80387959: fixed-clock shape and binary diagnostics across six opened sectors

**The dip persists without global flattening, but its host and physical nature remain unresolved.** Direct corrected-flux fits with local event baselines recover positive primary depths in all six already opened sectors and under every individual-event omission. No coherent odd/even difference or exact-half-phase secondary emerges. Sector36 has an isolated profile asymmetry. These results retain the signal; they do not establish a planet or exclude binaries.

| Sector / product | Primary depth, ppm | Even − odd, ppm | Exact-half secondary, ppm |
|---|---:|---:|---:|
| 10 / TESS-SPOC | 1038 ± 109 | −106 ± 219 | +40 ± 107 |
| 36 / TESS-SPOC | 813 ± 87 | −9 ± 174 | −94 ± 105 |
| 37 / TESS-SPOC | 904 ± 91 | −341 ± 186 | +88 ± 91 |
| 63 / TESS-SPOC | 807 ± 93 | −50 ± 190 | −117 ± 90 |
| 90 / QLP | 613 ± 89 | +72 ± 178 | +31 ± 86 |
| 100 / QLP | 582 ± 99 | +111 ± 199 | −113 ± 88 |

Errors are conditional linear-model errors, inflated by residual scatter when necessary. They do not fully model correlated noise, aperture/dilution errors or pipeline systematics. The table is retrospective, not six new blind recoveries.

## New discriminating information

**Global flattening is not needed to recover the dips.** This run uses native quality-zero PDCSAP_FLUX or DET_FLUX, with no additional global filter or clipping, and jointly fits individual local baselines with the fixed transit signal. The lowest primary depth after any event omission is 494 ppm in sector100; all omitted-event fits remain positive.

**A baseline fitted across the unmasked dip self-subtracts it.** A deliberately unmasked baseline comparator returns only 826–832 ppm from a deterministic 1000-ppm injected box, while the joint signal/baseline model recovers 1000 ppm. The corresponding measured depths are lower by about17%. This is a measured transfer property of the declared local procedure, not evidence for a shallower physical transit. The unmasked comparator is retained as a failed preprocessing alternative; it does not supersede the joint result. Injection is performed after archive pipeline processing and does not measure upstream attenuation.

**There is a product/epoch depth difference requiring care.** The descriptive inverse-variance means are 877 ± 47 ppm for original TESS-SPOC sectors10/36/37/63 and599 ±66 ppm for QLP90/100. Different products and apertures, source blending, crowding corrections and correlated systematics can change measured depth. The [QLP extraction](https://archive.stsci.edu/hlsp/qlp) changed to TGLC-based processing beginning with sector94. These differences therefore cannot be identified as time-varying astrophysical depth. No common-host radius or companion size is inferred. The subsequent, separately frozen [same-epoch paired-product comparison](paired-products/ASSESSMENT.md) finds no consistent QLP suppression and reveals common-cadence selection sensitivity. It does not resolve the later depth difference.

**Profile asymmetry is not consistently replicated.** Five exposure-integrated bins cover the original-duration ingress, core and egress plus adjacent shoulders. Sector36's ingress-minus-egress contrast is −639 ±233 ppm, while other sectors give +97±345, −358±246, −323±245, −241±234 and−27±261 ppm. Fixed ephemeris uncertainty, noise and reductions can produce asymmetry. This single conditional discrepancy is not an eclipsing-binary identification. The outer shoulder bins generally return toward baseline; no fitted new duration was adopted.

The parity and secondary checks have no coherent positive anomaly. An eccentric binary could have its secondary away from half phase; unequal brightness, dilution or inadequate precision can hide a secondary. These tests do not exclude those cases. No new period or secondary-phase search was performed.

## Frozen method and provenance

[plan.json](plan.json) predates fitting and preserves six raw hashes/retrieval records, the original fixed P=4.192168718052227 d / BTJD1575.375831123655 / duration0.092736 d and its unchanged timing-profile pairs. All six observations were already inspected; sector64/99 collateral cutouts are excluded from stellar analysis. Original target/period selection and prior follow-up results remain selection history.

Twenty-four declared models comprise a five-bin profile, single primary box, original-cycle even/odd boxes and exact-half secondary in each sector. Each event window spans±3 original durations and requires at least2 inside points,5 outside points and2 on each side. Event intercepts and slopes are joint nuisance parameters. Box/bin overlaps are integrated across the median native cadence; no new ephemeris, duration or limb-darkening fit occurs. Covariances use published errors with max(1, sqrt(chi²/dof)) residual inflation. Every event is omitted in turn. Native exposure smearing is accounted for approximately by median cadence, rather than resampling later data to the earliest30-minute cadence.

This differs from the [earlier physical fit](../physical-80387959-20261009/run.json), which used combined original sectors with global preprocessing and a physical transit model, and the [earlier secondary scan](../secondary-companion-20261010/80387959.json), which selected secondary phase on the original four sectors. The current check tests fixed shape/parity/half-phase behavior across later epochs without those freedoms.

## Verification

[verify.py](verify.py) independently checks raw hashes/identities and native data selection, exposure-overlap matrices, all24 fits and covariance matrices using normal equations, every omission result, and an analytic baseline-projection calculation of the injection transfer. [verification.json](verification.json) passes; the maximum solver discrepancy is <9×10⁻¹⁸ relative flux. [diagnostic.png](diagnostic.png) was visually inspected. This verifies implementation and arithmetic, not calibrated astrophysical probabilities.

```sh
OPENBLAS_NUM_THREADS=1 uv run python results/strongest-80387959-shape-20261012/verify.py
```

No new observations, downloads, source attribution, shared scientific module or candidate grade was introduced.
