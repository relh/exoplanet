# TIC402358350: transit shape is compatible with an assumed target host

A circular, undiluted target-host transit can fit the already-opened40/41/54/81 data with physically ordinary stellar density. The shallow shape does **not** require the low density returned by the unconstrained fits: a broad stellar-density constraint gives nearly identical data chi-square. This supports compatibility only; it does not identify the host, exclude blended binaries or estimate planet probability. All-data timing and shape fits are retrospective and do not replace the preserved frozen sector81 result.

## Frozen experiment

[plan.json](plan.json) was saved before fitting. It specifies the expanded40/41/54 primary seed, both1.5/2.5d preprocessing windows, fixed quadratic limb coefficients(0.4,0.2), circular orbit, no dilution, assumed target host, exposure integration and the existing bounded three-start fitter. All four sectors were previously opened; no observations were downloaded.

The hashed TIC catalog row gives mass1.138±0.156 solar masses and radius0.9949±0.0457 solar radii. These imply nominal density about1.63g/cm³ and scaled axis22.85 at the seed period. They are catalog estimates, not validated stellar parameters. The broad prior is Gaussian in log(a/R*) with sigma0.15, centered on22.85. At fixed period this corresponds to log-density sigma0.45, intentionally broader than nominal propagated catalog errors. It is an illustrative physical constraint, not a probabilistic population model.

| Detrending | Axis constraint | Radius ratio | a/R* | Impact | Duration(d) | Circular density(g/cm³) | Data chi-square/dof |
|---|---|---|---|---|---|---|---|
|1.5d|None|0.02656|12.62|0.830|0.17964|0.274|1972.395/1888|
|1.5d|Broad prior|0.02334|21.42|0.129|0.17764|1.342|1972.451/1888|
|2.5d|None|0.02717|11.18|0.874|0.18139|0.191|1880.083/1816|
|2.5d|Broad prior|0.02355|22.96|0.156|0.16513|1.653|1879.331/1816|

There are eight retained event windows, each with a separately profiled intercept and slope. The degrees of freedom subtract five transit parameters and sixteen baseline parameters. Formal errors use beta1 and do not model correlated noise. The prior-conditioned radius ratios correspond roughly to2.5 Earth radii **only if the signal is undiluted and on the named star**; source uncertainty makes this unsuitable as a measured planet radius.

## Degeneracy and convergence limits

All four selected optimizer runs report success and no active numerical bound, but these flags do not establish the global optimum. The2.5d constrained fit has a lower **data** chi-square than the unconstrained run, demonstrating that the latter stopped at an inferior local solution. Its three start objectives are1896.97,1880.18,1880.08; the constrained starts give1896.97,1879.33,1879.68 including prior penalties. Different starts and density assumptions favor very different impact parameters with closely similar flux fits. Do not interpret the unconstrained low-density optimum as a stellar-density discrepancy or a binary diagnosis.

No posterior sampling, credible intervals, eccentricity, dilution, limb-darkening uncertainty, correlated-noise model, multistar fit or false-positive comparison was performed. Fixed limb coefficients are generic rather than derived from an atmosphere model. These assumptions limit the physical inference. A broader optimization alone would not settle the dominant host ambiguity.

## Verification

[verify.py](verify.py) checks raw/input hashes and reconstructs both preprocessing reductions. It calls batman directly with the saved parameters, independently solves each event's baseline using weighted least squares, and reproduces data chi-square and prior penalties. This reuses the same transit library, so it is an independent arithmetic/baseline check, not independently implemented transit physics or proof of optimizer convergence. [verification.json](verification.json) records reduced chi-square1.035–1.045. [fits.png](fits.png) was visually inspected; orange points include each cadence's exposure integration and black points are binned local-baseline-corrected flux. Both density families fit the shallow dip similarly.

Reproduce with `uv run python results/physical-402358350-20261011/verify.py`. The run script refuses to overwrite its frozen plan. No shared scientific code changed.
