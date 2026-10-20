# Feasibility of numerical planet probabilities

No probability was computed. The current user preference is an established categorical rating system; this report preserves a future path to defensible numerical estimates. Internal dispositions must not be mistaken for official catalog assignments. A percentage of being an **undiscovered planet** is not supplied by an astrophysical false-positive package.

## What TRICERATOPS could answer

TRICERATOPS compares astrophysical transit/eclipsing scenarios. Its published validation scheme uses both false-positive probability (FPP) and nearby false-positive probability (NFPP); those criteria were evaluated on TOIs and do not automatically validate our weaker exploratory signals. [Original paper](https://arxiv.org/abs/2002.00691).

The inspected v1.1.0 implementation defines `1-FPP` as the sum of TP, PTP and DTP: planet scenarios on the target, including dilution alternatives. NFPP sums scenarios on resolved nearby stars, including nearby planets. Thus NFPP is not simply a probability of “no planet anywhere.” An any-host planet probability would require explicitly summing the relevant planet rows. The implemented scenario family is astrophysical; its normalization does not include a general instrumental-artifact or stochastic-variable-star alternative. This is why an apparently precise output can remain misleading for our signals. The constructor also queries catalogs and downloads sector cutouts, so constructing a target is not a read-only local operation. Degenerate likelihood warnings must be treated as failed computation, not confident classification. [Pinned implementation](https://raw.githubusercontent.com/stevengiacalone/triceratops/v1.1.0/triceratops/triceratops.py).

Our inference: neither scenario sum estimates novelty. Establishing “previously unknown” still requires dated exact-identity, ephemeris, literature and candidate-catalog checks; catalog absence supplies no calibrated novelty prior. Do not multiply a guessed novelty fraction by `1-FPP`.

## Available target inputs and unresolved constraints

Catalog values below are starting inputs, not independent stellar characterization. The three cached TIC neighbor tables and their SHA-256 hashes are in [provenance.json](provenance.json); that file includes the recorded parameter uncertainties.

| Target | TIC mass / radius (solar units), temperature | Available evidence and missing discriminating inputs |
|---|---|---|
| 80387959 | 0.89 / 0.7965, 5220 K | Repeated 4.19217-day dimming and five sector image stacks, but preferred host changes between target and neighbors. Need aperture/dilution reconstruction and host-specific stellar alternatives; no calibrated image likelihood is available. [Host evidence](../prf-80387959-event-stability-20261011/ASSESSMENT.md). Gaia catalog RV diagnostics do not yield an orbital exclusion or secure host. [RV context](../rv-context-80387959-20261011/ASSESSMENT.md). |
| 241928959 | 0.6277 / 0.6507, 3396 K | Five-event source stack favors target region, but independent epoch confirmation and close-binary exclusion remain absent. Photometric youth is tentative and can change stellar-model priors. Secondary non-detection is not a binary exclusion or calibrated limit. [Images](../prf-fullscene-241928959-20261011/ASSESSMENT.md), [youth](../spyglass-241928959-20261011/ASSESSMENT.md), [secondary](../secondary-241928959-20261011/ASSESSMENT.md). |
| 469309982 | 0.95 / 0.8794, 5445 K | Six sectors already inspected; ~2.8905-day dimming has uncertain extrapolated timing, possible secondary, source ambiguity and instrumental concerns. Folding only a favorable timing alternative would hide uncertainty. [Follow-up](../followup-469309982-20261011/ASSESSMENT.md), [retrospective seasons](../season-out-469309982-20261011/ASSESSMENT.md). |

No validated high-resolution contrast curve or phase-resolved spectroscopic binary exclusion was established in the reviewed evidence. Their absence does not prevent an exploratory package run, but broadens unresolved alternatives. A complete target-plus-neighbor input audit is still needed: stellar parameters/errors, exact apertures by sector, flux convention, exposure times, detrending, timing aliases and correlated noise. Do not remove a neighbor just because our inadequate PRF model ranked it poorly.

The API accepts centered transit photometry, normalized flux, uncertainty, period, exposure time and optional imaging/companion constraints. Its simple Gaussian aperture model is an additional modeling assumption. Defaults must not silently substitute two-minute integration for lower-cadence observations. [API documentation](https://triceratops.readthedocs.io/en/latest/user/api.html).

## Version and execution constraints

The current official release inspected is v1.1.0. It changes dilution treatment: corrected photometry is the default; raw SAP requires the appropriate uncorrected setting. It also changes the default background population from TRILEGAL to Gaia DR3. Results therefore depend on pinned version and explicit conventions; older hosted tutorials are not sufficient specifications. [Official release](https://github.com/stevengiacalone/triceratops/releases/tag/v1.1.0).

The local Python is 3.12.11; TRICERATOPS, vespa, lightkurve, astroquery and numba are absent. **Do not install v1.1.0 into the active campaign environment.** On Python 3.12 its requirements include NumPy<2, SciPy<1.14 and setuptools<81, conflicting with this repository's NumPy>=2, SciPy>=1.14 and setuptools>=84. An isolated environment with a pinned dependency lock is necessary; installation and runtime compatibility have not been tested. [Pinned package requirements](https://raw.githubusercontent.com/stevengiacalone/triceratops/v1.1.0/setup.py), [local project](../../pyproject.toml).

A historical official example reports minutes per calculation and repeats Monte Carlo evaluations to assess numerical scatter. That is not a runtime estimate for these crowded fields. [Official tutorial](https://triceratops.readthedocs.io/en/latest/tutorials/example.html). Budget initially for one serial control run, measure actual memory/runtime, then decide concurrency around the active search queue.

## Concrete next experiment, if numerical estimates are pursued

1. Freeze definitions: conditional target-planet scenario weight, any-host planet weight, NFPP and novelty status as separate outputs. Retain categorical uncertainty when the model omits a credible explanation.
2. Create an isolated pinned environment and reproduce a documented example plus our known-planet/contaminant controls. Preserve failure outputs; do not tune inputs to meet a threshold.
3. Assemble a reviewed input manifest from already-opened observations. Explicitly allowlist sectors before any package constructor/network call; audit aperture coordinates, dilution and exposure time. Preserve raw source hashes and catalog snapshots.
4. Run the full applicable scenario family with repeated deterministic seeds, increasing draws until numerical stability is demonstrated. Save scenario tables, log-evidences, warning/degeneracy status and fitted shapes, not only FPP.
5. Repeat defensible alternative stellar, timing, noise and dilution assumptions. Do not present Monte Carlo scatter as total uncertainty. Instrumental reliability needs a separate validated treatment; these package outputs alone cannot supply it.
6. Report any surviving numbers as model-conditional estimates with uncertainty and limitations. Retain all unfavorable fits and do not automatically promote a low-FPP signal or claim discovery.

This assessment used local files and primary software/paper sources only. No package was installed, target photometry downloaded, source algorithm changed or probability inferred. External response hashes and failed documentation routes are recorded in provenance; raw web responses were not retained, so hashes identify retrievals rather than provide a complete offline source archive.
