# Additional orbital-modulation tests: TIC 80387959 and TIC 241928959

**Neither candidate acquires a robust new binary diagnostic or a planet promotion.** This is a new analysis of already inspected observations, not independent recurrence. We tested whether out-of-eclipse light varies coherently at the original orbital clock and twice its frequency, extending previous localized secondary/parity tests to the rest of the orbital phase curve.

- **80387959:** small harmonic coefficients depend on sector, baseline and pipeline product. No substantial, stable phase-curve signature emerges across the four sectors. Absence here does not exclude a companion, particularly because corrected flux may suppress real broad variation.
- **241928959:** one sector has a weak positive second-harmonic cosine term, about **460–477 ppm** in corrected flux. Its conditional block-resampling coefficient SD is **186–209 ppm** for one-day blocks. Raw aperture flux has **535–575 ppm** with **347–405 ppm** SD. These are insufficiently decisive, share the same photons, and provide no second-epoch confirmation. This does not identify ellipsoidal variation, a binary, or a planet. Existing companion concerns remain.

## Exact scope and result

All QLP files had already been opened: 80387959 sectors **36, 37, 90, 100**; 241928959 sector **92**. Other opened sectors/products were not added to the declared comparison. The original fixed clocks are P=4.192168718052227 d / BTJD 1575.375831123655 / duration 0.092736 d and P=3.532592897546486 d / BTJD 3805.411656861608 / duration 0.032 d respectively. Periods and epochs were not optimized.

The following table reports the quadratic-baseline model. Errors are **one-day residual-block coefficient SDs**, not formal detection significances or calibrated confidence limits. The linear-baseline alternative and all four harmonic coefficients are preserved in [results.json](results.json).

| TIC | Sector | Aperture cos(4π phase), ppm | Corrected cos(4π phase), ppm |
|---|---:|---:|---:|
| 80387959 | 36 | −35 ± 70 | +45 ± 28 |
| 80387959 | 37 | −9 ± 52 | +12 ± 21 |
| 80387959 | 90 | −34 ± 57 | +41 ± 30 |
| 80387959 | 100 | +37 ± 43 | −13 ± 17 |
| 241928959 | 92 | +535 ± 347 | +460 ± 186 |

For 80387959 the fundamental coefficients also vary: e.g. aperture cosine changes from +317 ppm in sector36's linear model to −271 ppm in sector90's, while corrected counterparts are +53 and −1 ppm. This points to broad baseline/reduction sensitivity, not a stable physical orbital signal. A uniform null result cannot be claimed either.

For 241928959, the positive second-harmonic coefficient corresponds mathematically to brighter modeled flux near phases 0 and 0.5 relative to quadrature. No physical ellipsoidal template was fitted, and it must not be reported as an ellipsoidal-binary detection. Removing individual orbital-cycle groups gives corrected quadratic cosine coefficients **201–599 ppm**, retaining a positive sign but appreciable amplitude sensitivity. The phase plot shows uneven scatter and several large positive bins; no clipping or further tuning was introduced after inspection.

## Frozen procedure and limitations

[plan.json](plan.json) predates fitting and records existing input URLs, retrieval dates, hashes and exact seeds. Twenty declared models cover five sector files, aperture/corrected products, and degree-one/degree-two baselines. Native quality-zero finite positive samples were normalized by the median; points within 1.5 original durations of both primary and half-phase center were excluded **before** equal-weight 30-minute binning. Each contiguous segment separated by a gap >0.5 day has its own polynomial baseline, fitted simultaneously with the sine/cosine fundamental and second harmonic. No sliding high-pass filter was applied in this analysis.

The SAP series lacks an equivalent published SAP error array, so all models use equal-weight binned points. Uncertainties come from 200 circular residual-block draws at each of two declared lengths (0.5 and 1 day), separately within each continuous segment. Residual resampling assumes an approximately stationary residual process within each segment; deterministic systematics or longer correlations can violate that assumption. The two block sizes are sensitivity checks, not a calibrated noise model. Omission of each orbital-cycle group, including partial groups, is retrospective robustness testing rather than a holdout.

Corrections upstream in KSPSAP_FLUX (sectors36/37) and DET_FLUX (90/100/92) may attenuate or introduce orbital-scale features. SAP includes background and instrumental trends, which a polynomial need not remove. Consequently this comparison cannot set a reliable mass upper limit or reject all binaries. Source blending remains unresolved. Selection of targets and periods used these data, so neither null coefficients nor post-selected coefficients yield population probabilities.

## Verification and evidence

[diagnostic.png](diagnostic.png) was inspected. Its folded-bin error bars are display-only standard errors that ignore correlations; interpretation uses the block-sensitivity results. The coefficient panel makes the sector/reduction sensitivity explicit.

[verify.py](verify.py) independently reconstructs quality/phase masks and binned values from all five raw FITS files, verifies raw provenance and identity inputs, solves all 20 full fits and every orbit-omission fit with normal equations independently of the fitting script's SVD solver, and checks full rank and bootstrap covariance consistency. Maximum coefficient discrepancy is <5×10⁻¹⁷ relative flux. Each model's four separately injected 1000-ppm harmonics is recovered to <5×10⁻¹² ppm. That injection is an implementation/linear-model check **after pipeline processing**; it does not measure original QLP transfer, survey completeness or astrophysical validity.

```sh
OPENBLAS_NUM_THREADS=1 uv run python results/extension-80387959-241928959-20261012/verify.py
```

[verification.json](verification.json) records the checks. Scripts, design matrices, coefficients, omission outputs, injection checks and both block-length covariance matrices are retained. No new observations, spectra, catalog requests, TESS sectors or photometry were downloaded. No shared scientific code was modified; the completed search queues remain closed.
