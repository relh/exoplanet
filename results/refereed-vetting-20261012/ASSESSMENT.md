# Applying refereed candidate-vetting methods to our two strongest signals

**This is an internal research assessment, not a refereed paper or a planet validation.** We reviewed published candidate and validation workflows, mapped them to the preserved evidence, and added correlated-noise and contaminant-brightness tests for TIC 80387959 and TIC 402358350. Neither a favorable light-curve test nor completion of this checklist establishes a planetary host.

## Papers read and the methods adopted

The original full-text author manuscripts and publication metadata were retrieved from arXiv; URLs, UTC retrieval times and SHA-256 hashes are in [sources.json](sources.json). The journal references distinguish these papers from unreviewed social-media claims.

| Refereed study | Relevant procedure | Application here |
|---|---|---|
| [Giacalone et al. (2022), AJ 163, 99](https://doi.org/10.3847/1538-3881/ac4334), [author full text](https://arxiv.org/html/2201.12661), §§II–IV | Combine photometric diagnostics with high-resolution imaging, reconnaissance spectroscopy and resolved transit observations; model astrophysical false-positive scenarios | Audit the actual available constraints before interpreting statistical probabilities. Keep neighbors that have not been observationally excluded. |
| [Cacciapuoti et al. (2022), MNRAS 513, 102](https://doi.org/10.1093/mnras/stac652), [author full text](https://arxiv.org/html/2203.15826), §2 | Check whether neighboring stars are bright enough to explain the dip; inspect difference images, full light curves, parity and secondary signals | Apply brightness-budget sensitivity and retain unreliable centroids as unresolved, rather than treating a preferred image fit as a secure source. |
| [Eisner et al. (2021), Planet Hunters TESS II](https://doi.org/10.1093/mnras/staa3739), [author full text](https://arxiv.org/html/2011.13944), §§5–6 | Inspect spacecraft/background behavior, aperture and pixel dependence, neighboring sources and physical transit fits; obtain ground-based follow-up | Link the existing telemetry, aperture, physical and image tests, including their failures. Separate archive-limited checks from observations we do not have. |

The new noise analyses additionally follow the time-averaging rationale of Pont et al. (2006), with implementation-specific adaptations described in their reports. We use our own reproducible diagnostics, **not an execution of DAVE, LATTE, pyaneti or TRICERATOPS**. The papers use different thresholds and assumptions; their labels are not transferable certificates.

## Results of the added checks

**80387959:** the six sector depths remain positive, but noise-adjusted uncertainties rise to 113, 92, 105, 130, 92 and 133 ppm for sectors 10, 36, 37, 63, 90 and 100. Sector 100 is 582 ±133 ppm rather than ±99 ppm under the earlier conditional white-noise treatment. Its depth/error ratio falls from 5.86 to 4.37 and reaches 2.96 in one event-omission sensitivity case. This does not retroactively redefine the old frozen recovery test; it documents an additional weakness in treating that epoch alone as decisive.

**402358350:** all eight usable events remain positive. Across twelve methods, fixed-weight combined depths remain 590–659 ppm, with approximate noise-adjusted errors of 41–93 ppm. The illustrative linear ±3-duration corrected-flux result is 610 ±44 ppm; constant ±5-duration SAP changes from 602 ±41 to 602 ±93 ppm. Reweighting by the new errors yields 564–644 ppm, retained as a separate sensitivity calculation. Neither adjustment repairs the failed timing criterion.

**Neighbor brightness:** a fresh, explicitly conditional aperture-flux calculation shows why the source question remains important. TIC 80387965, 13.76 arcsec from 80387959, could reproduce the first signal with roughly a 1–2% eclipse under the tested throughput assumptions. For 402358350, TIC 1918682563 could do so with roughly a 21–29% eclipse. These are required eclipses under alternative models, not observed eclipses. Other close sources need very deep or nominally impossible eclipses, but catalog and throughput sensitivity prevents clearing the principal alternatives. All 10,548 source-sector cases are preserved without treating duplicate catalog entries as independent physical stars.

These noise methods differ: 80387959 compares post-fit residual averages with a simulated white reference for its exact weighted design; 402358350 uses out-of-event averages and the conventional finite-bin white expectation. Neither is a full stochastic noise model, and their beta factors should not be ranked as comparable reliability scores. Both retain insufficient-bin cases, input hashes and synthetic checks.

## Evidence and outstanding requirements

| Published-workflow step | TIC 80387959 | TIC 402358350 | Assessment |
|---|---|---|---|
| Recover the transit-like signal across observations | Six sectors; two earlier frozen-prediction recoveries | Eight usable events across four sectors | Recurrence supports further investigation; reanalysis of opened epochs is not a new holdout |
| Test flux extraction and baseline dependence | Joint local baselines; paired SPOC/QLP comparison | SAP and PDCSAP; twelve local-baseline variants | Dips survive; these reductions share photons |
| Check parity, secondary events and broad variability | No coherent parity/half-phase anomaly; existing harmonic checks | No convincing tested half-phase secondary; pulsation nuisance test inconclusive | No binary veto: eccentric/unequal eclipses and dilution remain possible; not an exhaustive new phase search |
| Model time-correlated residuals | New six-sector, event-preserving time-averaging audit | New 96-event-fit time-averaging audit | Conditional uncertainty sensitivity, not a survey false-alarm probability |
| Identify nearby stars capable of causing the dip | New SAP brightness-budget audit | New SAP brightness-budget audit | Actual aperture throughput and catalog reliability matter; conditional budgets do not identify a host |
| Locate the dimming source | Preferred image host changes with sector/event omission | Multiple alternatives and poor image fits | Unresolved; failed shallow-source controls cannot be bypassed |
| Check instrumental/background behavior | Existing pointing/empirical-image controls remain inadequate for attribution | Existing eight-event background/pointing audit has no common large excursion | No proof of instrumental cleanliness |
| Fit a physical transit and characterize the host | Existing conditional transit fit; RAVE dwarf-like spectrum | Existing circular target-host fits have density/impact degeneracy | Compatibility under an assumed host is not identification; no robust planet radius follows |
| Exclude close companions with high-resolution imaging | No validated contrast curve established | No validated contrast curve established | Not completed; a catalog nonmatch cannot substitute |
| Resolve the event with ground-based photometry | No source-resolved transit established | External sparse data and timing remain inconclusive | Not completed |
| Exclude a stellar companion spectroscopically | One RAVE velocity agrees with Gaia aggregate | No useful phase-resolved exclusion established | Not completed; one compatible velocity is insufficient |
| Compute astrophysical false-positive probabilities | Aperture/host assumptions remain unresolved | Aperture/host assumptions and variability remain unresolved | Not run; no invented FPP/NFPP or percentage |

Detailed new measurements: [80387959 noise](../paper-vetting-80387959-20261012/ASSESSMENT.md), [402358350 noise](../paper-vetting-402358350-20261012/ASSESSMENT.md), [neighbor flux budgets](../paper-host-vetting-20261012/ASSESSMENT.md).

Prior evidence: [803 shape](../strongest-80387959-shape-20261012/ASSESSMENT.md), [paired reductions](../strongest-80387959-shape-20261012/paired-products/ASSESSMENT.md), [402 baselines](../strongest-402358350-baselines-20261012/ASSESSMENT.md), [402 secondary](../secondary-sectors-402358350-20261011/ASSESSMENT.md), [402 telemetry](../telemetry-402358350-20261011/ASSESSMENT.md), [402 physical fit](../physical-402358350-20261011/ASSESSMENT.md), [803 spectroscopy](../web-80387959-20261012/ASSESSMENT.md), [failed localization controls](../strongest-host-identifiability-20261012/ASSESSMENT.md).

## Follow-up availability checked

Fresh public ExoFOP target pages for both TICs returned HTTP 200. Both show zero imaging, spectroscopy, time-series and file entries, and no TOI/community-candidate/planet-parameter entries. These are **public page inventory counts**, not statements that no observatory possesses data. The RAVE spectrum already found for 80387959 illustrates that important external archives are not equivalent to ExoFOP holdings. No follow-up images, spectra or new flux series were opened. [Request records and parsed tables](followup-metadata.json).

Neither catalog absence nor a clean diagnostic establishes novelty. Relevant published follow-up often uses telescope observations that cannot be generated by rerunning a script. The concrete missing observations are spatially resolved in-transit photometry, useful companion contrast curves, and repeated spectroscopy. For 402358350, reliable event timing must be established before attempting a decisive transit observation.

## Statistical interpretation and publication readiness

The [earlier probability feasibility review](../probability-feasibility-20261011/ASSESSMENT.md) remains applicable. TRICERATOPS compares a specified family of astrophysical scenarios; it does not supply an all-causes reliability or novelty probability. Instrumental effects, inadequate catalog scenes, aperture response errors and unmodeled variability can invalidate an apparently precise result. We have not discarded nearby sources based on failed spatial methods, fabricated contrast curves, or treated corrected-flux depth as automatically equal to aperture depth.

A publishable candidate assessment can preserve ambiguity. This report supports a candid methods/results narrative, but it does not claim that all checks in the papers were reproduced or that peer review would accept either candidate. A manuscript would also need explicit author responsibility, a reviewable data/code release policy, and a defensible discussion of selection effects; agent agreement is not a substitute for scientific review.

## Reproducibility and scope

Literature fetching and follow-up metadata queries are read-only. New experiment directories own their plans, inputs, analysis code, deterministic tests and independent verifiers. No original run is overwritten, shared scientific source changed, reserved sector opened, candidate submitted, or astronomer contacted. The experiments reuse previously inspected observations and preserve the existing clocks and host ambiguities.

The coordinator reran all three numerical verifiers and the document inventory verifier, and inspected the new figures. The complete `uv run pytest` suite passed **54 tests**. An initial combined test run exposed experiment modules both importing the name `run`; this was a Python module-name collision, not a scientific failure. Tests now load their own files under unique module names. The failure and correction are retained in [integration-verification.json](integration-verification.json).
