# Checked results and evidence index

**Current assessment: 13 October 2026.** The frozen searches, six-candidate continuation and strongest-lead robustness tests are complete within their declared scopes. Six signals retain internal APC assessments; none is a securely attributed new planet. Use the [README](README.md) for the compact comparison and [GOAL.md](GOAL.md) before extending the work.

This index records conclusions and supporting reports. The machine-readable ledgers contain per-target accounting. An invalidated interpretation concerns a particular signal, not every possible planet around its star. Opened-sector lists below describe this investigation, not exhaustive archive coverage.

The [refereed-workflow comparison](results/refereed-vetting-20261012/ASSESSMENT.md) records the subsequent top-two noise and [neighbor-brightness audit](results/paper-host-vetting-20261012/ASSESSMENT.md). Principal nearby hosts remain possible; these conditional flux budgets are not measured neighbor eclipses or false-positive probabilities.

The subsequent [TRICERATOPS extension](results/triceratops-20261013/ASSESSMENT.md) uses one already-opened sector per priority candidate. All 17 planned calculations are complete. Million-draw target-planet weights are 92.43% and 97.68%, conditional on the modeled scenarios; neither meets the published joint validation thresholds. Numerical convergence and model completeness remain unresolved. The [independent review](results/triceratops-review-20261013/ASSESSMENT.md) checks the inputs and output arithmetic. Interrupted logs and exact provenance replays are retained. Completed search scopes remain closed; no new observing epochs were opened.

The new decisive-evidence goal includes a [five-site visibility screen](results/site-visibility-20261013/ASSESSMENT.md), [independent mount-limit review and access assessment](results/observing-access-20261013/ASSESSMENT.md), and [draft observation protocol](results/decisive-observation-protocol-20261013/ASSESSMENT.md). Three full sky passes for TIC 80387959 reduce to one marginal LCO one-meter track; none retains the conservative mount margin. TIC 402358350 has no complete window in the tested network. These are planning constraints, not evidence for a planetary or stellar companion.

[LCO archival images](results/lco-archive-metadata-20261013/ASSESSMENT.md) provide no transit test: all nine distinct science exposures precede the predicted event. Two inspected baseline frames saturate both TIC 80387959 and its principal neighbor TIC 80387965. They do not establish usable precision for these sources. Apparent TIC 402358350 spectral coverage is a misleading archive footprint; the inspected pointing is about 5.3° away. Both downloaded image frames are now inspected evidence, not fresh holdouts.

[ESO raw metadata](results/eso-raw-metadata-20261013/ASSESSMENT.md) returns no pointings within 120 arcseconds of either target; a known-source positive control succeeds. This extends the earlier processed-product search but does not cover every off-axis image. [CHEOPS metadata](results/cheops-metadata-20261013/ASSESSMENT.md) likewise returns no indexed visits within the tested pointing cones. No new flux was opened. The [remaining-evidence audit](results/remaining-evidence-audit-20261013/ASSESSMENT.md) distinguishes these bounded nonmatches from physical exclusions and identifies the subsequently checked SuperWASP route.

The [SuperWASP metadata screen](results/superwasp-metadata-20261013/ASSESSMENT.md) finds 12 sources near TIC 80387959, each with only six or seven points spanning about 37 minutes; the nearest record has seven. No source is returned within 120 arcseconds of TIC 402358350. API requests failed, while the official search interface completed; failures remain distinct from nonmatches. No flux was opened. [Early-epoch timing propagation](results/old-epoch-timing-20261013/ASSESSMENT.md) fails all 20 original gates at representative 2004–2009 dates, making narrow fixed-clock non-detections inconclusive.

[T17 geometry](results/t17-feasibility-20261013/ASSESSMENT.md) checks all 47 retained TIC 80387959 windows at the instrument’s own location. Only 28 March 2027 passes the unchanged sky requirements. A cardinal-interpolation horizon model permits it with 5.48° clearance; the true operator mask and mount/meridian constraints are unavailable. [Independent review](results/t17-review-20261013/ASSESSMENT.md) reproduces the geometry but does not establish access or precision. The [operator inquiry](results/t17-access-inquiry-20261013/ASSESSMENT.md) remains unsent.

## Unresolved signals worth further work

### TIC 80387959 — recurring signal, host uncertain

- [New resolved neighbor test](results/resolved-followup-803-20261013/ASSESSMENT.md): TIC 80387968 has 43 quality-selected SkyMapper measurements; two sample one predicted event without dimming. Same-depth flat-bottom eclipses are disfavored at those samples, but the two-event gate fails and color/shape/calibration limitations prevent host exclusion. These measurements are now opened evidence.

- [Refereed-method noise audit](results/paper-vetting-80387959-20261012/ASSESSMENT.md): all six depths remain positive; sector 100 becomes 582 ±133 ppm with approximate time-averaging inflation. Its worst event-omission depth/error ratio is 2.96; not a calibrated detection significance.

Frozen predictions recover dimming in sectors 90 and 100: 621 ± 98 and 651 ± 114 ppm. Source rankings vary across sectors and omitted events. Examined epochs include sectors 10, 36, 37, 63, 90 and 100; those data are not fresh holdouts.

- [Six-sector shape and baseline test](results/strongest-80387959-shape-20261012/ASSESSMENT.md): all sectors and event-omission fits retain a positive dip without additional global flattening. No coherent parity or exact-half secondary anomaly; isolated sector-36 asymmetry and older/newer depth differences remain. The [paired SPOC/QLP test](results/strongest-80387959-shape-20261012/paired-products/ASSESSMENT.md) finds no universal pipeline offset and documents common-quality sampling sensitivity.
- [Additional footprint audit](results/new-epochs-80387959-20261012/ASSESSMENT.md): sectors 64/99 cutouts were opened but both target apertures contain only collateral pixels. They are unusable target observations, not additional stellar epochs or transit non-detections.
- Timing: [later-sector measurements](results/followup-80387959-qlp90-100-20261009/heldout.json).
- Independent spectroscopy: [RAVE DR6 investigation](results/web-80387959-20261012/ASSESSMENT.md) securely matches one 2010 observation, RV 5.94 ± 0.87 km/s versus Gaia 7.02 ± 0.32 km/s (1.17 combined formal sigma). Predominantly normal morphology supports ordinary dwarf parameters for the bright star; no transit-host inference follows, and binaries remain possible. No useful GALAH target record found.
- [Orbital-modulation test](results/extension-80387959-241928959-20261012/ASSESSMENT.md): no stable substantial harmonic across the tested sectors/products; processing can suppress broad variation, so this does not exclude binaries.
- Source: [event stability](results/prf-80387959-event-stability-20261011/ASSESSMENT.md), [empirical-response feasibility](results/empirical-source-feasibility-20261012/ASSESSMENT.md). The blended scene's pointing response does not independently identify each star.

### TIC 402358350 — recurring signal, timing and host unresolved

- [New resolved neighbor test](results/resolved-followup-402-20261013/ASSESSMENT.md): TIC 74037550 has 836 retrieved ZTF measurements, 545 passing quality cuts. All 72 fixed-clock/time-convention/stream-or-filter comparisons are inconclusive. The failed TAP response and successful cloud retrieval are separate records; no neighbor clearance or probability update follows.

- [Refereed-method noise audit](results/paper-vetting-402358350-20261012/ASSESSMENT.md): all eight events remain positive across twelve methods; fixed-weight depths 590–659 ppm with approximate adjusted errors 41–93 ppm. Reweighted sensitivity 564–644 ppm is retained. Timing and host remain unresolved.

All listed sectors 40, 41, 54 and 81 are opened. Sector 81 gives 635 ± 72 ppm at the frozen prediction, but timing spread 0.09142 day exceeds the 0.072-day gate. Source fits retain poor residuals and alternative hosts. A conditional transit model fits without establishing a planet.

- [Raw-product local-baseline test](results/strongest-402358350-baselines-20261012/ASSESSMENT.md): all eight usable events remain positive in twelve SAP/PDC baseline variants, with combined depths 590–659 ppm. Adjacent intervals are much shallower. The gap event, unmatched controls and unfavorable SAP control remain recorded; no running-median filter, clock refit or new epoch was used.
- Timing: [training extension](results/expanded-402358350-20261011/ASSESSMENT.md), [sector 81 test](results/heldout-402358350-s81-20261011/ASSESSMENT.md).
- Source: [sector 54](results/prf-402358350-s54-20261011/ASSESSMENT.md), [sector 81](results/prf-402358350-s81-20261011/ASSESSMENT.md), [motion sensitivity](results/prf-motion-402358350-20261011/ASSESSMENT.md), [Gaia scene](results/gaia-402358350-scene-20261011/ASSESSMENT.md).
- [Published-pulsation nuisance and injection test](results/extension-402358350-5546257-20261012/ASSESSMENT.md): the simple sinusoid leaves the corrected-flux dip essentially unchanged, but sampling/detrending can transfer injected variation into box depths. It does not exclude all pulsation contamination.
- Physical checks: [aperture/corrected flux](results/sap-pdc-402358350-20261011/ASSESSMENT.md), [transit fits](results/physical-402358350-20261011/ASSESSMENT.md), [secondary checks in 40/41/54](results/secondary-sectors-402358350-20261011/ASSESSMENT.md) and [81](results/secondary-402358350-s81-20261012/ASSESSMENT.md), [telemetry](results/telemetry-402358350-20261011/ASSESSMENT.md). None excludes binaries or artifacts.
- External context: [catalogs/literature](results/novelty-402358350-20261011/ASSESSMENT.md), [coverage](results/external-coverage-402358350-20261011/ASSESSMENT.md). These earlier checks found no listed target match or securely associated target ZTF/Gaia light curve within their stated scope; neither result proves novelty or absence of a transit.

- [Further literature and neighbor photometry](results/web-402358350-20261012/ASSESSMENT.md): exact-source published pulsation at 1.05067 days for TIC 402358249 is reproduced in Gaia, but does not explain the 11.77-day signal. All four Gaia fixed-clock tests and all 48 ZTF clock/time-scale/stream combinations for TIC 1918682563 are inconclusive. Sparse Gaia sampling, clock uncertainty and large ZTF scatter prevent detection or exclusion of contamination. These neighbor observations are now opened data.

### TIC 241928959 — one epoch, companion concerns

Five events in sector 92 favor the target region, but no second epoch confirms recurrence. Physical fits trade high density against a grazing, larger companion. Gaia astrometric and multiple-image flags complicate the single-star interpretation; they do not identify a companion.

- Source and shape: [full-scene images](results/prf-fullscene-241928959-20261011/ASSESSMENT.md), [physical fits](results/physical-241928959-20261012/ASSESSMENT.md).
- Independent data: [sparse ZTF check](results/ztf-original-clocks-two-20261011/ASSESSMENT.md), [coverage audit](results/coverage-review-241928959-20261011/ASSESSMENT.md). Gaia epoch photometry is unavailable; ASAS-SN coverage remains unknown after service errors.
- [Further web/catalog review](results/web-241928959-20261012/ASSESSMENT.md): no new securely linked spectroscopy or companion measurement. SPYGLASS IV association, resolved-wide-binary and WDS nonmatches do not exclude isolated youth or a close companion.

- [Orbital-modulation test](results/extension-80387959-241928959-20261012/ASSESSMENT.md): weak one-sector second harmonic is sensitive to processing and orbital-cycle omission; not a binary identification.

### TIC 469309982 — mixed recurrence and secondary evidence

Sectors 9, 10, 36, 37, 63, 64 and 90 are opened. Only one of six retrospective season/window tests meets the timing and recovery conditions. The possible secondary is concentrated in one season. Host attribution remains uncertain.

- [New sector 90](results/new-epochs-469309982-96166003-20261012/ASSESSMENT.md): primary −54 ± 32 ppm, alternative refined clock 14 ± 34 ppm. Seed-reference positives are retained without replacing the primary; timing and expected sensitivity are insufficient for exclusion.
- Timing: [sector 64 follow-up](results/followup-469309982-20261011/ASSESSMENT.md), [sector 63](results/near-epoch-469309982-20261011/ASSESSMENT.md), [season-out tests](results/season-out-469309982-20261011/ASSESSMENT.md), [secondary by season](results/secondary-seasons-469309982-20261011/ASSESSMENT.md).
- Robustness: [source limitations](results/prf-motion-469309982-20261011/ASSESSMENT.md), [telemetry](results/telemetry-469309982-discovery-20261011/ASSESSMENT.md), [conditional reliability](results/reliability-469309982-20261012/ASSESSMENT.md). Zero flags in 40 draws per block model is not a survey false-alarm probability; one injection selects a competing epoch in one reduction.

- [Exact-source literature](results/extension-469309982-96166003-20261012/ASSESSMENT.md): the cluster-paper row reports Platais 8 membership probability 0.00, so that reference supplies no cluster age.

### TIC 96166003 — weak, timing-dependent recovery

All listed sectors 19, 43, 44, 59 and 86 are opened. Sector 19 is weak; sector 59 gives 265 ± 52 ppm at the expanded primary prediction but negative depths at three alternatives. All timing gates are inconclusive. Faint-neighbor ambiguity remains.

- [New sector 86](results/new-epochs-469309982-96166003-20261012/ASSESSMENT.md): primary 248 ± 101 ppm, alternative expanded clock 7 ± 134 ppm. All six comparisons remain timing-inconclusive; this is not a validated recurrence.
- Discovery and timing: [review](results/review-96166003-20261011/ASSESSMENT.md), [sector 19 extension](results/expanded-96166003-20261012/ASSESSMENT.md), [sector 59 test](results/heldout-96166003-s59-20261012/ASSESSMENT.md).
- Source: [difference images](results/source-check-96166003-20261011/ASSESSMENT.md), [faint-scene models](results/prf-96166003-20261012/ASSESSMENT.md).
- Robustness: [crossed clock/processing test](results/same-clock-96166003-20261012/ASSESSMENT.md), [conditional null controls](results/reliability-96166003-20261012/ASSESSMENT.md), [dated CTOI check](results/ctoi-96166003-20261012/ASSESSMENT.md). Processing agreement does not repair uncertain timing; selected-family controls do not calibrate original discovery selection or planet odds.

- [Exact-source literature](results/extension-469309982-96166003-20261012/ASSESSMENT.md): the planet-yield paper contains a simulated planet, not a previously observed one. Its entry cannot validate or invalidate the TESS signal.

### TIC 5546257 — contamination strengthened, exact clock unresolved

Sectors 9, 35, 36, 62, 89 and 99 are opened. The sector 62 frozen prediction gives 386 ± 30 ppm, but narrowly fails the timing-precision gate. Images favor known-binary neighbor TIC 5546242; its catalog orbit and tested harmonics do not explain the selected 1.76729-day train. The mismatch does not validate an on-target planet. Newly opened resolved-neighbor Gaia epochs now align with the refined TESS clock, so the catalog mismatch is not a veto on this contaminant.

- [New QLP sectors 89/99](results/new-epochs-5546257-20261012/ASSESSMENT.md): primary nominal-clock dips 271 ± 28 and 239 ± 33 ppm. Both fail the original timing-precision gate; all alternate clocks are retained. Different extraction methods/apertures prevent direct source or depth-evolution claims.
- [Resolved-neighbor Gaia test](results/extension-402358350-5546257-20261012/ASSESSMENT.md): all five nominal refined-clock in-window points dim, with a sixth nearby. The catalog model also explains most samples; a period alias is plausible. All saved timing alternatives remain in the report, and the backward timing gate still fails.

Earlier evidence: [follow-up](results/followup-5546257-20261011/ASSESSMENT.md), [localization](results/prf-motion-5546257-s62-20261011/ASSESSMENT.md), [telemetry](results/telemetry-5546257-20261011/ASSESSMENT.md), [Gaia identity](results/gaia-5546257-scene-20261011/ASSESSMENT.md), [contaminant-clock test](results/contaminant-clock-5546257-20261012/ASSESSMENT.md).

## Checks shared across candidates

- [Prospective observation planning](results/followup-planning-20261013/ASSESSMENT.md): 64 nominal event opportunities through April 2027. Preserved profiles permit provisional 5.6-hour tracks for 80387959, while 402358350 requires 17.5–18.5 hours and fails the timing gate. No site/instrument visibility or sensitivity is established; the [field diagrams](results/followup-overview-20261013/ASSESSMENT.md) use catalog coordinates, not new images.

- [Raw aperture-contrast controls](results/strongest-host-identifiability-20261012/ASSESSMENT.md): five of eight pass, with wrong-host results for Kepler-93. No candidate application. Geometry-only checks quantify close-source aperture overlap, not host probabilities.
- [ASAS-SN access review](results/strongest-external-access-20261012/ASSESSMENT.md): Ohio State’s coordinate form is reachable but includes an interactive CAPTCHA; Hawaii V2 remains unreachable here. No target coverage or flux was obtained, and no service failure is treated as a non-detection.

- [Event baselines and omissions](results/event-baseline-six-20261012/ASSESSMENT.md): all six checked primary dips remain positive with separate event baselines and each single-event omission; alternate clocks and weak later recovery remain unfavorable. Fifteen nominal comparisons retained, with no timing or source uncertainty removed.
- [Additional coverage](results/coverage-six-extension-20261012/ASSESSMENT.md): QLP 469309982/90, 96166003/86 and 5546257/89/99, plus non-QLP footprints for 80387959. The four new QLP epochs were tested under separate frozen plans; the 80387959 footprints proved unusable collateral pixels. Other metadata-only footprints remain untested: 96166003/71 and 5546257/8/63. Coverage alone is not recurrence.
- [Additional spectroscopy availability](results/extension-469309982-96166003-20261012/SPECTROSCOPY.md): bounded release-specific nonmatches for 469309982 and 96166003; not binary exclusions.

- [Gaia companion metadata](results/companion-constraints-shortlist-20261012/ASSESSMENT.md): exact identities and four non-single-star tables checked; no returned orbital solutions, not binary exclusion. TIC 241928959's elevated RUWE and 14% multiple-peak fraction are existing metadata, not a new detection.
- [Empirical-source feasibility](results/empirical-source-feasibility-20261012/ASSESSMENT.md): cached stamps predict combined-scene variation but do not calibrate individual source responses.
- [Pointing-correction controls](results/pointing-correction-controls-20261012/ASSESSMENT.md): repairs Kepler-93 host ranking; three of four cases pass. One contaminant sector retains its host but has a smaller discrimination gap, failing the frozen improvement rule. No candidate application; this does not rule out all correction methods.
- [Probability-model feasibility](results/probability-feasibility-20261011/ASSESSMENT.md): conditional astrophysical probabilities would not establish novelty or cover every instrumental explanation.

## Deprioritized or invalidated interpretations

| Signal / group | Assessment | Evidence |
|---|---|---|
| TIC 5540688 | All 15 image events favor neighbor 5540683. Its model-dependent ~3% dip favors an eclipsing source; unconfirmed. Sectors 35/36/62 unopened. | [Discovery](results/review-5540688-20261011/ASSESSMENT.md), [images](results/prf-5540688-20261011/ASSESSMENT.md), [Gaia](results/gaia-5540688-scene-20261011/ASSESSMENT.md), [neighbor depth](results/neighbor-depth-5540683-20261011/ASSESSMENT.md) |
| TIC 5546257 | Images favor binary neighbor 5546242; resolved Gaia dips now align with the refined TESS clock despite the catalog-period mismatch. Exact alias and dilution remain unresolved. | [Localization](results/prf-motion-5546257-s62-20261011/ASSESSMENT.md), [resolved Gaia epochs](results/extension-402358350-5546257-20261012/ASSESSMENT.md), [catalog period](results/gaia-5546257-scene-20261011/ASSESSMENT.md) |
| TIC 22972044, 30832104, 430216116, 322826591 | Images favor neighboring sources; their physical classifications remain incomplete. | [22972044](results/prf-22972044-20261011/ASSESSMENT.md), [30832104](results/review-30832104-20261011/ASSESSMENT.md), [430216116](results/prf-430216116-20261011/ASSESSMENT.md), [322826591](results/prf-322826591-20261011/ASSESSMENT.md) |
| TIC 399642075 | Likely eclipsing-neighbor contamination; close-source and dilution ambiguity remains. | [Source evidence](results/prf-399642075-20261011/ASSESSMENT.md) |
| TIC 267545898 | Broad morphology, mixed timing and inadequate image models; not promoted. | [Follow-up](results/followup-267545898-20261011/ASSESSMENT.md), [model limitations](results/prf-motion-267545898-20261011/ASSESSMENT.md) |
| TIC 362222987, 396160833 | Weak later recovery; shuffled controls frequently produce strong signals. | [362222987](results/null-362222987-20261011/ASSESSMENT.md), [396160833](results/null-396160833-20261011/ASSESSMENT.md) |
| TIC 159873548, 231968820, 138558387 and other ledger ROT matches | Known rotation plus morphology and processing concerns. Distinguish exact identities from nearby catalog matches. | [All original screening passes](results/solar-radius-lead-audit-20261011/audit.json) |
| TIC 236317267 | All 21 events and 18 registration tests favor neighbor 236317263, ~3.52 pixels away. Sectors 51/78 unopened. | [Source fits](results/prf-236317267-20261011/ASSESSMENT.md) · [Discovery](results/review-236317267-20261011/ASSESSMENT.md) |
| TIC 459244300 | Exact rotational-variable match; broad, processing-sensitive dip. Later sectors unopened. | [Review](results/review-459244300-20261011/ASSESSMENT.md) |
| TIC 284383833 | Exact rotational-variable match; broad minima and an edge event lost with alternate detrending. Sectors 51/78 unopened. | [Review](results/review-284383833-20261011/ASSESSMENT.md) |
| TIC 411696721 | Exact rotational-variable match; broad minima and a 2.365-fold depth change with detrending. Sectors 32/71 unopened. | [Review](results/review-411696721-20261011/ASSESSMENT.md) |
| TIC 369603533, 219495467, 443608653 | Broad, processing-sensitive variability. Reports distinguish exact from positional catalog associations. | [369603533](results/review-369603533-20261012/ASSESSMENT.md), [219495467](results/review-219495467-20261012/ASSESSMENT.md), [443608653](results/review-443608653-20261012/ASSESSMENT.md) |
| TIC 106583384 | All 20 events favor region 106583444/780959515. Close component unresolved; sectors 7/61 unopened. | [Source evidence](results/prf-106583384-20261012/ASSESSMENT.md) |
| TIC 43676101 | All 14 image events favor neighbor 43676071. Physical classification unresolved. | [Source checks](results/prf-43676101-20261012/ASSESSMENT.md) |
| TIC 313548505 | Broad feature strongly dependent on detrending; physical cause unknown. | [Review](results/review-313548505-20261011/ASSESSMENT.md) |
| TIC 196681132 | Identifiers and period match a published K2 eclipsing binary; not a novel planet. | [Identity and paper](results/vsx-single-signals-20261011/ASSESSMENT.md) |
| TIC 422626648 | Alternating depths and RV variability raise stellar-companion concerns; no convincing independent confirmation. | [Preserved evidence trail](README-HISTORY.md) |
| TIC 314649431, 25324731, 240023401, 378761120, 286607959 | On-target interpretations rejected after displaced images and deep neighboring eclipses. | [Representative case](results/qlp-378761120-expanded-20261010/ASSESSMENT.md), [full historical index](README-HISTORY.md) |
| Weak-seed local flags other than 469309982 | 22 of 23 flags deprioritized for known variability, inconsistent events, broad signals or noise. | [Every flag and linked review](results/weak-seed-audit-20261011/audit.json) |


## Coverage, negative results and errors

[Public spectroscopy availability](results/web-spectroscopy-20261012/ASSESSMENT.md): no ESO processed spectrum within 120 arcsec of the top three targets and no matching entry in the dated 5,105-star HARPS RVBank index. These archive-specific nonmatches are not binary exclusions or a census of all spectroscopy.

The [completion audit](results/scoped-completion-20261012/ASSESSMENT.md) reconciles the frozen search and initial vetting package. Subsequent checks are indexed above. These scopes overlap; do not sum them as unique stars.

- [Solar-radius ledger](results/solar-radius-lead-audit-20261011/audit.json): 7,004 attempts, 28 reviewed passes and one original error; retains dispositions and evidence hashes.
- [Weak-seed ledger](results/weak-seed-audit-20261011/audit.json): 689 attempts and 23 reviewed flags. TIC 88928641's reproduced raw-data failure is not a successful non-detection.
- [Fainter QLP expansion](results/qlp-faint-expanded-20261010/ASSESSMENT.md): 1,845 targets, recovery outcomes and 17 peak follow-ups.
- [Queue recovery](results/solar-radius-ranks3920-4432-20261011/ASSESSMENT.md): preserved reserved-data exception for TIC 5546257; no silent overwrite or duplicated search.
- [Archived journal](README-HISTORY.md): earlier pools and unsuccessful checks. Use current assessments when historical entries conflict.

## Controls and interpretation limits

| Check | Finding | Limit |
|---|---|---|
| [Kepler-93 images](results/prf-137151335-20261011/ASSESSMENT.md) | Original model can prefer the wrong host | Poor-fit rankings alone cannot establish or reject a planet |
| [Five known planets](results/solar-radius-positive-controls-20261011/ASSESSMENT.md) | Some pass; others are missed | Not survey completeness |
| [Shallow injections](results/solar-radius-shallow-injections-20261011/ASSESSMENT.md) | Limited sensitivity in selected examples | Not an all-star efficiency or exclusion |
| [TIC 5546257 telemetry](results/telemetry-5546257-20261011/ASSESSMENT.md) | One disturbed image event biases localization | Removing it does not remove the photometric dip |
| Independent arithmetic checks | Reproduce the stated model and measurements | Do not establish real-world model accuracy or planet probabilities |

## External leads already checked

[HD 32564](results/rv-hd32564-20261010/ASSESSMENT.md): HARPS signals replicated, with [activity](results/rv-hd32564-activity-20261010/ASSESSMENT.md) and alias concerns retained. External lead, not our discovery or confirmation. [User-post provenance](results/user-posts-20261010/NOTES.md).

[TIC 4206066 method review](results/rabtsevich-method-review-20261011/ASSESSMENT.md): incorporated season-out and future-data protocol lessons; no independent replication or validation claimed.
