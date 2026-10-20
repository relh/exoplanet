# Cached-stamp empirical response: no-go for independent host attribution

The cached stamps support prediction of the **combined scene's** response to recorded pointing, but do not independently identify each star's response. This bounded feasibility test therefore does **not** proceed to candidate host fits. It neither resolves nor rejects the80387959 or402358350 signals. No new data were downloaded and no candidate-event flux comparison, response tuning on events, PRF ranking or candidate probability was performed.

A narrower future nuisance-correction experiment may be useful, because pointing predicts much out-of-event variation. It would require known-planet and contaminant controls before application to these candidates; the numerical improvement below is not that validation.

## Frozen diagnostic

[plan.json](plan.json) was written before measurement. It allowlists the existing five80387959 and four402358350 stamps through their prior download/model manifests and hashes, and preserves their unchanged frozen clocks. For each supplied clock, observations within the larger of0.5day or three durations were excluded.402358350 uses the union of original and expanded-clock exclusions. This deliberately broad mask is a selected precaution, not a formal timing confidence envelope or assurance that every unknown astrophysical variation is masked.

Quality-zero finite times outside those masks were divided into alternating2-day blocks anchored at the sector's first finite time. One parity trained the response and the other was held out. Each pixel was modeled by an intercept plus the two recorded POS_CORR components, standardized only using training data. The comparator is its constant training mean. No split, basis or coefficient choice was tuned to improve the test result. These are disjoint out-of-event predictive checks, not new independent transit observations.

| Target | Sector | Pointing1 1–99% span, pixels | Pointing2 span, pixels | Held-out RMS / constant-model RMS |
|---|---:|---:|---:|---:|
|80387959|36|0.0314|0.1129|0.177|
|80387959|37|0.0364|0.0365|0.191|
|80387959|63|0.0300|0.0386|0.548|
|80387959|90|unavailable: placeholder|unavailable|not fitted|
|80387959|100|unavailable: placeholder|unavailable|not fitted|
|402358350|40|0.1049|0.1282|0.082|
|402358350|41|0.0849|0.1327|0.065|
|402358350|54|0.0405|0.0518|0.136|
|402358350|81|0.0658|0.0795|0.144|

All usable regression designs have rank3 and condition numbers1.02–6.04 after standardization. Approximately94.9–100% of held-out pointing vectors fall inside the training bounding box. Each fit includes all121 finite stamp pixels. The metric is **unweighted aggregate pixel RMS**, without per-pixel uncertainty normalization; bright-star/systematic variation can dominate it. It does not show that residuals meet photon-noise expectations or that shallow event-depth systematics are small. Interleaved blocks share the same detector and astrophysical scene; long correlations and state extrapolation remain limitations. Zero POS_CORR columns for90/100 are unavailable information, not evidence of stable pointing.

## Why this is not an independently calibrated source response

For non-event images, the scene is a sum of constant star fluxes times shifted source responses. Learning its mean and two pointing derivatives constrains that **sum**, not each source's response separately. With independently unknown source templates, an arbitrary small pattern added to one template and subtracted from another with the appropriate flux ratio leaves the combined image unchanged. Small positive normalized examples are constructed in verify.py. The linear operator for a common shift preserves the same ambiguity; therefore more precise regression coefficients do not by themselves identify the variable source's template.

The measured subpixel motions provide useful derivative information but limited independent subpixel sampling. A common, spatially constrained PSF/kernel and known catalog scene could impose enough extra assumptions to address some degeneracy. This assessment does **not** prove that every such deconvolution or empirical-PSF method must fail. It establishes that this simple cached-stamp combined-scene regression has not supplied that calibration. Close blends, incomplete catalogs, uncertain flux ratios and intrinsic variability would still need to be modeled and tested. Data-derived centroid proxies from the same blended flux would add further coupling and were deliberately not substituted for missing independent pointing.

The existing [80387959 gradient analysis](../prf-80387959-motion-sensitivity-20261011/ASSESSMENT.md) used mission-derived gradients and improved fit without resolving the host. This run instead learned an aggregate non-event response and measured its held-out predictiveness; it did not repeat that event-ranking exercise. The [402358350 source81 result](../prf-402358350-s81-20261011/ASSESSMENT.md) likewise retains poor residuals despite favorable target ranks.

## Decision and finite next gate

**No-go:** do not infer candidate hosts or launch another independent-source PRF comparison from the learned coefficients. The planned feasibility stage is complete with an explicit limitation.

**Conditional, separate experiment only:** a frozen non-event-trained pointing correction could be tested for preservation of known astrophysical signals. Before either candidate's events are evaluated, use cached [Kepler-93](../prf-137151335-20261011/ASSESSMENT.md), where the old model demonstrably confused the host, and a spatially obvious contaminant such as [106583384](../prf-106583384-20261012/ASSESSMENT.md). Prespecify training masks/splits, event-depth preservation and source-discrimination criteria; include off-event injections, background alternatives and stability across epochs. Controls must assess real response mismatch rather than only inject the exact fitted template. If depth preservation or true host discrimination fails, stop. Passing these controls would justify only the tested correction's use, not a general calibrated host probability.

Those control experiments were **not** performed here because the requested bounded feasibility assessment reaches its independent-response limitation first. This is a possible new method-development package, not a mandatory infinite sequence of additional candidate fits. Genuinely resolved photometry, independently calibrated wider-field response, or physical companion constraints would be more direct new evidence if available.

## Reproducibility

`run.py`, `plan.json`, `results.json` and the seven cached non-event design/coefficient arrays preserve the experiment. Existing source manifests retain raw pixel URLs; plan/model and raw pixel hashes are checked. `verify.py` reconstructs excluded-event masks using nearest-cycle arithmetic, train/test membership and pointing values, then independently reproduces847 pixel fits with QR and all seven held-out RMS metrics. It checks all nine raw stamp hashes and seven input-manifest/clock hashes. The illustrative null-direction check initially used a perturbation too large to keep both templates positive; [the failure and correction](initial-verification-failure.json) are preserved, and the corrected small positive example passes. No raw regression result changed.

[verification.json](verification.json) establishes arithmetic/provenance only. No new observing sector, telescope data download, scientific source change, shared-document edit or external communication occurred. The candidate interpretation remains unchanged.
