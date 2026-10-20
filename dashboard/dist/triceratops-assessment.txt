# Exploratory TRICERATOPS analysis

**The bounded exploratory calculation is complete. Neither candidate is validated; both retain their previous unresolved assessments.** This experiment applies TRICERATOPS 1.1.0 to one previously examined TESS sector for each of our two strongest signals. The resulting scenario weights are conditional on the package's astrophysical models. They are not calibrated probabilities that these signals are real planets, and they do not establish novelty.

<!-- RESULTS -->
## Results

| Target | Target-primary planet weight | FPP | NFPP | Any-host planet weight |
|---|---:|---:|---:|---:|
| TIC 80387959 | 92.43% | 7.57% | 4.29% | 94.99% |
| TIC 402358350 | 97.68% | 2.32% | 0.40% | 99.08% |

These are **single-seed, million-draw, model-conditional weights**. They do not estimate the probability that a candidate is real or previously unknown. Numerical convergence remains unestablished because the bounded experiment does not repeat the million-draw calculation.

For TIC 80387959, three 100,000-draw seeds give target-primary planet weights of 92.23–92.80% and NFPP of 4.27–4.55%.
The million-draw target-primary estimate differs from the smaller-run median by +0.09 percentage points.
Largest alternative scenarios: TIC 80387959 STP (2.50%); TIC 80387965 NEB (2.27%); TIC 80387968 NEB (1.26%); TIC 80387959 BEB (0.57%).

For TIC 402358350, three 100,000-draw seeds give target-primary planet weights of 97.36–97.80% and NFPP of 0.38–0.42%.
The million-draw target-primary estimate differs from the smaller-run median by +0.11 percentage points.
Largest alternative scenarios: TIC 402358350 STP (1.35%); TIC 402358350 SEB (0.38%); TIC 402358249 NEB (0.13%); TIC 74037550 NEB (0.11%).

Neither candidate meets the original joint numerical validation thresholds (FPP < 1.5% and NFPP < 0.1%) in the million-draw calculation. Their prior signal, timing and source-attribution limitations remain in force.

### Sensitivity and diagnostic controls

| Input | Noise multiplier | Target-primary planet weight | FPP | NFPP |
|---|---:|---:|---:|---:|
| TIC 80387959 / none | 1.5 | 92.58% | 7.42% | 4.10% |
| TIC 80387959 / none | 2 | 91.98% | 8.02% | 4.23% |
| TIC 80387959 / flat | 1 | 44.15% | 55.85% | 24.52% |
| TIC 80387959 / inverted | 1 | 41.99% | 58.01% | 25.39% |
| TIC 402358350 / none | 1.5 | 95.87% | 4.13% | 0.99% |
| TIC 402358350 / none | 2 | 93.74% | 6.26% | 1.77% |
| TIC 402358350 / flat | 1 | 23.38% | 76.62% | 39.08% |
| TIC 402358350 / inverted | 1 | 15.91% | 84.09% | 44.12% |
| Kepler-93 b / sector 40 | 1 | 82.88% | 17.12% | 5.77% |

With TIC 80387959's flux set to a constant 1 (no dimming), the model assigns 44.15% to target-primary planets and 81.40% to planets on any modeled host. The scenario family excludes a general no-signal/artifact alternative, so these weights cannot measure whether a detected planet is real.

With TIC 402358350's flux set to a constant 1 (no dimming), the model assigns 23.38% to target-primary planets and 62.98% to planets on any modeled host. The scenario family excludes a general no-signal/artifact alternative, so these weights cannot measure whether a detected planet is real.

The restricted Kepler-93 b control does not meet the original validation thresholds. Its known planetary status comes from additional published evidence, not this single-sector calculation. This experiment therefore does not reproduce that published validation or calibrate candidate reliability.

Each sensitivity/control calculation uses 100,000 draws and seed 13. Flat and inverted tests retain the observed-depth neighbor eligibility and the supplied period; they test behavior when a candidate is forced into the astrophysical scenario family, not a false-alarm rate. No control output is a calibrated reliability estimate.

[Machine-readable results and adopted run list](summary.json). All scenario tables and warnings are retained alongside the individual run summaries.
<!-- END RESULTS -->

## Inputs and scope

| Target | Sector | Period | Flux | Exposure |
|---|---:|---:|---|---:|
| TIC 80387959 | 36 | 4.192168718052227 d | Native SPOC SAP | Approximately 10 min |
| TIC 402358350 | 54 | 11.769544332077816 d | Native SPOC SAP | Approximately 10 min |

The selections were fixed in [plan.json](plan.json) before probability calculations. Sector 36 is the first previously examined 10-minute sector for 80387959; sector 54 has existing source and physical-model assessments for 402358350. These are representative single-sector calculations, not a joint likelihood for all observations. The original clocks and event-coverage selections remain unchanged. The other sectors, successful timing recoveries, failed timing gates, and host-localization limitations are not encoded in these numerical weights.

The input light curves reuse the saved native-SAP joint box/event-baseline fits from the [neighbor brightness audit](../paper-host-vetting-20261012/ASSESSMENT.md). Only the fitted event intercepts and slopes are removed; the dip remains. Flux is normalized by the mean fitted baseline. All retained samples within three durations on each side are used, without binning. The scalar uncertainty is the out-of-transit residual standard deviation; separate runs multiply it by 1.5 and 2. This does not model time-correlated noise or propagate uncertainty/covariance in baseline fitting.

Both `calc_depths` and `calc_probs` use `dilution_corrected=False`. The aperture is the original SPOC bit-2 mask, with catalog positions projected through its saved celestial WCS. Both aperture pixels and stellar positions use the same zero-based coordinate system. Exposure time is the native median cadence, with 20 integration samples per exposure. No contrast curve or companion-exclusion constraint is supplied.

The package constructor was bypassed solely to avoid automatic image downloads. Its state is initialized from the local catalog and aperture products; the package's depth and probability routines are unchanged. No additional TESS observations were opened. Gaia DR3 mean catalog photometry supplies the default 0.1-square-degree background population; these are catalog measurements, not newly opened epoch photometry. The transformed field populations actually used and independent repeated raw TAP responses are separately hashed.

## Catalog accounting

Every cached source within 150 arcsec enters the aperture model. Exact duplicated catalog identities are counted once: a removed row must be explicitly flagged `DUPLICATE` and have an included counterpart with identical coordinates, T magnitude and Gaia identifier. One row is removed for 80387959, 21 for 402358350. [Correction plan](catalog-correction-plan.json). Split or uncertain sources without this evidence remain included. Original catalogs, prepared inputs and preliminary calculations are retained in [original-catalog](original-catalog/); their outputs are superseded rather than silently discarded.

TRICERATOPS estimates missing mass, radius and effective temperature from catalog photometry. Evolved sources with missing masses receive the package's nominal one-solar-mass assumption. These estimates and flags are preserved in the per-target stellar tables. Stellar parameters are held fixed in each calculation; their uncertainty is not represented by seed-to-seed scatter.

The package models each source with a circular Gaussian PSF of width 0.75 pixel. It considers a resolved neighbor eligible if the modeled aperture contribution could produce the observed decrement with an eclipse no deeper than 100%. This is a model-dependent eligibility test, not an observed exclusion. The prior brightness audit deliberately retained uncertainty in aperture response; a neighbor rejected by this nominal calculation is not thereby physically ruled out.

## Numerical checks

All applicable target, unresolved-companion, background and eligible-neighbor scenario families are retained, including binary alternatives at twice the proposed period. No scenario is manually suppressed. Full scenario parameters, log evidences, normalized weights, warnings, run times and errors are saved for each run.

The original [convergence criterion](convergence-plan.json) required three independent million-draw runs, agreement across seeds and agreement with 100,000-draw estimates within two percentage points. A [bounded amendment](bounded-amendment.json), based on measured runtime, instead schedules three 100,000-draw seeds and one million-draw seed per candidate. Consequently this experiment cannot establish the original numerical convergence requirement. Report the actual seed ranges and draw-count changes; do not call these confidence intervals.

A known-planet control uses already examined Kepler-93 b / TIC 137151335 sector 40 at its unchanged clock, with the same native-SAP baseline and aperture conventions. [Control plan](control-plan.json). It omits the additional published observations that established that planet, so it is a check of this restricted configuration, not a reproduction of its published validation. Flat and inverted candidate light curves provide additional computational diagnostics. None constitutes population calibration.

## Interpretation

- **Target-planet weight:** TP + PTP + DTP, equal to 1 − FPP. These scenarios place the planet around the target primary, with different dilution assumptions.
- **FPP:** all alternatives to those target-primary planet scenarios. It includes some planet-on-another-star explanations; it does not mean “no planet anywhere.”
- **NFPP:** all scenarios on resolved neighboring stars, including neighboring planets.
- **Any-host planet weight:** TP + PTP + STP + DTP + BTP + NTP. This is a sum within the specified model family, not a probability that the detected signal is astrophysically real.

The model family lacks a general instrumental-artifact or stochastic stellar-variability explanation. It normalizes its modeled scenarios even for a light curve that does not contain a credible transit. A large planet weight can therefore coexist with unresolved signal reliability, timing, detrending or source-identification problems. No percentage from this experiment should be labeled “chance that we found an undiscovered planet.”

The original TRICERATOPS paper requires both FPP < 1.5% and NFPP < 0.1% for its statistical-validation category. Its “likely planet” category also requires NFPP < 0.1%, together with FPP < 50%. These thresholds were assessed on TOIs under that study’s workflow; they do not automatically transfer to this exploratory single-sector configuration. Numerical threshold comparisons are reported separately from our requirements for trustworthy timing, source identification and signal reliability. [Original paper](https://arxiv.org/abs/2002.00691).

## Reproduction and provenance

Use the isolated environment recorded in [environment.txt](environment.txt); it is intentionally separate from the scientific repository environment because dependency requirements conflict. Preparation, correction, run, scheduling, replay and summary scripts are retained here. Raw downloads and the isolated environment are under ignored `data/triceratops-20261013/`. Existing raw TESS products remain at their original cache paths, with source sidecars and hashes in the frozen plans.

Primary software sources: [v1.1.0 source](https://github.com/stevengiacalone/triceratops/tree/v1.1.0), [method paper](https://arxiv.org/abs/2002.00691). These results use the 1.1.0 Gaia-background and dilution conventions, which differ from older examples.

The background population uses the release's Gaia photometry and main-sequence relations, with solar metallicity. It excludes catalog rows that cannot be characterized and does not establish completeness for unresolved or extremely faint stars. The saved raw responses contain 5,720 and 41,601 catalog rows; 5,577 and 34,434, respectively, enter the usable background populations. Offline reconstruction gives a one-to-one match after allowing approximately 0.000012 numerical differences from TAP CSV versus the package's table serialization. The initial overly strict comparison and its failure log are retained; the scientific population inputs were not changed to pass this check. [Verification](gaia-verification.json).

## Reboot recovery

The analysis machine rebooted after thirteen of the seventeen bounded runs had completed. No local calculation survived, and the saved dispatch scripts contain no remote execution mechanism. The completed TIC 80387959 million-draw run was retained. TIC 402358350's million-draw and doubled-noise runs were interrupted before writing a result; their partial logs are preserved in `reboot-interrupted/`. The two remaining TIC 402358350 diagnostic controls had not started.

The [recovery manifest](reboot-resumption.json) hashes the retained artifacts before resumption. The replacement scheduler runs one probability calculation at a time with two Numba threads and one BLAS thread. It also completes the three already-planned TIC 80387959 100,000-draw provenance replays: the earlier corrected-catalog outputs lacked contemporaneous per-run input hashes, so they are retained in `provenance-replay/` and compared with the hash-recorded replacements. No scientific inputs, clocks, scenario families or completed research goals were changed by recovery. [Replay comparison](replay-verification.json).
