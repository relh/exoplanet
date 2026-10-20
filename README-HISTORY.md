# Archived investigation notes

Snapshot preserved before the README was reorganized on 2026-10-11. These chronological entries include superseded assessments; use [README.md](README.md) for current priorities. Evidence links remain relative to the repository root.

# Exoplanet search

## Candidate findings — updated 2026-10-11

**No confirmed discovery or securely attributed new planet candidate yet.**

**TIC5546257 — new unresolved transit-like lead:** 303-ppm dips every1.7671 days in discovery data; a frozen prediction using three early sectors gives386 ±30 ppm in later sector62 (formal SNR12.85). Timing uncertainty narrowly fails the strict recovery rule. A nearby known eclipsing binary has a different period; an initial sector35 difference-image centroid is offset by1.56 pixels from the bright source, and source modeling is in progress. This is not yet an established new planet. [Discovery review](results/review-5546257-20261011/ASSESSMENT.md) · [Frozen follow-up](results/followup-5546257-20261011/ASSESSMENT.md). Both aperture and corrected discovery flux retain280–310 ppm dimming, but source-plus-motion image fits remain inadequate and cannot identify the host. [Image-model limitations](results/prf-motion-5546257-20261011/ASSESSMENT.md) · [Flux robustness](results/sap-pdc-5546257-20261011/ASSESSMENT.md). Removing one pointing-disturbed image event improves sector35 localization and favors the nearby known binary; its period mismatch remains unexplained, while the cleaned light-curve dip is unchanged. [Telemetry/source sensitivity](results/telemetry-5546257-20261011/ASSESSMENT.md).

**4,432 distinct original solar-radius attempts audited:** the latest512 targets yield four screening passes—two known rotational variables, one broad processing-sensitive feature, and the unresolved TIC5546257 lead above. [Batch evidence](results/solar-radius-ranks3920-4432-20261011/ASSESSMENT.md) · [Complete pass ledger](results/solar-radius-lead-audit-20261011/ASSESSMENT.md).

**Source-vetting limitation:** known Kepler-93 b favors the target in one sector and a neighbor in another under the same image model. Poor-residual source rankings cannot serve as standalone planet vetoes. Earlier ambiguous leads remain unresolved, with their separate photometric concerns retained. [Known-planet control](results/prf-137151335-20261011/ASSESSMENT.md).

**TIC22972044 — new screening pass, contamination favored:** 582-ppm dips every2.1498days pass the initial gates, but both discovery-sector stacks favor fainter neighbor **TIC22972048**. Its physical variability remains unclassified; this is not a likely new on-target planet. [Discovery evidence](results/review-22972044-20261011/ASSESSMENT.md) · [Source fits and limitations](results/prf-22972044-20261011/ASSESSMENT.md).

**Weak-signal extension completed all689 attempts:** 688 measured, one preserved raw-data error and23 reviewed local flags. Twenty-two are deprioritized; TIC469309982 remains unresolved. [Accounting](results/weak-seed-audit-20261011/ASSESSMENT.md) · [Final batch](results/weak-seed-ranks512-689-20261011/ASSESSMENT.md).

**TIC469309982 — unresolved:** sector64 reaches SNR5.1 among nine timing alternatives saved beforehand (nominal SNR2.9). The selected clock then gives SNR2.9 in previously unopened sector63, below independent-recovery criteria. The central dip pattern is retained, but timing, source attribution and a possible secondary remain unresolved. [Sector64](results/followup-469309982-20261011/ASSESSMENT.md) · [Subsequent sector63 test](results/near-epoch-469309982-20261011/ASSESSMENT.md). Its later-sector dip appears in both aperture and corrected flux, but aperture evidence is sensitive to background/pointing events; corrected flux retains the dip when those cycles are omitted. These are post-selection checks, not independent confirmation. [Flux comparison](results/sap-pdc-469309982-20261011/ASSESSMENT.md) · [Telemetry and omissions](results/telemetry-469309982-20261011/ASSESSMENT.md).

**Added-sector leads now deprioritized:** TIC160163644 and TIC394877426 match known rotational variables and fail variability/event-consistency checks. TIC306680120 shows broad oscillations with a preferred period near one-third of its proposed orbit. None of the three local-search flags is currently a likely planet candidate; their reserved sectors remain unopened. [Vetting and catalog evidence](results/weak-seed-review-20261011/ASSESSMENT.md) · [All eight pilot outcomes](results/weak-seed-pilot-20261011/ASSESSMENT.md).

**Added-data control:** more sectors strengthen known TOI-1435 b from formal SNR about 6 to 11, but the frozen reserved-sector check remains inconclusive. This supports testing weak seeds without establishing a new discovery or completeness rate. [Control evidence](results/added-sectors-control-153976959-20261011/ASSESSMENT.md).

**TIC 30832104 — new screening pass, contamination favored:** 652-ppm dips every 9.71 days pass the initial gates, but both sector-9 image events favor fainter neighboring **TIC 30832145**. The neighbor's physical variability remains unclassified; this is not a new on-target planet candidate. [Discovery, catalog and source evidence](results/review-30832104-20261011/ASSESSMENT.md).

**TIC 430216116 — now deprioritized as an on-target planet lead:** image fits across all three discovery sectors, all 15 individual events and all 15 event-omission stacks favor neighboring **TIC 430216137**. Its 4.67-day variability remains physically unclassified; the earlier on-target Earth-size estimate is unsupported. The favorable shuffle controls and inconclusive later-sector check are retained. [Source evidence and limitations](results/prf-430216116-20261011/ASSESSMENT.md).

**TIC 267545898 — now deprioritized as a likely on-target planet:** local image fits offer little support for target-centered dimming after allowing pointing-related structure. The models remain imperfect, so the cause is unresolved. A strong later-sector dip exists among broad timing alternatives, but the nominal prediction fails and the exploratory search fails the original correlated-noise gate. [Image-model evidence](results/prf-motion-267545898-20261011/ASSESSMENT.md) · [Mixed follow-up](results/followup-267545898-20261011/ASSESSMENT.md).

**TIC 399642075 — likely contamination:** its 2.28867-day dimming favors the nearby known eclipsing-binary region in both discovery sectors. Two close neighbors remain difficult to separate, and the full dilution/amplitude explanation is unresolved. [Image and catalog evidence](results/prf-399642075-20261011/ASSESSMENT.md).

**New screening pass TIC138558387 matches a known rotational variable.** Its13.20-day feature is broad and changes depth strongly with detrending; exact TIC/Gaia identity is verified. It is deprioritized as a new-planet lead. [Catalog and light-curve evidence](results/review-138558387-20261011/ASSESSMENT.md).

**TIC396160833 is now deprioritized:**17/48 shuffled discovery curves matched or exceeded its peak strength, adding to background concerns and unsuccessful later-epoch checks. The physical cause remains unresolved. [Conditional null test](results/null-396160833-20261011/ASSESSMENT.md).

**TIC362222987 is now deprioritized:**46/48 shuffled discovery light curves produced stronger maximum dip-search peaks. Together with failed later-epoch recovery, this weakens the lead further; it remains physically unresolved. [Conditional null test and limits](results/null-362222987-20261011/ASSESSMENT.md).

**Known-planet controls:** the unchanged pipeline fully passes Kepler-93 b and TOI-5159 b at roughly 200–230 ppm. Three other preselected planets fail or remain below threshold; a stronger planet in one of those systems is recovered separately. These are known-planet checks, not discoveries or a completeness estimate. [All five outcomes and residual searches](results/solar-radius-positive-controls-20261011/ASSESSMENT.md).

**Completed frozen ranks 2896–3407:** 512 stars, 336 below threshold, 176 flagged, zero passes and zero errors. **3,408 distinct original target attempts are now audited**; the next frozen batch is running. [Batch evidence](results/solar-radius-ranks2896-3408-20261011/ASSESSMENT.md).

**Completed frozen ranks3408–3919:** 512 stars,332 below threshold,179 flagged, one off-target screening pass and zero errors. **3,920 distinct original attempts are audited**; the next batch is running. [Batch evidence](results/solar-radius-ranks3408-3920-20261011/ASSESSMENT.md).

**Completed-lead audit:** all eleven passing signals among the first 3,920 solar-radius target attempts have evidence-linked reviews; none is currently a securely attributed new planet candidate. [Complete ledger and review priorities](results/solar-radius-lead-audit-20261011/ASSESSMENT.md).

**Completed frozen ranks 2384–2895:** 512 terminal attempts: 314 below threshold, 196 flagged, one contamination-suspect lead and one processing error. The error was separately recovered on its two valid sectors, with no passing signal. **2,896 distinct target attempts are audited**; the next batch is running. [Batch and recovery details](results/solar-radius-ranks2384-2896-20261011/ASSESSMENT.md).

**Completed frozen ranks 1872–2383:** 512 targets, 335 below threshold, 176 flagged, one screening lead and zero errors; 1,233 training products audited before follow-up. This brought the expanded campaign to **2,384 completed targets** at that stage. The queue is searching the next frozen batch. [Batch evidence](results/solar-radius-ranks1872-2384-20261011/ASSESSMENT.md).

**Completed frozen ranks 1360–1871:** 512 targets, 318 below threshold, 191 flagged, 3 screening passes and zero errors; 1,245 training files audited before any reserved-sector follow-up. This brought the expanded campaign to **1,872 completed targets** at that stage. [Results](results/solar-radius-ranks1360-1872-20261011/ASSESSMENT.md). A two-worker queue was launched for the subsequent 5,132 frozen targets in 11 batches; the latest completed count is above. These are running/planned searches, not completed results. [Queue plan](results/solar-radius-remaining-queue-20261011/ASSESSMENT.md).

Current unresolved signals and the main reason each remains unconfirmed:

| Signal | Current evidence | Remaining obstacle |
|---|---|---|
| **TIC80387959 — 4.19217 days** | Recurs in independent TESS sectors. | Competing stars fit different sectors/events; the host remains uncertain. [Host stability](results/prf-80387959-event-stability-20261011/ASSESSMENT.md) |
| **TIC241928959 — about3.533 days** | Five events; pixel fits favor the target region. | No independent observing-epoch confirmation; close companion/binary explanations remain. [Source fit](results/prf-fullscene-241928959-20261011/ASSESSMENT.md) · [Independent check](results/ztf-original-clocks-two-20261011/ASSESSMENT.md) |
| **TIC362222987 — about8.924 days** | Discovery dip appears in aperture and corrected flux. | Deprioritized: no convincing recovery in sectors20/85, plus background and shuffle-test concerns. [Follow-up](results/near-epoch-362222987-20261011/ASSESSMENT.md) |
| **TIC396160833 — about13.500 days** | Discovery dip appears in aperture and corrected flux. | Deprioritized: no convincing later recovery, plus background and shuffle-test concerns. [Follow-up](results/near-epoch-396160833-20261011/ASSESSMENT.md) |

**Deprioritized:** TIC422626648 has alternating depths and strong RV variability consistent with a stellar-companion concern; TIC196681132 is a published eclipsing-binary recovery; TIC120689141 and TIC423928109 have strong known-variability explanations. Detailed evidence and negative results follow below.

**Sensitivity limit:** in three selected quiet stars, the full pipeline recovered3/18 injected100-ppm signals and11/18 at300ppm. No100-ppm probes were recovered at4.73 or13.13days. All15 missed100-ppm probes remain below local SNR7 even at their exact injected times, pointing to limited signal-to-noise in these examples. These are small-sample diagnostics, not survey completeness; non-detections do not exclude shallow planets. [Design and results](results/solar-radius-shallow-injections-20261011/ASSESSMENT.md) · [Missed-signal diagnosis](results/solar-radius-shallow-diagnosis-20261011/ASSESSMENT.md). A one-star pilot adding two sectors improved some signals but left gaps at the longest injected period; no additional100-ppm configuration reached SNR7. [Added-sector pilot](results/longer-baseline-sensitivity-9626063-20261011/ASSESSMENT.md).

**Independent-epoch checks weaken TIC362222987:** no nominal dip in reserved sector85 (SNR−2.14) or nearer sector20 (−0.04). The strongest match across150 saved timing alternatives is only0.98 in sector20. Timing/model uncertainty prevents a complete exclusion; no independent confirmation is established. [Sector85](results/followup-362222987-20261011/ASSESSMENT.md) · [Sector20](results/near-epoch-362222987-20261011/ASSESSMENT.md).

**Completed frozen ranks848–1359:**512 targets,296 below threshold,216 flagged,0 errors and0 passing signals. The audit checked1,241 training files and unopened reserved sectors. This brought the expanded campaign to1,360 completed targets at that stage. [Run and limitations](results/solar-radius-ranks848-1360-20261011/ASSESSMENT.md). Manual review retains the rejection of the strong TIC291471120 signal because of broad, inconsistent dips and processing-dependent depth. [Review](results/rejected-291471120-20261011/ASSESSMENT.md).

**Processing check — TIC362222987’s dip appears in both aperture and corrected flux.** This is shared-photon evidence, not independent confirmation. Its discovery-only timing uncertainty grows too large for a simple long-baseline non-detection to be decisive. [Flux comparison](results/sap-pdc-362222987-20261011/ASSESSMENT.md) · [Frozen clock](results/refinement-362222987-20261011/ASSESSMENT.md).

**New instrumental concern — TIC362222987’s strongest dip coincides with substantial background variation.** No consistent centroid displacement was found; the signal remains unresolved after the later-epoch checks above. [Telemetry checks](results/telemetry-362222987-20261011/ASSESSMENT.md).

**Literature correction — TIC120689141 is KIC5774694, with a published 12.1 ± 1.0-day stellar rotation period.** This agrees with our12.153-day signal and its broad shape; it is removed from new-planet priority. [Exact identity, literature and caveats](results/review-120689141-20261011/ASSESSMENT.md).

**New unresolved lead — TIC362222987:** an 8.928-day, 199-ppm dip passes discovery screening in sectors17–18 (conditional on-target size ≈1.56 Earth radii). Competing periods and unequal event depths limit confidence; later-epoch checks above have not confirmed it, and source attribution remains unchecked. [Discovery evidence and caveats](results/review-362222987-20261011/ASSESSMENT.md).

**New screening lead TIC423928109 matches a cataloged rotational variable.** Its 9.934-day, 571-ppm feature passes the automated gates, but its broad shape and strong sinusoidal variability weaken a transit interpretation. Exact TIC/Gaia identity is verified; it is removed from new-planet priority. [Evidence](results/review-423928109-20261011/ASSESSMENT.md).

**Known-variable recovery — TIC196681132 is EPIC212601505, previously listed as an eclipsing binary in a 2018 K2 paper.** Exact 2MASS and UCAC identifiers match; the published0.724453-day period and2.10% depth closely match our measurements. It is removed from new-planet priority. TIC241928959 and TIC422626648 remain unresolved signals, with no convincing independent confirmation. [Catalog identity, primary paper and verification](results/vsx-single-signals-20261011/ASSESSMENT.md).

**Completed the next512 solar-radius targets:**255 below threshold,254 flagged,3 screening leads,0 errors. Two leads have strong stellar-variability explanations; TIC362222987 remains unresolved. All1,238 training products and the unopened reserved sectors passed the terminal audit. The expanded campaign now totals848 targets. [Run and limitations](results/solar-radius-next512-20261011/ASSESSMENT.md).

Latest instrumental diagnostic: **TIC396160833’s four discovery dips coincide with curved background rises.** This adds an instrumental concern, without proving causation; no consistent centroid offset was established. [Diagnostics and limitations](results/telemetry-396160833-20261011/ASSESSMENT.md).

Latest processing check: **TIC396160833’s discovery dip is present in aperture and corrected flux**, with a processing-dependent depth. This is shared-photon evidence, not independent confirmation, and does not override the unsuccessful later-epoch checks. [Comparison and limits](results/sap-pdc-396160833-20261011/ASSESSMENT.md).

Latest follow-up: **TIC396160833 shows no convincing recovery in nearer sector25 either**: nominal SNR0.008; maximum over the frozen profile pairs2.23. Timing uncertainty still prevents decisive exclusion, but this adds negative evidence. [Predesign, measurements and limits](results/near-epoch-396160833-20261011/ASSESSMENT.md).

**Catalog correction — TIC34576133 is BW Ari, a known rotational variable with a listed9.57-day period.** Exact TIC identity is verified; it is removed from new-planet priority. [Identity evidence](results/solar-radius-next256-vsx-20261011/ASSESSMENT.md).

Latest independent-epoch check: **TIC396160833 remains unresolved.** Its nominal reserved-sector dip is insignificant, but a2.56-day prediction spread makes the test inconclusive. BW Ari’s test is likewise timing-inconclusive. [Frozen predictions and verification](results/solar-radius-next256-followup-20261011/ASSESSMENT.md).

**Historical discovery-stage signals — TIC396160833 and TIC34576133:** fitted periods13.495 and9.364days, depths164 and752ppm. Both pass screening, but the first needs spacecraft-systematics checks and the second has broad dips with surrounding variability. Neither was a credible new planet candidate at discovery; the follow-up and catalog correction above supersede this initial assessment. [Plots and caveats](results/solar-radius-next256-review-20261011/ASSESSMENT.md).

Completed256-star batch:127 below threshold,127 flagged,2 follow-up signals and0 errors;607 discovery products verified. [Batch audit](results/solar-radius-next256-20261011/ASSESSMENT.md).

Completed search extension: **64 additional solar-radius stars yielded24 below-threshold results,40 flagged signals and0 eligible candidates or errors.** All156 discovery products were audited; reserved sectors remain unopened. The expanded pool now has80 stars searched. [Results and limits](results/solar-radius-next64-20261011/ASSESSMENT.md).

Latest recovery controls: **36 injections across three pilot stars produced15 full-screen recoveries, all in the two stars with weaker baseline peaks; the strongly variable star recovered none.** These synthetic detections are not candidates or survey completeness. [Grid, failures and audit](results/solar-radius-stratified-injections-20261011/ASSESSMENT.md).

Completed expanded-radius pilot: **16 stars searched across44 discovery products;4 below threshold,12 flagged,0 eligible signals and0 errors.** Later sectors remain unopened. A12-injection check in one variable pilot star yielded no full-screen recoveries, so sensitivity needs further assessment. [Recovery limits](results/solar-radius-pilot-injections-20261011/ASSESSMENT.md). [Results and audit](results/solar-radius-pilot-20261011/ASSESSMENT.md) · [Frozen selection](results/solar-radius-pilot-selection-20261011/ASSESSMENT.md).

New search scope: **16,581 nearby stars with catalog radii0.81–1.10solar have earlier/later sectors in the cached TESS-SPOC inventory.** This metadata pool extends the search; known-object screening, product verification and photometric tests are still pending. These are not candidate signals. [Complete query and inventory audit](results/nearby-solar-radius-inventory-20261011/ASSESSMENT.md).

Latest secondary-eclipse check: **TIC241928959 has no convincing half-phase dip** in two durations and two detrending windows (maximum formal SNR1.07). This does not exclude a binary or confirm a planet. [Measurements and limits](results/secondary-241928959-20261011/ASSESSMENT.md).

**Binary-suspect signal — TIC422626648:** alternating QLP dips are about0.93% and0.54% deep, consistent across two detrending windows and with the raw-image amplitude pattern. Together with Gaia RV variability, this strengthens an eclipsing-binary interpretation near8.19days and deprioritizes it as a planet lead. It is not a confirmed binary orbit. [Measurements and limitations](results/parity-422626648-20261011/ASSESSMENT.md).

Latest repeatability check: **TIC422626648 is favored in all six individual event images, both chronological halves, and every event-removal stack.** The preference survives removing the event with the known background offset. Binary interpretation and independent confirmation remain unresolved. [Event fits and verification](results/prf-events-422626648-20261011/ASSESSMENT.md).

Latest source fit: **TIC422626648 is favored over12 tested neighbors in the stacked pixel-response fit**, including all17 alignment perturbations. This supports target-region attribution; the Gaia radial-velocity binary concern and lack of independent confirmation remain. [Fits, controls and limitations](results/prf-422626648-s91-20261011/ASSESSMENT.md).

Latest variable-catalog check: **Neither remaining single-sector signal has an ASAS-SN catalog entry within60arcsec.** This supplies no photometric confirmation or binary exclusion; both remain unresolved. [Scope and verified responses](results/asassn-remaining-signals-20261011/ASSESSMENT.md).

Latest stellar-context check: **TIC241928959 has a SPYGLASS I photometric youth probability of0.40 and no assigned cluster.** The exact catalog identity is verified; this does not establish youth or validate its dips. [Catalog values, definitions and limits](results/spyglass-241928959-20261011/ASSESSMENT.md).

The dated investigation entries below preserve earlier evidence; this catalog identification supersedes their new-candidate interpretation for TIC196681132.

Latest independent checks: **TIC241928959 and TIC422626648 show no convincing combined ZTF dip at their nominal TESS clocks**. Only five and three measurements fall inside those windows; timing uncertainty prevents exclusion. TIC196681132’s stronger photometric recovery is now identified with a previously reported variable. [Measurements and limits](results/ztf-original-clocks-two-20261011/ASSESSMENT.md).

Latest catalog check: **Gaia provides no non-single-star solution for the63 checked scene sources**, which does not exclude binaries. TIC196681132 also has discrepant older-TIC and Gaia distance estimates, so its stellar radius and inferred companion size need caution. [Verified queries and stellar context](results/gaia-nss-single-signals-20261011/ASSESSMENT.md).

Latest physical check — **TIC196681132’s ZTF odd dips are deeper than its even dips**, but the difference is weak after accounting descriptively for excess scatter. No convincing halfway eclipse appears at the tested duration. The independent-photometry agreement remains promising, with a binary explanation unresolved. [Diagnostics and verification](results/ztf-binary-196681132-20261011/ASSESSMENT.md).

**Historical photometric lead, now a known-variable recovery — TIC196681132:** unmodified ZTF data show roughly2.1% dimming at the original0.724472-day TESS clock, with similar depths in early/later observations and all three filters. The signal survives event-removal and timestamp-sensitivity checks. This post-inspection agreement merits follow-up, but binary explanations remain unresolved. [Independent-photometry evidence and caveats](results/ztf-original-clock-196681132-20261011/ASSESSMENT.md).

Latest independent search: **TIC196681132’s strongest early-ZTF peak does not convincingly repeat in later reserved data** (formal SNR1.17). Added-signal controls recover a different timing solution, which remains a follow-up clue rather than an observed confirmation. [Split design, results and limitations](results/ztf-search-196681132-20261011/ASSESSMENT.md).

Latest timing check: **the retrieved ZTF data do not provide a clean frozen-window confirmation**. Only104 observations pass the conditional timing gate; two nominal TIC196681132 in-window points become ambiguous across the prediction range. No confirmation or exclusion is claimed. [Timing assumptions, controls and coverage](results/ztf-timing-20261011/ASSESSMENT.md).

Latest ZTF audit: **all ten retrieved source positions favor the intended Gaia targets**, and no same-filter near-duplicate timestamps were found among1903 quality-screened measurements. Blends, timing conventions and coverage discrepancies remain unresolved; no independent transit recovery yet. [Association and duplicate checks](results/ztf-association-20261011/ASSESSMENT.md).

Latest independent-data progress: **ZTF cloud retrieval succeeded for all ten records near the three unresolved targets**, yielding2134 measurements (1903 quality-zero, finite measurements). Timing, source association and catalog-count discrepancies still need review; no ground-based transit recovery is claimed. [Retrieved data and audit](results/ztf-cloud-20261011/ASSESSMENT.md).

Latest independent-data check: **ZTF catalog records exist near all three unresolved targets**, but requests for their light curves still timed out. A separate cloud catalog is reachable for the next retrieval attempt; no ground-based transit recovery is claimed. [Catalog evidence and failures](results/ztf-catalog-route-20261011/ASSESSMENT.md).

Latest binary check: **TIC241928959’s alternating depths are statistically similar, but only one usable odd event remains**. The comparison cannot exclude an eclipsing binary; missing event-scatter uncertainty is recorded explicitly. [Measurements and limits](results/parity-241928959-20261011/ASSESSMENT.md).

Latest model check: **TIC241928959 remains preferred when the fuller67-source scene is fitted successfully with an alternative solver**. Synthetic solver checks pass, and all17 tested alignment shifts retain the target preference. The earlier failure is preserved; unresolved companions and independent confirmation remain outstanding. [Recovery and limitations](results/prf-fullscene-241928959-20261011/ASSESSMENT.md).

Latest source fit: **TIC241928959 is favored over its known close neighbor in all five event images** and all17 tested alignment shifts. A fuller crowded-scene fit failed; the successful brighter-source model and controls remain conditional. Binary explanations and independent confirmation are unresolved. [Evidence and preserved failure](results/prf-241928959-s92-20261011/ASSESSMENT.md).

Latest repeatability check: **TIC196681132 is favored over the known neighbor in21 of22 event images**, both chronological halves and every leave-one-event-out stack. The disagreeing event has large image residuals and remains recorded. This supports target-region attribution but does not exclude a binary. [Event fits, controls and verification](results/prf-events-196681132-20261011/ASSESSMENT.md).

Latest source fit: **TIC196681132 is favored over the eclipse alternative involving its known neighbor by the stacked image-response fit**, including all17 tested alignment shifts. Synthetic controls pass, but model residuals, unresolved companions and the lack of an independent epoch keep the signal unconfirmed. [Fits, controls and limits](results/prf-196681132-s91-20261011/ASSESSMENT.md).

Latest checks: **ZTF queries timed out for all three signals**, yielding no independent observations. TIC196681132’s image moments depend on the measurement window, so they cannot securely exclude its neighbor. [Localization limits](results/localization-stability-196681132-20261011/ASSESSMENT.md) · [Recorded download failures](results/ztf-single-signals-20261011/ASSESSMENT.md).

Latest blend check: **TIC196681132 has a catalog neighbor capable of reproducing the fitted depth in a simple dilution model**, requiring about81% eclipse depth at equal aperture throughput. Images favor the target region, but host attribution remains unresolved. [Assumptions and verified calculations](results/blend-budget-single-signals-20261011/ASSESSMENT.md).

Independent-data check: **the three TESS clocks are too uncertain for narrow-window exclusions a year earlier** under the existing conditional timing estimates. ZTF downloads subsequently timed out; no recovery is claimed. [Timing limits and request status](results/ztf-single-signals-20261011/ASSESSMENT.md).

Latest coverage check: **TESScut returns no additional image epoch for the three unresolved target-region signals**. The subsequent ground-based ZTF queries timed out; no independent recovery is claimed. [Verified coverage and next checks](results/ffi-coverage-single-signals-20261011/ASSESSMENT.md).

Latest binary diagnostic: **TIC196681132’s alternating dips differ only weakly**—about0.3percentage points, roughly twice the event-scatter uncertainty. This neither establishes nor excludes a binary. [Fixed-clock comparison and limits](results/parity-196681132-20261011/ASSESSMENT.md).

Latest binary check: **TIC422626648 has Gaia radial-velocity variability indicators and a29.7km/s reported range**, raising a stellar-companion or spectral-blend concern. Its cool template limits interpretation, and no velocity-period match is available. The other two unresolved targets lack these diagnostics. [Identity checks and limitations](results/rv-context-single-signals-20261011/ASSESSMENT.md).

Latest source check: **TIC196681132 has recurring target-region dimming near0.725days** in raw images, with background changes in several events. Its2.174-day fit shares observations and appears to be a triple-period alias. Binary and blend explanations remain unresolved. [Image and catalog evidence](results/qlp-faint-midradius-single-review-20261011/196681132-peak0/ASSESSMENT.md).

Latest source check: **TIC157940461 is weakened**. Its three raw event images show changing positive/negative residuals near a bright neighbor, without a secure target transit. [Images and limitations](results/qlp-faint-midradius-single-review-20261011/157940461-peak0/ASSESSMENT.md).

Latest source check: **TIC241928959’s roughly3.535-day dips recur near the target in five raw images**, but a neighbor half a pixel away remains a viable eclipsing-source alternative. Catalog nonmatches do not settle the interpretation. [Images, blend calculation and limits](results/qlp-faint-midradius-single-review-20261011/241928959-peak0/ASSESSMENT.md).

New unresolved signal: **TIC422626648 shows roughly4.096-day dips near the target region in six raw event images**. A competing5.456-day fit shares the data; close blends, binary explanations and a background offset remain unresolved. No independent observing epoch is available. [Initial review and limitations](results/qlp-faint-midradius-single-review-20261011/422626648-peak0/ASSESSMENT.md).

Completed search: **1461 single-sector targets:1270 below threshold,176 flagged,15 unusable**. Six fits across four stars have initial plot reviews and require further source checks; none is a credible new planet candidate yet. [Terminal reconciliation and pending work](results/qlp-faint-midradius-single-remaining-20261011/ASSESSMENT.md).

Latest pilot: **16 single-sector stars yielded no eligible candidates** (13 below threshold,3 flagged). Controls recovered no Earth-radius injections; larger signals were easier to recover. This pool lacks an independent reserved epoch, and1461 frozen targets remain. [Results, controls and limitations](results/qlp-faint-midradius-single-pilot-20261011/ASSESSMENT.md).

Latest search: **all nine stars with newly identified alternate epochs screened below threshold** in their frozen discovery data (strongest fitted dip SNR3.78–5.61). Reserved epochs remain unopened; no candidate qualified for follow-up. [Design, verification and limits](results/alternate-epochs-nine-20261011/ASSESSMENT.md).

New search scope: **nine previously unused stars have additional observing epochs in SPOC products**, found by auditing1885 targets. No light curves were opened during that metadata audit; the discovery search above is now complete. Three include a short special observation requiring separate coverage checks. [Metadata evidence and target list](results/unused-other-products-20261011/ASSESSMENT.md).

Latest recovery: **TIC139343242 is below threshold in its two usable discovery sectors** (strongest fitted dip SNR6.13). The unusable sector and original failure are preserved; its reserved sector remains unopened. [Recovery and verification](results/recovery-139343242-20261011/ASSESSMENT.md).

Latest completed search: **123 additional targets yielded no eligible candidates** (102 below threshold,17 flagged,4 unusable). Together with the pilot, all139 frozen targets have been attempted. One multi-sector failure was subsequently recovered below threshold (above). [Results and input audit](results/qlp-faint-midradius-near-reserved-remaining-20261011/ASSESSMENT.md).

Latest pilot: **16 stars with closely spaced reserved sectors produced no eligible candidates** (15 below threshold, one flagged). None of six Earth-radius injections recovered; larger injections performed better, so this does not exclude small planets. The123 remaining targets have now been attempted (above). [Results, sensitivity and verification](results/qlp-faint-midradius-near-reserved-pilot-20261011/ASSESSMENT.md).

Latest completed search: **2,810 targets, with 2,458 below threshold, 338 flagged and 14 unusable light curves**. All 11 eligible fits have initial plot reviews; all 11 reserved-sector timing tests are inconclusive. All 11 initial source inspections are complete; none establishes a credible new planet candidate. No securely attributed new planet yet. [Verified terminal results](results/qlp-faint-midradius-one-reserved-remaining-20261011/checkpoint-2810-verification.json).

Latest search: the **5,716-target search has finished**: **4,984 below threshold, 727 flagged, and five unusable light curves**. All **22 eligible follow-up fits** completed and have initial plot reviews; all44 reserved-sector timing tests are inconclusive. One fit still has an initial source check pending: the already reported TIC58464534 signal; none is a securely attributed new planet candidate. This is a scoped sample, not an all-TESS completeness result. [Terminal reconciliation](results/qlp-faint-midradius-remaining-one-20261011/terminal-verification.json).

Prior scope audit: a metadata audit found **139 unused stars with multiple, more closely spaced sectors**, plus1,485 single-sector stars and400 with no returned QLP product. No light curves were opened during that audit; the pilot above subsequently opened16. [Audit and proposed validation design](results/qlp-faint-midradius-unused-coverage-audit-20261011/ASSESSMENT.md).

Latest source check: **TIC149005183 (8.226205 days) is weakened**. Three raw images show background shifts and changing residuals near brighter neighboring blends without a clean target transit. [Images and limitations](results/qlp-faint-midradius-one-reserved-remaining-coverage-followup-20261011/149005183-peak2/ASSESSMENT.md).

Latest source check: **TIC291110031 (8.776997 days) is weakened**. Both raw event images have broad background offsets, with inconsistent target-region residuals. No transit host is secure; the reserved-sector test remains inconclusive. [Images and limitations](results/qlp-faint-midradius-one-reserved-remaining-coverage-followup-20261011/291110031-peak0/ASSESSMENT.md).

Latest source check: **TIC423597656 (9.111625 days) is weakened**. All three raw event images show changing positive/negative residuals near bright neighbor TIC423597665 at the image edge, without a secure target transit. [Images and limitations](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/423597656-peak0/ASSESSMENT.md).

Latest source check: **TIC23687157 (1.855 days) favors neighbor contamination**. Ten raw event images show an off-target feature near Gaia eclipsing binary TIC23687134; an eleventh has an extreme background offset. Gaia’s96.4-day period does not match the TESS fit, so the physical cause remains unresolved. [Images, identity check and limitations](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/23687157-peak0/ASSESSMENT.md).

Latest source check: **TIC319010061 (0.57649 days) is weakened**. Forty-one raw event images show a recurring feature near an abrupt column boundary, with background changes and mixed target-region residuals. The raw-value audit confirms the boundary; no transit host is secure. [Images and audit](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/319010061-peak0/ASSESSMENT.md).

Latest source check: **TIC435878345’s 2.974-day signal strongly favors contamination near TIC435878339**. All nine raw and nine processed event images place the dimming about3.7pixels from the target. The unique neighboring host remains unresolved. [Image and catalog checks](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/435878345-peak0/ASSESSMENT.md).

Latest source check: **TIC224180405’s 1.10265-day dips strongly favor neighboring-source contamination**. All22 usable raw images show the dimming displaced from the target, near TIC224180336 in a crowded scene. Gaia has no returned variability entry for the queried sources; a unique host remains unresolved. [Images, catalog audit and limits](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/224180405-peak0/ASSESSMENT.md).

Latest source check: **TIC439689688 favors neighboring-source contamination**. Eight usable event images place the dimming feature away from the target in a crowded scene. The 2.36-day fit also appears to be a period alias; the underlying signal is near 0.787 days. Gaia has no variability entry for the queried sources, which does not exclude an eclipse. [Evidence and limits](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/439689688-peak2/ASSESSMENT.md).

Latest source check: **TIC77453582 (about 5.99 days) is weakened**. Five raw event images show changing background offsets and mixed-sign scene residuals without a secure transit host. Its reserved-sector test remains inconclusive. [Images and assessment](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/77453582-peak0/ASSESSMENT.md).

Latest source check: **TIC94923263 (8.47 days) is weakened**. Both usable event images show substantial background offsets without a consistent isolated dimming source. Its reserved-sector timing test remains inconclusive. [Images and assessment](results/qlp-faint-midradius-one-reserved-remaining-coverage-followup-20261011/94923263-peak0/ASSESSMENT.md).

Latest source check: **TIC26042880’s5.66-day dips favor neighboring-source contamination**, rather than a planet around the target. The older-sector timing test is inconclusive. [Images and assessment](results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/26042880-peak0/ASSESSMENT.md).

Completed search scope and limitations: [2,810-target assessment](results/qlp-faint-midradius-one-reserved-remaining-20261011/ASSESSMENT.md).

Latest search extension: **a fresh 16-star pilot completed with no eligible candidates** (13 below threshold,3 flagged). It opens a2826-target metadata sample with one distant reserved epoch. Small injection tests recovered larger planets more reliably; no Earth-radius trial passed screening. [Scope, results and sensitivity](results/qlp-faint-midradius-one-reserved-pilot-20261011/ASSESSMENT.md).

Latest catalog check: **TIC80387959 does not pass Gaia’s suggested radial-velocity variability cuts**, but the competing neighbors lack the required diagnostics. This neither validates a planet nor resolves the uncertain transit host. [Identity-checked RV context and limits](results/rv-context-80387959-20261011/ASSESSMENT.md).

Latest cross-epoch check: **TIC429034844’s source attribution fails to agree across sectors**. Sector42 favors the target; sectors43 and70 favor its close neighbor, including under brightness-ratio constraints. Fixed-template controls pass despite this disagreement, leaving the host unresolved. [Older-epoch evidence and limits](results/prf-epochs-429034844-20261011/ASSESSMENT.md).

Latest scene-model check: **TIC429034844’s neighbor preference survives five brightness-ratio constraints, but weakens substantially**. The unconstrained fit had assigned almost all close-pair light to the fainter star. Using the catalog ratio reduces the conditional fit advantage from626 to69 in chi-square; host attribution is still unresolved. [Sensitivity results and controls](results/prf-ratio-429034844-20261011/ASSESSMENT.md).

Latest PRF check: **TIC429034844’s image fit favors close neighbor TIC611135702 under the adopted alignment**. Both simulated hosts pass fixed-template controls, but shifting registration by0.125 pixel reverses the preference. Host attribution remains unresolved. [Fit, controls and alignment sensitivity](results/prf-429034844-s70-20261011/ASSESSMENT.md).

Latest blend check: **TIC429034844 has a viable close-neighbor eclipse alternative**. TIC611135702 lies2.21 arcseconds away; an illustrative flux-mixing calculation requires a29–33% neighbor eclipse to reproduce the combined dips. Existing TESS localization does not exclude it, and Gaia velocity contamination remains untested. [Geometry, dilution and limits](results/close-blend-429034844-20261011/ASSESSMENT.md).

Latest physical check: **TIC429034844 has substantial Gaia radial-velocity variability**, strengthening a binary or blended-spectrum explanation. The reported robust range is95 km/s across22 observations,19 involving spectral deblending. There is no epoch-velocity match to the TESS period, so the physical cause remains unresolved. [Identity-checked evidence and limits](results/rv-context-429034844-20261011/ASSESSMENT.md).

Latest source check: **TIC373414832 (14.428026 days) is weakened**. All four usable event images show reversing positive/negative lobes near brighter neighbor TIC373414837, without a secure target-host transit. [Images and assessment](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/373414832-peak1/ASSESSMENT.md).

Latest source checks: **both TIC354475391 fits are weakened**. Four usable event images show changing positive/negative features around a brighter neighboring blend. The fits share348 inside-dip exposures, so they do not independently confirm a planet. [First fit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/354475391-peak0/ASSESSMENT.md) · [Second fit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/354475391-peak1/ASSESSMENT.md).

Latest source check: **TIC248352802 (13.838306 days) remains unresolved**. Four raw event images have large background offsets and mixed-sign target-region residuals; they do not securely identify a transit source. [Images and assessment](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/248352802-peak0/ASSESSMENT.md).

Latest source check: **TIC399119821 (8.507515 days) is weakened**. Its two usable images show opposite-sign background offsets; an earlier predicted window is fully flagged. No consistent isolated source is established. [Images and assessment](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/399119821-peak0/ASSESSMENT.md).

Latest source check: **TIC302382075 is weakened**. Three raw event images show weak target-region residuals and background changes; the enormous fitted depth is not a reliable physical measurement. Large excursions already exist in the QLP input flux. [Images and data audit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/302382075-peak0/ASSESSMENT.md).

Latest source check: **TIC320351354 (5.638430 days) is weakened**. Its four usable images show background steps and inconsistent target-region residuals, without a repeatable isolated dimming source. [Images and raw-column audit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/320351354-peak2/ASSESSMENT.md).

Latest source checks: **both TIC1693886 fits are weakened**. Each selects two usable images with background offsets and mixed target-adjacent residuals. They share62 inside-dip exposures and do not independently confirm a planet. [First fit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/1693886-peak0/ASSESSMENT.md) · [Competing fit](results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/1693886-peak1/ASSESSMENT.md).

Latest source check: **TIC439403383 (13.594649 days) is weakened**. Four event images show background offsets of opposite signs, without a consistent isolated dimming source. [Images and assessment](results/qlp-faint-midradius-remaining-one-followup-20261011/439403383-peak1/ASSESSMENT.md).

Latest source check: **TIC372994314 (7.177796 days) is weakened**. Eight raw event images are dominated by changing positive/negative residuals near a brighter neighboring blend, not a clean target-host eclipse. [Images and assessment](results/qlp-faint-midradius-remaining-one-followup-20261011/372994314-peak0/ASSESSMENT.md).

Latest source check: **TIC101351671 (6.457586 days) is weakened**. Its four event images show large background offsets and mixed positive/negative residuals rather than a reliable isolated dimming source. [Images and assessment](results/qlp-faint-midradius-remaining-one-followup-20261011/101351671-peak0/ASSESSMENT.md).

Latest timing check: **TIC429034844’s dips align across three opened sectors at a provisional0.466995-day period**. Alternating-depth differences vary by sector; a binary remains plausible. A finer local grid now resolves the conditional likelihood range, but full timing uncertainty and physical classification remain unresolved. [Refined fit and limits](results/joint-clock-fine-429034844-20261011/ASSESSMENT.md).

Latest alternating-dip check: **TIC429034844’s two dip families both localize near the target**, across43 usable sector70 images. A shared source region is supported; unresolved blends and an eclipsing binary remain possible. [Images and limits](results/parity-pixels-429034844-20261011/ASSESSMENT.md).

Latest source check: **TIC429034844’s dimming repeatedly localizes near the target** in raw and processed sector70 images. This supports the target region, but does not resolve close blends or the possible eclipsing-binary interpretation. [All30 event maps and limitations](results/qlp-faint-midradius-remaining-one-followup-20261011/429034844-peak1/ASSESSMENT.md).

Latest alias check: **TIC429034844** shows a shorter **0.466822-day** dip sequence across three already-opened sectors. Older dips fall outside the original predicted windows; an eclipsing binary and blended source remain plausible. It is an unresolved signal, not a likely planet. [Folds and verification](results/alias-429034844-20261011/ASSESSMENT.md).

Latest morphology check: **TIC365744968 is weakened as an isolated-transit candidate**. Broad repeating aperture-flux modulation is largely removed by QLP processing, leaving a shallow residual near the original minimum. Stellar activity is a stronger alternative; an embedded transit is neither established nor excluded. [Three-sector comparison](results/morphology-365744968-20261011/ASSESSMENT.md).

Latest literature check: **TIC365744968 is a published young M4 group member (THOR28)**. Stellar activity now needs explicit testing as an explanation for its broad1.397-day signal; this is not a known transit-period match or a planet exclusion. [Identity verification and source](results/literature-365744968-20261011/ASSESSMENT.md).

Latest source check: **TIC365744968 (1.397134 days)** has recurring target-region residuals, but several events have large background changes. Its host remains unresolved and older-sector timing tests remain inconclusive. It warrants further checks, not a planet claim. [Assessment and all32 event images](results/qlp-faint-midradius-remaining-one-followup-20261011/365744968-peak0/ASSESSMENT.md).

**TIC377129640 is already reported in the literature as an eclipsing variable**, with an exact TIC/Gaia identity match to a March2026 preprint. It is removed from consideration as a newly discovered signal; the preprint is not independent physical validation. [Literature assessment](results/literature-377129640-20261011/ASSESSMENT.md).

Latest source check: **TIC160463097 (4.152796 days)** favors contamination: all six usable event images show an off-target feature about four pixels from the star. The crowded field prevents unique source assignment. [Assessment and images](results/qlp-faint-midradius-remaining-one-followup-20261011/160463097-peak0/ASSESSMENT.md).

Latest source check: **TIC66775591 (1.304981 days)** strongly favors contamination: all44 usable difference images show an off-target feature near **TIC66775597**, a Gaia eclipsing-binary candidate with a **1.304738-day** period. Exact eclipse-time alignment remains untested. [Assessment and images](results/qlp-faint-midradius-remaining-one-followup-20261011/66775591-peak0/ASSESSMENT.md).

Latest literature check: **TIC58464534** is also an existing eclipsing-binary catalog entry, with a **2.800456-day** published period near twice our fitted period. It is not a new planet candidate. **TIC443761618 (1.241700 days)** now favors contamination: recurring offset residuals lie near a blended neighbor group containing Gaia eclipsing-binary candidate **TIC371688493 (0.621000 days)**. Unique source attribution remains unresolved. [Literature evidence](results/literature-58464534-20261011/ASSESSMENT.md) · [Unresolved signal assessment](results/qlp-faint-midradius-remaining-one-followup-20261011/443761618-peak0/ASSESSMENT.md).

Latest source check: **TIC101404423 (2.433118 days)** is strongly disfavored as a target-host planet: repeated difference images peak near **TIC101404439**, a Gaia eclipsing-binary candidate with a **2.429853-day** period within the TESS timing range. Contamination is strongly favored; exact eclipse-time agreement remains untested. [Assessment and evidence](results/qlp-faint-midradius-remaining-one-followup-20261011/101404423-peak0/ASSESSMENT.md).

Latest source check: **TIC169623350 (0.997498 days)** is weakened: recurring raw-image differences lie near neighboring **TIC169623369**, about two pixels from the target. Contamination is favored; the physical origin and unique source remain unresolved. Older-sector timing predictions remain inconclusive. [Assessment and images](results/qlp-faint-midradius-remaining-one-followup-20261011/169623350-peak0/ASSESSMENT.md).

Latest deeper check: **TIC149919534 (16.042907 days)** is weakened by time-resolved checks. Its stronger event lies on a changing baseline: the fitted target signal shifts from 5.94 to 1.29 depending on which side supplies the baseline. The first event also overlaps control variability; no reliable recurring target-host transit is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/ASSESSMENT.md).

Latest deeper check: **TIC156001092 (13.423921 days)** remains an unresolved signal. Across 36 matching scene models, off-event variability can equal or exceed the selected dips; neither the host nor a planetary explanation is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/ASSESSMENT.md) · [Matched controls](results/prf-156001092-matched-controls-20261011/controls.png).

The remaining **4,144-target two-sector midradius search has finished**. After counting two unchanged network retries once per star, [final reconciliation](results/qlp-faint-midradius-remaining-two-20261011/joined-terminal.json) gives **3,218 below threshold, 886 flagged, and 40 with insufficient training coverage** (4,104 usable searches). Original counts and all 42 original errors remain preserved. Each of the 40 data-quality failures has only one usable assigned sector under unchanged preprocessing; no replacement sectors or reserved data were used. All 71 eligible follow-up computations finished (30 original-policy, 41 coverage diagnostics), and [initial plot reviews now cover all 71](results/qlp-faint-midradius-remaining-two-20261011/review-inventory.json). All 71 have initial source-diagnostic reports; host attribution and further scientific vetting remain incomplete. [Terminal audit](results/qlp-faint-midradius-remaining-two-20261011/terminal-verification.json). This is a scoped sample, not an all-TESS completeness result.

Latest check: **TIC85408605 (7.888412-day alternative fit)** retains strong off-target events near TIC85408619 and adds a weak intervening event. The competing fits share92 dip-window exposures; contamination remains favored and the true period unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/85408605-peak1/ASSESSMENT.md).

Latest check: **TIC303599188 (0.930261/2.790390 days)** localizes off-target under both fits, near TIC303599200/303599195. The longer fit shares82 of85 inside exposures with the shorter fit, strengthening the contamination/alias interpretation. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/303599188-peak2/ASSESSMENT.md).

Latest check: **TIC180872988 (11.164831 days)** has weak mixed sector2 images and a sector3 background change that is flagged in the processed data. No consistent isolated dip source is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/180872988-peak0/ASSESSMENT.md).

Latest check: **TIC390173361 (13.208303 days)** has only two raw exposures per sector24 dip window, opposite-sign background gradients, and no sector25 coverage at predicted times. No reliable host attribution is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/390173361-peak0/ASSESSMENT.md).

Latest check: **TIC396062641 (16.228765 days)** has one usable event per sector, both dominated by field-wide background changes. No consistent isolated source is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/396062641-peak0/ASSESSMENT.md).

Latest check: **TIC341632641 (15.563823 days)** shows opposite-sign field-wide changes in sector74 and edge structure in sector73. No reliable host attribution is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/341632641-peak1/ASSESSMENT.md).

Latest check: **TIC155990070 (12.910009 days)** has large field-wide background changes in sector103 and inconsistent weak residuals in sector104. No reliable host attribution is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/155990070-peak0/ASSESSMENT.md).

Latest check: **TIC183120530 (14.057944 days)** has field-wide background changes, including opposite-sign event images in sector68. No consistent isolated dip source is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/183120530-peak0/ASSESSMENT.md).

Latest check: **TIC169785835 (16.812329 days)** shows two recurring off-target dips near **TIC169785532**, a Gaia-cataloged eclipsing binary (6.720692 days). A fixed catalog-period check does not establish consistent recurrence; the possible alias remains unresolved, and nearby faint blends prevent unique source attribution. The target-host planet interpretation is deprioritized. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/169785835-peak0/ASSESSMENT.md).

Latest check: **TIC9823113 (15.062543/15.615863 days)** has background/quality concerns under both competing fits. They share 58 inside exposures in sector80, and both have fully flagged sector79 windows. Neither has reliable host attribution. [Latest assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9823113-peak1/ASSESSMENT.md).

Latest check: **TIC156001092 (13.423921 days)** has recurring target-adjacent residuals in sector69, accompanied by positive and negative residuals at neighboring stars. Sector68 processed dip windows are fully flagged. Further source/background modeling is needed; host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/ASSESSMENT.md).

Latest check: **TIC9038963 (13.685119/14.979057 days)** has background/quality concerns under both competing fits. The alternative fit adds negative raw event maps, weak processed residuals and only two or three exposures per dip window. Neither fit has reliable host attribution. [Latest assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9038963-peak1/ASSESSMENT.md).

Latest check: **TIC317713012 (12.683696 days)** shows field-wide background changes and inconsistent source structure across five usable image windows in sectors85/86. No reliable host attribution is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/317713012-peak1/ASSESSMENT.md).

Latest check: **TIC408547900 (13.920856 days)** shows large field-wide background changes and inconsistent target-relative residuals across sectors73/74, despite unflagged raw event exposures. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/408547900-peak1/ASSESSMENT.md).

Latest check: **TIC74189224 (13.125585 days)** shows field-wide background changes and differing off-target features across sectors103/104. One event is fully flagged and processed pixel products were unavailable. No reliable host attribution is established. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/74189224-peak0/ASSESSMENT.md).

Latest check: **TIC18119757 (13.990829 days)** has four event maps that are negative across the field. Its sector26 validation error is a reproducible preprocessing limit, not a download failure. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/18119757-peak0/ASSESSMENT.md).

Latest check: **TIC148962744 (14.037689 days)** shows field-wide background and column structure in sector74. All raw sector75 dip exposures and all processed dip exposures are flagged. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/148962744-peak0/ASSESSMENT.md).

Latest check: **TIC79111355 (18.842155 days)** now has separate single-event image diagnostics: sector94 shows mixed target-adjacent residuals, while sector95 is dominated by a field-wide background change. No consistent isolated source is established. Original coverage failures remain preserved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/79111355-peak0/ASSESSMENT.md).

Latest check: **TIC149919534 (16.042907 days)** has tentative target-region residuals in two sector75 events, alongside background gradients. Flagged sector74 coverage prevents a second-sector source check; host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/ASSESSMENT.md).

Latest check: **TIC232521494 (14.427498 days)** shows alternating field-wide background changes, fully flagged processed dip windows, and one raw event with only two unflagged exposures. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/232521494-peak0/ASSESSMENT.md).

Latest check: **TIC420110652 (15.764952/14.951141 days)** has field-wide negative image stacks under both competing fits, flagged processed event windows, and sparse sector73 coverage. Neither fit has reliable host attribution. [Latest assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/420110652-peak1/ASSESSMENT.md).

Latest check: **TIC333652041 (12.979163 days)** shows field-wide background changes and inconsistent source structure across sectors102/103. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/333652041-peak0/ASSESSMENT.md).

Latest check: **TIC142381963 (12.713720 days)** has fully flagged processed sector75 event windows and weak, mixed sector76 image residuals. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/142381963-peak0/ASSESSMENT.md).

Latest check: **TIC22741082 (15.546694 days)** is limited by alternating image-background changes, weak processed residuals, and a fully flagged event window. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/22741082-peak0/ASSESSMENT.md).

Latest check: **TIC425293543** has deep target-region eclipses across four sectors. Separate fits to alternating eclipses give **3.9436258/3.9436372 days**, strengthening a **roughly3.94363-day eclipsing-binary interpretation**. The orbital solution and faint blends remain unresolved; this is not a credible planet candidate. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/425293543-peak0/ASSESSMENT.md).

Latest check: **TIC29439764 (12.528371/12.917509 days)** has field-wide image changes under both fits, fully flagged processed sector24 event windows, and sparse sector25 coverage. Source attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/29439764-peak0/ASSESSMENT.md).

Latest check: **TIC358699700 (16.417682/12.291004 days)** likely suffers neighboring-source contamination: both fits point toward TIC358699657 and faint blends, and their final dip windows overlap. The exact variable remains unresolved; Gaia nonmatches do not exclude it. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/358699700-peak2/ASSESSMENT.md).

Latest check: **TIC160147376 (13.474719/15.360800 days)** shows field-wide image changes under both competing fits, with flagged or sparse processed event coverage. Neither fit has reliable host attribution. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/160147376-peak1/ASSESSMENT.md).

Latest check: **TIC148931702 (13.848450 days)** has four supported photometric dips, but its event images show field-wide background changes without a consistent isolated source. Host attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/148931702-peak0/ASSESSMENT.md).

Latest check: **TIC313485055 (15.251392 days)** has four supported dips, but sector74 processed events are fully flagged and sector75 images retain a strong gradient. Source attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/313485055-peak0/ASSESSMENT.md).

Latest check: **TIC137207967 (13.059159 days)** has four supported photometric dips, but all four raw difference images are negative across the field. Source attribution remains unreliable. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/137207967-peak1/ASSESSMENT.md).

Latest check: **TIC389659430 (18.799587/17.896661 days)** has weak, mixed raw/processed source images and sparse event coverage. Neither competing fit has clean confirmation across sectors. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/389659430-peak0/ASSESSMENT.md).

Latest check: **TIC154570351 (14.005431 days)** has field-wide negative raw difference images and no quality-zero processed exposures inside any predicted event window (313 flagged exposures). [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/154570351-peak0/ASSESSMENT.md).

Latest check: **TIC299127362 (13.086244 days)** shows mixed residuals around a brighter neighboring group, with sparse coverage in some events. Source attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/299127362-peak0/ASSESSMENT.md).

Latest check: **TIC324894265 (7.662988 days)** is limited by strong mixed image residuals around bright neighboring TIC324894237. The source and physical cause remain unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/324894265-peak1/ASSESSMENT.md).

Latest check: **TIC198489509 (14.235155 days)** remains unresolved: target-region features in sector74 coexist with edge/background changes, while sector75 shows strong background and column structure. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/198489509-peak0/ASSESSMENT.md).

Latest check: **TIC317129781 (15.121657 days)** shows large alternating image-background changes, without a consistent isolated source. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/317129781-peak0/ASSESSMENT.md).

Latest check: **TIC136996439 (13.600712 days)** has field-wide image-background changes, weak processed structure, and an event whose seven processed exposures are all flagged. Source attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/136996439-peak2/ASSESSMENT.md).

Latest check: **TIC79155290 (13.464913 days)** has large image-background changes. One event retains a target-region feature with an adjacent negative residual; source attribution remains unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/79155290-peak0/ASSESSMENT.md).

Latest check: **TIC122288285 (13.523160/12.995343 days)** shows field-wide image-background changes under both fits, with no reliable host attribution. The fits share one measured dip. [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/122288285-peak0/ASSESSMENT.md).

Latest check: **TIC232521775 (14.331656 days)** remains unresolved: sector74 images show background and mixed target-region structure; sector75 lacks a second accepted image event. Missing coverage is not a failed detection. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/232521775-peak0/ASSESSMENT.md).

Latest check: **TIC85408605 (15.776969/7.888412 days)** likely suffers neighboring-source contamination. Both sector79 dips lie near TIC85408619 and nearby blended sources, far from the target. The two fits reuse the same supported dips. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/85408605-peak0/ASSESSMENT.md).

Latest source check: **TIC 80571902 (10.950771 days)** likely suffers neighboring-star contamination: all three supported events show a displaced feature near TIC 80571910 and a fainter blend. Both events of its competing 17.762186-day fit show the same displaced feature; the exact variable and true period remain unresolved. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/80571902-peak0/ASSESSMENT.md).

Latest check: **TIC 142396584 (14.188274 days)** retains one dip across QLP and SPOC processing, but image backgrounds prevent secure source attribution. Three other processed comparisons lack coverage after gap-edge trimming, not failed detections. [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0/ASSESSMENT.md).

Unresolved signals worth retaining for further investigation (not credible new planet claims):

| Signal | Period | Current limitation | Evidence |
|---|---:|---|---|
| TIC 155990070 (peak 0) | 12.910009 d | Large S103 background changes; inconsistent S104 residuals, host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/155990070-peak0/ASSESSMENT.md) |
| TIC 169785835 (peak 0) | 16.812329 d | Off-target dips near cataloged eclipsing binary TIC169785532; possible alias unverified, unique variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/169785835-peak0/ASSESSMENT.md) |
| TIC 183120530 (peak 0) | 14.057944 d | Field-wide background changes and opposite-sign S68 event maps; no reliable host attribution. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/183120530-peak0/ASSESSMENT.md) |
| TIC 29439764 (peak 1) | 12.917509 d | Background/quality and sparse-coverage concerns; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/29439764-peak1/ASSESSMENT.md) |
| TIC 341632641 (peak 1) | 15.563823 d | Opposite-sign S74 field changes and S73 edge structure; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/341632641-peak1/ASSESSMENT.md) |
| TIC 358699700 (peak 0) | 12.291004 d | Likely neighboring-source contamination; exact variable/period unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/358699700-peak0/ASSESSMENT.md) |
| TIC 396062641 (peak 0) | 16.228765 d | One image event per sector, field-wide background changes; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/396062641-peak0/ASSESSMENT.md) |
| TIC 9823113 (peak 0) | 15.062543 d | Background/quality and held-coverage concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9823113-peak0/ASSESSMENT.md) |
| TIC 9823113 (peak 1) | 15.615863 d | Background/quality concerns; shared exposures with alternate fit; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9823113-peak1/ASSESSMENT.md) |
| TIC 29439764 (peak 0) | 12.528371 d | Background/quality and sparse-coverage concerns; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/29439764-peak0/ASSESSMENT.md) |
| TIC 261759545 (peak 1) | 1.399025 d | Likely cataloged-binary contamination near TIC 261759559; its half-period agrees with the three-dip shorter cycle within 3.4 s. Background fits fail in the crowded field. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/261759545-peak1/ASSESSMENT.md) |
| TIC 405695928 (peak 0) | 1.342617 d | Extreme archived scatter and roughly 49% selected depth; cause unresolved; source checks pending, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/405695928-peak0/ASSESSMENT.md) |
| TIC 111866055 (peak 0) | 1.700671 d | Likely known-binary contamination near TIC111866057; displaced images and approximate catalog half-period agree. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/111866055-peak0/ASSESSMENT.md) |
| TIC 183257459 (peak 2) | 1.988639 d | Contamination/alias concern: offset feature near a faint blend; all background fits fail and one extra phase is weak. Source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/183257459-peak2/ASSESSMENT.md) |
| TIC 3920290 (peak 0) | 1.102303 d | Likely eclipsing-binary contamination: displaced raw dip near TIC3920308, with matching approximate half-period; exact host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/3920290-peak0/ASSESSMENT.md) |
| TIC 257984190 (peak 0) | 2.586563 d | Inconsistent displaced/edge image patterns; no repeatable source, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/257984190-peak0/ASSESSMENT.md) |
| TIC 358699700 (peak 2) | 16.417682 d | Likely neighboring-source contamination; exact variable unresolved, both fits now checked. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/358699700-peak2/ASSESSMENT.md) |
| TIC 122288285 (coverage peak 0) | 13.523160 d | Both fits show field-wide image-background changes; shared later dip, unresolved source and inconclusive reserved timing. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/122288285-peak0/ASSESSMENT.md) |
| TIC 122288285 (coverage peak 1) | 12.995343 d | Both fits show field-wide image-background changes; shared later dip, unresolved source and inconclusive reserved timing. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/122288285-peak1/ASSESSMENT.md) |
| TIC 79155290 (coverage peak 0) | 13.464913 d | Large image-background changes; last event has mixed target-region structure. Host unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/79155290-peak0/ASSESSMENT.md) |
| TIC 136996439 (coverage peak 2) | 13.600712 d | Background/quality concern: field-wide changes and one fully flagged processed event. Host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/136996439-peak2/ASSESSMENT.md) |
| TIC 80571902 (coverage peak 1) | 17.762186 d | Likely neighbor contamination for both the 10.95-day and 17.76-day fits; exact variable and true period unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/80571902-peak1/ASSESSMENT.md) |
| TIC 180872988 (coverage peak 0) | 11.164831 d | Low-flux band plus pixel background/quality concerns; no reliable host. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/180872988-peak0/ASSESSMENT.md) |
| TIC 317129781 (coverage peak 0) | 15.121657 d | Large alternating image-background changes; no consistent isolated source, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/317129781-peak0/ASSESSMENT.md) |
| TIC 198489509 (coverage peak 0) | 14.235155 d | Background/column structure and edge features prevent source attribution; refined period and reserved timing remain uncertain. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/198489509-peak0/ASSESSMENT.md) |
| TIC 324894265 (coverage peak 1) | 7.662988 d | Strong mixed residuals around bright TIC324894237; source and physical cause unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/324894265-peak1/ASSESSMENT.md) |
| TIC 299127362 (coverage peak 0) | 13.086244 d | Mixed residuals near bright TIC299127335 and sparse event coverage; source unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/299127362-peak0/ASSESSMENT.md) |
| TIC 389659430 (coverage peak 0) | 18.799587 d | Weak mixed source images, sparse events and sector28 coverage/quality limitations; both fits unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/389659430-peak0/ASSESSMENT.md) |
| TIC 389659430 (coverage peak 1) | 17.896661 d | Weak mixed source images, sparse events and sector28 coverage/quality limitations; both fits unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/389659430-peak1/ASSESSMENT.md) |
| TIC 154570351 (coverage peak 0) | 14.005431 d | Background/quality concern: all313processed in-event exposures flagged; source unresolved, not a nondetection. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/154570351-peak0/ASSESSMENT.md) |
| TIC 220580368 (peak 0) | 4.446674 d | Likely contamination near TIC 220580389 (~3.8 pixels off target); its Gaia binary period differs, so exact variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/220580368-peak0/ASSESSMENT.md) |
| TIC 142396584 (peak 0) | 14.188274 d | Background/source-systematics concerns; one dip survives QLP/SPOC comparison, other three lost to gap-edge trimming. Host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0/ASSESSMENT.md) |
| TIC 302011199 (peak 0) | 0.804755 d | Near-target feature remains unresolved; close neighbor is a cataloged binary at a different period, with image-systematics concerns. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/302011199-peak0/ASSESSMENT.md) |
| TIC 232521775 (peak 0) | 14.331656 d | Background/mixed image structure; sector75 has only one accepted image event. Host unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/232521775-peak0/ASSESSMENT.md) |
| TIC 85408605 (peak 0) | 15.776969 d | Likely neighbor contamination near TIC85408619; fits share supported events. Exact source/period unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/85408605-peak0/ASSESSMENT.md) |
| TIC 85408605 (peak 1) | 7.888412 d | Likely neighbor contamination near TIC85408619; fits share supported events. Exact source/period unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/85408605-peak1/ASSESSMENT.md) |
| TIC 15736353 (peak 0) | 7.235772 d | Likely contamination: sectors 70/71 place the signal near faint TIC 15736352, ~1.7 pixels off target; exact variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/15736353-peak0/ASSESSMENT.md) |
| TIC 425293543 (peak 0) | 1.972353 d | Deep target-region eclipsing suspect; held-out validation failed, faint blends unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/425293543-peak0/ASSESSMENT.md) |
| TIC 356743185 (peak 0) | 13.809279 d | Artifact/background concern: raw images inconsistent, processed sector74 event exposures all flagged; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/356743185-peak0/ASSESSMENT.md) |
| TIC 80571902 (peak 0) | 10.950771 d | Likely neighbor contamination for both the 10.95-day and 17.76-day fits; exact variable and true period unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/80571902-peak0/ASSESSMENT.md) |
| TIC 381024599 (peak 0) | 5.398956 d | Likely contamination near TIC 381024603: offset feature survives both background corrections in both sectors; exact variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/381024599-peak0/ASSESSMENT.md) |
| TIC 181272177 (peak 0) | 1.976920 d | Likely cataloged-binary contamination: sectors 88/89 point near TIC 181272135, whose Gaia binary period is about twice the QLP period. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/181272177-peak0/ASSESSMENT.md) |
| TIC 446524946 (peak 0) | 1.114581 d | Likely cataloged-binary contamination: image source near TIC 446692470, whose Gaia period is about twice the QLP period; reserved sectors recur. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/446524946-peak0/ASSESSMENT.md) |
| TIC 148001520 (peak 0) | 4.355528 d | Offset feature persists after two background corrections in both sectors; contamination concern, exact source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/148001520-peak0/ASSESSMENT.md) |
| TIC 361980197 (peak 0) | 17.352627 d | Likely neighboring-source contamination: raw sectors 46/47 and processed sector 47 place the deep dips ~3.7 pixels off target; exact blend component unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/361980197-peak0/ASSESSMENT.md) |
| TIC 350072366 (peak 0) | 14.456618 d | Diagnostic only; source checks pending, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-three-coverage-followup-20261011/350072366-peak0/ASSESSMENT.md) |
| TIC 390173361 (peak 0) | 13.208303 d | Sparse S24 background gradients; S25 predicted windows uncovered, host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/390173361-peak0/ASSESSMENT.md) |
| TIC 22741082 (peak 0) | 15.546694 d | Background/quality concern; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/22741082-peak0/ASSESSMENT.md) |
| TIC 74189224 (peak 0) | 13.125585 d | Background/contamination and coverage concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/74189224-peak0/ASSESSMENT.md) |
| TIC 408547900 (peak 1) | 13.920856 d | Background/source-systematics concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/408547900-peak1/ASSESSMENT.md) |
| TIC 9038963 (peak 0) | 13.685119 d | Background/quality concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9038963-peak0/ASSESSMENT.md) |
| TIC 9038963 (peak 1) | 14.979057 d | Background/quality and sparse exposure concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/9038963-peak1/ASSESSMENT.md) |
| TIC 156001092 (peak 0) | 13.423921 d | Tentative target-adjacent residuals; neighboring residuals/quality concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/ASSESSMENT.md) |
| TIC 317713012 (peak 1) | 12.683696 d | Background/source-systematics concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/317713012-peak1/ASSESSMENT.md) |
| TIC 367812343 (peak 0) | 15.569127 d | Unresolved: negative image residual and insufficient-event checks; reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/367812343-peak0/ASSESSMENT.md) |
| TIC 148931702 (peak 0) | 13.848450 d | Background/source-systematics concern; host unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/148931702-peak0/ASSESSMENT.md) |
| TIC 303599188 (peak 0) | 0.930261 d | Likely contamination near TIC 303599200/303599195; alternative aliases, exact variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/303599188-peak0/ASSESSMENT.md) |
| TIC 303599188 (peak 2) | 2.790390 d | Likely contamination near TIC 303599200/303599195; alternative aliases, exact variable unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/303599188-peak2/ASSESSMENT.md) |
| TIC 365662408 (peak 0) | 13.638752 d | Diagnostic only; source checks pending, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-four-coverage-followup-20261011/365662408-peak0/ASSESSMENT.md) |
| TIC 332624792 (peak 0) | 13.994011 d | Unresolved: broad positive versus entirely negative raw residuals; no repeatable compact source, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/332624792-peak0/ASSESSMENT.md) |
| TIC 313485055 (peak 0) | 15.251392 d | Sector74processed events fully flagged; sector75 gradient prevents reliable source attribution. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/313485055-peak0/ASSESSMENT.md) |
| TIC 18119757 (peak 0) | 13.990829 d | Field-wide negative event maps; held coverage limited; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/18119757-peak0/ASSESSMENT.md) |
| TIC 148962744 (peak 0) | 14.037689 d | Background/quality concerns; no reliable host attribution. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/148962744-peak0/ASSESSMENT.md) |
| TIC 429294074 (peak 1) | 1.484929 d | Likely cataloged-binary contamination: all three dip phases point toward TIC 429294064; its binary half-period matches the shorter cycle within ~4 s. Crowded-field limits retained. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/429294074-peak1/ASSESSMENT.md) |
| TIC 235596071 (peak 0) | 4.801536 d | Likely contamination near TIC 235596068/235596066 in both sectors; exact variable unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/235596071-peak0/ASSESSMENT.md) |
| TIC 307925590 (peak 1) | 5.192774 d | Background/source-systematics concern: mixed neighbor residuals persist after subtraction across four sectors; no secure host, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-four-followup-20261011/307925590-peak1/ASSESSMENT.md) |
| TIC 202443757 (peak 0) | 14.660408 d | Diagnostic only; reserved timing inconclusive, source checks pending. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/202443757-peak0/ASSESSMENT.md) |
| TIC 398284654 (peak 0) | 17.885979 d | Diagnostic only; reserved timing inconclusive, source checks pending. | [Assessment](results/qlp-faint-midradius-remaining-three-coverage-followup-20261011/398284654-peak0/ASSESSMENT.md) |
| TIC 354165453 (peak 0) | 14.522381 d | Diagnostic only; reserved timing inconclusive, source checks pending. | [Assessment](results/qlp-faint-midradius-remaining-three-coverage-followup-20261011/354165453-peak0/ASSESSMENT.md) |
| TIC 392005513 (peak 0) | 1.472822 d | Unresolved: wider background checks retain opposite-sign source residuals; nearby Gaia eclipsing binary has a different period. Reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/392005513-peak0/ASSESSMENT.md) |
| TIC 137207967 (peak 1) | 13.059159 d | All four raw event images have field-wide negative backgrounds; host unresolved, alternative detrending and reserved timing problematic. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/137207967-peak1/ASSESSMENT.md) |
| TIC 130291325 (peak 0) | 13.663299 d | Unresolved: raw sectors show broad positive versus entirely negative residuals; no repeatable compact source, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/130291325-peak0/ASSESSMENT.md) |
| TIC 160147376 (peak 1) | 13.474719 d | Background/quality concern; source unresolved, reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-followup-20261011/160147376-peak1/ASSESSMENT.md) |
| TIC 149919534 (peak 0) | 16.042907 d | Tentative target-region residuals; background/quality concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/ASSESSMENT.md) |
| TIC 160147376 (peak 0) | 15.360800 d | Background/quality and sparse-coverage concern; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/160147376-peak0/ASSESSMENT.md) |
| TIC 232521494 (peak 0) | 14.427498 d | Background/quality and sparse coverage; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/232521494-peak0/ASSESSMENT.md) |
| TIC 79111355 (peak 0) | 18.842155 d | Individual images inconsistent; background/source concerns; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/79111355-peak0/ASSESSMENT.md) |
| TIC 75880405 (peak 0) | 5.262464 d | Likely contamination: raw and processed dips in two sectors lie near the TIC 75880397/398/399 group; exact source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/75880405-peak0/ASSESSMENT.md) |
| TIC 280051317 (peak 1) | 14.344853 d | Background/quality concern: all 432 processed in-dip exposures flagged across three sectors; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/280051317-peak1/ASSESSMENT.md) |
| TIC 333652041 (peak 0) | 12.979163 d | Background/source-systematics concern; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/333652041-peak0/ASSESSMENT.md) |
| TIC 142381963 (peak 0) | 12.713720 d | Background/quality concern; source unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/142381963-peak0/ASSESSMENT.md) |
| TIC 420110652 (peak 0) | 15.764952 d | Background/quality and sparse coverage; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/420110652-peak0/ASSESSMENT.md) |
| TIC 420110652 (peak 1) | 14.951141 d | Mixed/background residuals; processed events flagged; host unresolved. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/420110652-peak1/ASSESSMENT.md) |
| TIC 126237371 | 0.726116 d | Likely contamination: processed dips in two sectors lie off target near TIC 126236985; exact variable unresolved and reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/126237371-peak0/ASSESSMENT.md) |
| TIC 469939625 | 14.687542 d | Diagnostic only: two supported events, detrending-sensitive; raw maps are background-dominated and reserved timing is inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/469939625-peak1/ASSESSMENT.md) |
| TIC 355707138 | 13.600126 d | Diagnostic only: detrending-sensitive, distant timing inconclusive; weak Sector 102 source residual does not repeat in Sector 103, and requested processed products are unavailable. | [Assessment](results/qlp-faint-midradius-remaining-three-followup-20261011/355707138-peak0/ASSESSMENT.md) |
| TIC 229684154 | 13.868528 d | Artifact-suspect: four events are stray-light flagged; three raw-sector maps show broad or negative residuals without a localized stellar dip. Reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-four-followup-20261011/229684154-peak0/ASSESSMENT.md) |
| TIC 219807827 | 13.027622 d | Artifact-suspect: two events are stray-light flagged, the raw image is entirely negative, and the first event is weaker in processed flux; reserved timing inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-four-followup-20261011/219807827-peak0/ASSESSMENT.md) |
| TIC 462575744 | 14.132484 d | Artifact-suspect: both raw-event maps show broad background changes; processed Sector 74 events are stray-light flagged and reserved timing is inconclusive. | [Assessment](results/qlp-faint-midradius-remaining-four-followup-20261011/462575744-peak0/ASSESSMENT.md) |
| TIC 438792601 | 0.781550 d | Likely contamination: both raw-image dips lie near Gaia eclipsing-system candidate TIC 288891067, whose 0.7816035-day period closely matches; blended pixels prevent unique attribution. | [Assessment](results/qlp-faint-midradius-four-pilot-followup-20261011/438792601-peak0/ASSESSMENT.md) |
| TIC 129577784 | 1.95689 d (selected alias) | Diagnostic only: similarly deep dips at one-third-cycle spacing; reserved timing is inconclusive and raw pixels do not localize a host. | [Assessment](results/qlp-near-epoch-sector83-pilot-followup-20261011/129577784-peak2/ASSESSMENT.md) |
| TIC 352831349 | 13.02207 d | Artifact-suspect diagnostic: both raw-event maps show broad background changes; reserved timing inconclusive. | [Assessment](results/qlp-faint-retrospective-gap-followup-20261011/352831349-peak0/ASSESSMENT.md) |
| TIC 258513090 | 13.27966 d | Artifact-suspect diagnostic: raw maps are negative or broadly positive, without a repeatable compact dimming source. | [Assessment](results/qlp-faint-retrospective-gap-followup-20261011/258513090-peak0/ASSESSMENT.md) |
| TIC 310128088 | 14.64575 d | Artifact-suspect diagnostic: processed events all carry stray-light/exclusion flags; raw difference is broad and cannot identify a host. | [Assessment](results/qlp-faint-retrospective-gap-followup-20261011/310128088-peak0/ASSESSMENT.md) |
| TIC 97487157 | 0.713787 d | Likely contamination: both pixel products locate the dip near TIC 97487160, about 2.7 pixels from target; reserved data unusable, exact variable unresolved. | [Assessment](results/qlp-faint-one-reserved-sector22-pilot-followup-20261010/97487157-peak0/ASSESSMENT.md) |
| TIC 154604434 | 3.38271 d | Likely contamination: processed dip lies near Gaia eclipsing system TIC 154542227 with a closely matching period; raw pixels cannot localize the source. | [Assessment](results/qlp-faint-one-reserved-sector34-pilot-followup-20261010/154604434-peak0/ASSESSMENT.md) |
| TIC 291207362 | 1.46418 d | Likely contamination: raw pixel dip lies near TIC 291207358, a Gaia eclipsing-system entry with a differing period, 2.85 pixels from target. | [Assessment](results/qlp-faint-one-reserved-sector87-pilot-followup-20261010/291207362-peak0/ASSESSMENT.md) |
| TIC 123404957 | 13.83438 d | Diagnostic only: detrending-sensitive, reserved timing inconclusive; raw pixels dominated by extended background structure. | [Assessment](results/qlp-faint-one-reserved-sector97-pilot-followup-20261010/123404957-peak0/ASSESSMENT.md) |
| TIC 164698536 | 14.44281 d | Diagnostic only: two events, detrending-sensitive, reserved timing inconclusive; background-corrected raw pixels have a negative target residual. | [Assessment](results/qlp-faint-one-reserved-sector97-pilot-coverage-followup-20261010/164698536-peak0/ASSESSMENT.md) |
| TIC 189526569 | 2.92635 d | Likely contamination: both pixel products locate the dip near TIC 189525884 (duplicate 620829057); its aperture shows ~14% primary and ~4% secondary eclipses. | [Assessment](results/qlp-faint-one-reserved-sector85-pilot-followup-20261010/189526569-peak0/ASSESSMENT.md) |
| TIC 254039664 | 3.53266 d | Likely contamination: both pixel products locate an off-target dip near TIC 254033964, whose aperture shows an ~11.4% eclipse. | [Assessment](results/qlp-faint-one-reserved-sector67-pilot-followup-20261010/254039664-peak0/ASSESSMENT.md) |
| TIC 432280723 | 2.21411 d | Likely contamination: wide pixel dip lies near a neighboring group; TIC 432277754 aperture shows ~36% primary and ~12% secondary eclipses. | [Assessment](results/qlp-faint-one-reserved-sector84-pilot-followup-20261010/432280723-peak0/ASSESSMENT.md) |
| TIC 313631310 | 5.04145 d | Diagnostic only: two events, detrending-sensitive, QLP/SPOC disagreement, inconclusive reserved timing and nonlocalizing pixels. | [Assessment](results/qlp-faint-one-reserved-sector54-pilot-coverage-followup-20261010/313631310-peak1/ASSESSMENT.md) |
| TIC 101436430 | 2.97824 d | Likely contamination: raw pixel dip lies near TIC 185284269, 3.65 pixels from target. Reserved-sector timing inconclusive. | [Assessment](results/qlp-faint-one-reserved-sector91-pilot-followup-20261010/101436430-peak0/ASSESSMENT.md) |
| TIC 1044290 | 5.96860 d | Likely contamination: both pixel products locate dips near TIC 1044282, whose aperture shows a ~27% eclipse. | [Assessment](results/qlp-faint-one-reserved-sector48-pilot-followup-20261010/1044290-peak0/ASSESSMENT.md) |
| TIC 262142774 | 4.38215 d | Likely contamination: raw difference image favors neighboring TIC 262142751. Gaia EB period differs. | [Assessment](results/qlp-faint-one-reserved-sector55-pilot-followup-20261010/262142774-peak1/ASSESSMENT.md) |
| TIC 353048232 | 4.46154 d | Likely contamination: raw difference image favors neighboring TIC 353048229. Exact variable remains unresolved. | [Assessment](results/qlp-faint-one-reserved-sector55-pilot-followup-20261010/353048232-peak0/ASSESSMENT.md) |
| TIC 466895419 | 2.18354 d | Conflicting pixel diagnostics: processed feature is off target, raw residuals surround a bright star. No secure host or independent timing recovery. | [Assessment](results/qlp-faint-one-reserved-sector55-pilot-followup-20261010/466895419-peak0/ASSESSMENT.md) |
| TIC 390650992 | 0.79492 d | Likely contamination: both pixel products locate dips near neighboring split/duplicate entries 390650995/520548011. Exact variable and period unresolved. | [Assessment](results/qlp-faint-one-reserved-sector23-pilot-followup-20261010/390650992-peak1/ASSESSMENT.md) |
| TIC 44345170 | 5.83167 d | Likely contamination: raw and processed pixel dips lie near neighboring TIC 44345176. Its Gaia EB period differs; exact variable remains unresolved. | [Assessment](results/qlp-faint-one-reserved-sector56-pilot-followup-20261010/44345170-peak0/ASSESSMENT.md) |
| TIC 80387959 | 4.19217 d | Recurs in held-out sectors, but host fits change when individual events are omitted; neighboring-source contamination remains unresolved. | [Held-out checks](results/followup-80387959-qlp90-100-20261009/heldout.json), [host assessment](results/prf-80387959-20261009/ASSESSMENT.md), [event stability](results/prf-80387959-event-stability-20261011/ASSESSMENT.md), [event controls](results/prf-80387959-event-controls-20261011/ASSESSMENT.md), [motion sensitivity](results/prf-80387959-motion-sensitivity-20261011/ASSESSMENT.md) |
| TIC 359659538 | 2.44439 d | Later-sector timing is inconclusive; an entirely negative difference image cannot locate a dimming source. | [Assessment](results/qlp-faint-sector80-pilot-followup-20261010/359659538-peak0/ASSESSMENT.md) |
| TIC 317166760 | 0.77053 d | Earlier-sector timing is inconclusive; weak, patchy pixel residuals do not establish the host. | [Assessment](results/qlp-faint-sector57-pilot-followup-20261010/317166760-peak0/ASSESSMENT.md) |
| TIC 239098567 | 1.75685 d | Earlier-sector timing is inconclusive; displaced, structured image residuals leave contamination unresolved. | [Assessment](results/qlp-faint-sector73-pilot-followup-20261010/239098567-peak0/ASSESSMENT.md) |

This index highlights selected unresolved leads; the retained assessments below include other unresolved signals and contamination findings. Catalog nonmatches do not establish novelty.

**Newer audited original-attempt snapshots:** [four-sector 974](results/qlp-faint-midradius-remaining-four-20261011/checkpoint-0974.json) (405 below threshold,
377 flagged, 192 failed); [three-sector 1,215](results/qlp-faint-midradius-remaining-three-20261011/checkpoint-1215.json) (891 below, 318 flagged, six failed);
[two-sector 3,223](results/qlp-faint-midradius-remaining-two-20261011/checkpoint-3223.json) (2,567 below, 619 flagged, 37 failed). These 5,412 distinct targets
are snapshots of the remaining campaigns. Recoveries are separate attempts for the
same stars; the older joined recovery count below has a narrower scope. Surveys remain active.

**Three-sector remaining batch completed:** [Terminal reconciliation](results/qlp-faint-midradius-remaining-three-20261011/joined-terminal.json) covers 1,493 distinct stars. Original attempts: 1,070 below threshold, 412 flagged, 11 failed. Six narrower-window recoveries and four unchanged network retries yield 1,078 below threshold, 414 flagged and one without usable coverage. Original errors remain retained; flagged results are not planet candidates. The two-sector search has also finished; see the reconciliation above.

**Four-sector remaining batch completed:** [Terminal audit](results/qlp-faint-midradius-remaining-four-20261011/terminal-verification.json) verifies all1,025original attempts and five follow-ups. Original counts:420below threshold,404flagged,201failed. After200baseline recoveries and the prior manual recovery counted once, [1,025distinct stars](results/qlp-faint-midradius-remaining-four-20261011/joined-1025.json) have usable windows:599below and426flagged. Original failures remain retained; no completeness or planet claim. The two-sector campaign has also finished; see the reconciliation above.

**Earlier search scope:** [The remaining 1,025 midradius four-sector targets](results/qlp-faint-midradius-remaining-four-20261011/ASSESSMENT.md)
were searched across 55 training-sector combinations, with distant
validation sectors reserved. The [audited 520-target snapshot](results/qlp-faint-midradius-remaining-four-20261011/joined-0520.json) has usable windows
for 519 distinct stars after separate recoveries: 320 below threshold and
199 flagged; one recovery remains pending in this snapshot. Its 88 original failures remain retained. Three signals reached
follow-up: all three are now artifact-suspect after source and quality checks.
Controls pass six of 24 injections, none Earth-sized. The survey and recovery
streams remain active; this is not whole-campaign completion.

**Latest completed recovery:** [Five shorter-window searches](results/qlp-faint-midradius-next32-recovery-pilot-20261011/ASSESSMENT.md)
all stayed below threshold. The preceding 32-star batch now has usable windows
for all 32 distinct stars: 19 below threshold and 13 disqualified. Its five
original four-sector failures remain documented separately. Recovery controls
passed 12 of 24 injections, all at two or three Earth radii; none Earth-sized.

**Additional sector coverage:** [A three-sector pilot](results/qlp-faint-midradius-three-pilot-20261011/ASSESSMENT.md)
completed 16 usable searches: nine below threshold and seven disqualified,
with no qualifying follow-up. Seven of 24 control injections pass, none
Earth-sized. The remaining 1,493 targets are now being searched in parallel
with the four-sector campaign. Its [235-target checkpoint](results/qlp-faint-midradius-remaining-three-20261011/checkpoint-0235.json)
contains 178 below-threshold and 57 flagged results, with only the already-reviewed
TIC 355707138 eligible for diagnostic follow-up. The
[metadata selection](results/qlp-faint-midradius-coverage-20261011/THREE_SECTOR_SELECTION.md)
contains 1,509 additional stars, disjoint from the four-sector tier; these are
search targets, not planet candidates.

**Two-sector extension piloted:** [16 additional targets](results/qlp-faint-midradius-two-pilot-20261011/ASSESSMENT.md)
produced 13 below-threshold and three flagged searches, with no eligible follow-up.
Controls passed 11 of 24 injections, all at two or three Earth radii; none Earth-sized.
The [frozen two-sector selection](results/qlp-faint-midradius-coverage-20261011/TWO_SECTOR_SELECTION.md)
contains 4,160 additional stars across 90 training-sector combinations, disjoint
from both earlier tiers. [The remaining 4,144-target search has finished](results/qlp-faint-midradius-remaining-two-20261011/ASSESSMENT.md).
Its first audited checkpoint has 43 below-threshold, nine flagged and one failed
attempt, with no eligible follow-up. Additional controls pass 8 of 24 injections,
all at two or three Earth radii; none Earth-sized.

**Radius-extension pilot reviewed:** [16 distinct stars now have usable search windows](results/qlp-faint-midradius-recovery-pilot-20261011/ASSESSMENT.md),
with nine below-threshold results and seven flagged signals. Five original
four-sector failures are retained alongside separate two-sector recovery attempts.
TIC 438792601 passed discovery screening, but raw Sectors 99 and 100 favor the
same off-target source group; no credible new planet candidate.
The broader [metadata selection](results/selection-faint-midradius-20261011/ASSESSMENT.md)
contains 1,073 four-sector targets. Recovery controls pass nine of 24 injections,
none Earth-sized. The next 32-star batch is now reviewed above.

**Distance-extension sample audited:** [13 usable searches from 15 pool stars](results/bright-outer-audit-20261011/ASSESSMENT.md)
yielded nine below-threshold results and four disqualified signals, with no
qualifying follow-ups. All reserved epochs remain unopened. The last two searches
recovered only one of 16 injected transits through screening and timing checks,
at three Earth radii. Two single-epoch stars remain unsearched. This scoped sample
does not exhaust TESS or establish completeness; no new credible candidate.

**Previous distance-extension search:** [Seven single-sector targets](results/qlp-bright-outer-one-pilot-20261011/ASSESSMENT.md)
yielded six below-threshold searches and one disqualified signal. All distant
validation sectors remain unopened. Only one of 24 in-range synthetic injections
passes, at three Earth radii, so sensitivity is weak. Two untouched stars with
one distant validation sector each are frozen next; no new credible candidate.

**Previous distance-extension search:** [Two-sector pilot](results/qlp-bright-outer-two-pilot-20261011/ASSESSMENT.md)
found no qualifying signal in TIC 406767596 or TIC 376405406. Their distant
validation observations remain unopened. Nine of 16 in-range synthetic injections
pass screening and timing, none Earth-sized. Seven untouched stars with single
discovery sectors and distant validation are frozen next.

**Previous distance-extension search:** [TIC 392763403](results/qlp-bright-outer-three-pilot-20261011/ASSESSMENT.md)
has a usable three-sector search but no qualifying peak; coverage, segment-edge
and consistency checks fail. All four distant validation sectors remain unopened.
Three of eight in-range injections pass screening and timing, none Earth-sized.
Two untouched targets with two-sector discovery baselines and distant validation
are frozen next. No new credible planet candidate is claimed.

**New distance extension:** [Bright small stars at 120–200 pc](results/selection-bright-outer-small-20261011/ASSESSMENT.md)
yielded 15 targets after metadata cuts and dated exclusions. The first
[four-sector search, TIC 239124404](results/qlp-bright-outer-four-pilot-20261011/ASSESSMENT.md),
failed consistency checks; neither distant reserved sector was opened. None of
eight in-range injected transits was recovered, limiting the null result.
TIC 392763403 is frozen next with three discovery sectors and four distant
reserved sectors. No new credible planet candidate is claimed.

**Latest source check:** [TIC 129577784 raw pixels](results/tesscut-129577784-s83-20261011/ASSESSMENT.md)
show weak, patchy residuals across 13 event windows. No host can be identified;
the signal remains an alias-suspect diagnostic. The requested SPOC pixel product
was unavailable (HTTP 404), with the failed check retained.

**Nearby-epoch tier complete:** [Audited 271 selected stars](results/near-epoch-tier-audit-20261011/ASSESSMENT.md)
across 16 batches: 266 usable searches and five retained failures. The final
[Sector 20 target](results/qlp-near-epoch-sector20-pilot-20261011/ASSESSMENT.md)
fell below threshold. TIC 129577784 remains an alias-suspect diagnostic; no credible
new candidate emerged. Of 320 synthetic trials, 302 were in range and 71 passed
screening and timing checks, only one Earth-sized. These controls do not measure
survey completeness. This exhausts this specific tier, not all TESS observations.

**Previous nearby-epoch attempt:** [Sector 26](results/qlp-near-epoch-sector26-pilot-20261011/ASSESSMENT.md)
has unusable discovery data for TIC 257531000: only 110 clean cadences, below the
required 200. This is not a nondetection; injections were not run. The tier now
totals 265 usable searches from 270 selected stars, with five failures retained.
One untouched target remains, frozen for Sector 20 next.

**Previous nearby-epoch search:** [Sector 54](results/qlp-near-epoch-sector54-pilot-20261011/ASSESSMENT.md)
adds one usable search below threshold. None of eight synthetic injections passes;
two long-period trials are outside the actual search grid. This weak sensitivity
does not exclude planets. The tier now totals 265 usable searches from 269 selected
stars. Two untouched targets remain, with the Sector 26 target frozen next.

**Previous nearby-epoch search:** [Sector 4](results/qlp-near-epoch-sector4-pilot-20261011/ASSESSMENT.md)
adds two usable searches, both below threshold. Two of 16 in-range synthetic
injections pass screening and timing, both two Earth radii. The tier now totals
264 usable searches from 268 selected stars. Three untouched targets remain,
with one Sector 54 target frozen next.

**Previous nearby-epoch search:** [Sector 32](results/qlp-near-epoch-sector32-pilot-20261011/ASSESSMENT.md)
adds three usable searches, all below threshold. Two of 24 in-range synthetic
injections pass screening and timing; neither is Earth-sized. The tier now totals
262 usable searches from 266 selected stars. Five untouched targets remain,
with two Sector 4 targets frozen next.

**Previous nearby-epoch search:** [Sector 104](results/qlp-near-epoch-sector104-pilot-20261011/ASSESSMENT.md)
adds three usable searches, all below threshold. Five of 24 in-range synthetic
injections pass screening and timing; none is Earth-sized. The tier now totals
259 usable searches from 263 selected stars. Eight untouched targets remain,
with three Sector 32 targets frozen next.

**Previous nearby-epoch search:** [Sector 18](results/qlp-near-epoch-sector18-pilot-20261011/ASSESSMENT.md)
adds four usable searches, all below threshold. Two of 24 in-range synthetic
injections pass screening and timing, both three Earth radii; sensitivity is weak.
The tier now totals 256 usable searches from 260 selected stars. Eleven untouched
targets remain, with three Sector 104 targets frozen next.

**Previous nearby-epoch search:** [Sector 45](results/qlp-near-epoch-sector45-pilot-20261011/ASSESSMENT.md)
adds five usable searches: four below threshold and one flagged, with no qualifying
follow-up signal. Eleven of 24 in-range synthetic injections pass screening and
timing; none is Earth-sized. The tier now totals 252 usable searches from 256
selected stars. Fifteen untouched targets remain, with four Sector 18 targets
frozen next.

**Previous nearby-epoch search:** [Sector 83](results/qlp-near-epoch-sector83-pilot-20261011/ASSESSMENT.md)
adds 11 usable searches. TIC 129577784 received diagnostic follow-up, but multiple
dips per selected cycle favor a period alias; reserved timing is inconclusive.
Four of 24 injections pass screening and timing; eight long trials are outside
the actual search grids. No new credible candidate. The tier now totals 247 usable
searches from 251 selected stars. Twenty untouched targets remain, with five
Sector 45 targets frozen next.

**Previous nearby-epoch search:** [Sector 79](results/qlp-near-epoch-sector79-pilot-20261011/ASSESSMENT.md)
adds 12 usable searches, all below threshold. Four of 24 in-range synthetic
injections pass screening and timing; none is Earth-sized. This limited sensitivity
does not exclude small planets. The tier now totals 236 usable searches from 240
selected stars. Thirty-one untouched targets remain, with 11 Sector 83 targets
frozen next.

**Previous nearby-epoch search:** [Sector 16](results/qlp-near-epoch-sector16-pilot-20261011/ASSESSMENT.md)
adds 13 usable searches: ten below threshold and three flagged, with no qualifying
follow-up signal. One of 24 synthetic injections passes (three Earth radii);
two long-period trials are outside the actual search grids. Sensitivity remains
weak. The tier now totals 224 usable searches from 228 selected stars. Forty-three
untouched targets remain, with 12 Sector 79 targets frozen next.

**Previous nearby-epoch search:** [Sector 92](results/qlp-near-epoch-sector92-pilot-20261011/ASSESSMENT.md)
adds 14 usable searches: ten below threshold and four flagged, with no qualifying
follow-up signal. None of 24 in-range synthetic injections passes screening;
poor sensitivity limits this null result. The tier now totals 211 usable searches
from 215 selected stars. Fifty-six untouched targets remain, with 13 Sector 16
targets frozen next.

**Previous nearby-epoch search:** [Sector 51](results/qlp-near-epoch-sector51-pilot-20261011/ASSESSMENT.md)
adds 18 usable searches from 21 targets: 17 below threshold, one flagged and three
unusable light curves. No qualifying follow-up signal. None of 24 synthetic
injections passes; six long-period trials lie outside the actual search grids.
Sensitivity is poor, so this null result does not exclude planets. The tier now
has 197 usable searches from 201 selected stars. Seventy untouched targets remain,
with 14 Sector 92 targets frozen next.

**Previous nearby-epoch search:** [Sector 71](results/qlp-near-epoch-sector71-pilot-20261011/ASSESSMENT.md)
adds 37 usable searches: 35 below threshold and two flagged, with no qualifying
follow-up signal. Eleven of 24 synthetic injections pass screening and timing;
none of the Earth-sized injections pass. The tier now totals 179 usable searches
from 180 selected stars. There are 91 untouched targets left, with 21 Sector 51
targets frozen next. These nearby epochs provide weaker replication than widely
separated observations.

**Previous nearby-epoch search:** [Sector 46](results/qlp-near-epoch-sector46-pilot-20261011/ASSESSMENT.md)
adds 61 usable searches from 62 selected stars: 56 below threshold, five flagged,
and one unusable light curve. No qualifying follow-up signal. Fourteen of 24
synthetic injections pass, none Earth-sized; this is not a completeness estimate.
The tier now totals 142 usable searches; 128 untouched targets remain, with 37
Sector 71 targets frozen next.

**New nearby-epoch tier:** [81 Sector 43 searches](results/qlp-near-epoch-sector43-pilot-20261011/ASSESSMENT.md),
69 below threshold and 12 flagged; no qualifying signal or data failure.
Ten of 24 in-range injections passed screening and timing, including one
Earth-radius trial. This tier reserves another nearby sector, which provides
weaker replication than a distant epoch. There are 190 untouched targets left.

**TIC 80387959 host test:** [28 event-level and omission checks](results/prf-80387959-event-stability-20261011/ASSESSMENT.md)
reproduce the original stacked fits but show host preferences changing in every
sector. This recurring signal remains unresolved; selective event removal does
not justify a planet claim.

**Campaign accounting:** [34,255 distinct selected stars](results/campaign-evidence-review-20261011/ASSESSMENT.md),
34,177 with usable searches after recovery and 78 remaining unusable.
This covers the two audited selection tiers, not all TESS data. Current
follow-up evidence and candidate-index links are verified; no securely
attributed new planet is established.

**Retrospective quality checks:** [three signals have processed-data concerns](results/retrospective-quality-check-20261011/ASSESSMENT.md).
Both supported events for TIC 288525984 and TIC 394050941 carry stray-light flags;
TIC 298551568 has one flagged event and weak support in the other reduction.
Products for two other signals were unavailable. No new planet candidate is established.

**Follow-up inventory reconciled:** [107 unique peaks across 95 stars](results/two-reserved-followup-audit-final-20261011/ASSESSMENT.md),
with duplicate records retained but counted once. No missing required artifact
or remaining gap under the current diagnostic rule. These are follow-up signals,
not confirmed planets; timing and source-attribution limitations remain.

**Retrospective follow-up gaps:** [six early peaks checked](results/qlp-faint-retrospective-gap-followup-20261011/terminal.json).
All twelve reserved-sector timing tests remain inconclusive because the training
signals have only two supported events. Plots and individual assessments are
retained; no candidate is promoted and source attribution remains unresolved.

**Earlier-tier coverage audit:** [28,049 selected targets accounted for](results/two-reserved-tier-audit-20261011/ASSESSMENT.md),
with 28,015 stars yielding usable searches after recovery and 34 remaining
unusable. Alternate-sector recovery plans preserve the original reserved lists
without training overlap. Original failures remain retained; these counts do
not establish survey completeness.

**Completed exploratory-tier audit:** [66 batches reconciled](results/one-reserved-tier-audit-20261011/ASSESSMENT.md):
6,206 distinct selected stars, 6,162 usable searches after recovery and
44 unresolved data failures. Evidence for 25 follow-up peaks is retained;
these are not 25 planet candidates. No new securely attributed planet emerged.
This is a scoped evidence audit, not survey completeness.

**Exploratory Sector 35:** [one usable search](results/qlp-faint-one-reserved-sector35-pilot-20261010/ASSESSMENT.md),
below threshold. None of eight in-range injections passed screening.
The [scoped inventory](results/qlp-faint-one-reserved-after35-20261010/coverage.json)
now has zero untouched stars meeting the reserved-epoch rule: 34,255 historically
selected, 3,677 lacking a distant reserved epoch, and 890 without products in
the 38,822-star snapshot. Selection counts do not imply usable searches or
survey completeness. Existing unresolved signals still require investigation.

**Exploratory Sector 46:** [one usable search](results/qlp-faint-one-reserved-sector46-pilot-20261010/ASSESSMENT.md),
below threshold. None of eight in-range injections was recovered, so the null
cannot rule out planets. The last untouched star in this scoped sample is
selected in Sector 35; this is not an exhaustive search of all TESS data.

**Exploratory Sector 81:** [one usable search](results/qlp-faint-one-reserved-sector81-pilot-20261010/ASSESSMENT.md),
below threshold. None of eight in-range injections was recovered, so this
null cannot rule out planets. Sector 46 has one untouched target selected next.

**Exploratory Sector 102:** [one usable search](results/qlp-faint-one-reserved-sector102-pilot-20261010/ASSESSMENT.md),
below threshold. Corrected controls yielded one screening and timing pass
from eight in-range injections; no Earth-radius pass. Failed wrapper runs
are retained. Limited sensitivity constrains the null; Sector 81 is selected next.

**Exploratory Sector 3:** [two usable searches](results/qlp-faint-one-reserved-sector3-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. One of 12 in-range injections
passed screening and timing; four trials were outside the grid. No Earth-radius
pass; limited sensitivity constrains the null. Sector 102 has one untouched target selected next.

**Exploratory Sector 15:** [two usable searches](results/qlp-faint-one-reserved-sector15-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. None of 12 in-range injections
was recovered; four additional trials were outside the grid. This null
cannot rule out planets. Sector 3 has two untouched targets selected next.

**Exploratory Sector 33:** [two usable searches](results/qlp-faint-one-reserved-sector33-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. None of 16 in-range injections
was recovered at its period or passed screening; the null cannot rule out planets.
Sector 15 has two untouched targets selected next.

**Exploratory Sector 73:** [two usable searches](results/qlp-faint-one-reserved-sector73-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. None of 16 in-range injections
passed screening, so the null result cannot rule out planets.
Sector 33 has two untouched targets selected next.

**Exploratory Sector 100:** [two usable searches](results/qlp-faint-one-reserved-sector100-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. One of 12 in-range injections
passed screening and timing; four longer-period trials were outside the grid.
No Earth-radius pass; poor sensitivity limits the null result.
Sector 73 has two untouched targets selected next.

**Exploratory Sector 103:** [two usable searches](results/qlp-faint-one-reserved-sector103-pilot-20261010/ASSESSMENT.md),
both below threshold, with no data failure. One of 16 in-range injections
passed screening and timing; no Earth-radius pass. Poor sensitivity limits
the null result. Sector 100 has two untouched targets selected next.

**Exploratory Sector 27:** [three usable searches](results/qlp-faint-one-reserved-sector27-pilot-20261010/ASSESSMENT.md),
two below threshold and one flagged; no qualifying signal or data failure.
None of 24 in-range injections passed screening, so poor sensitivity limits
this null result. Sector 103 has two untouched targets selected next.

**Exploratory Sector 90:** [three usable searches](results/qlp-faint-one-reserved-sector90-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Three of 24 in-range injections
passed screening and timing; no Earth-radius pass. Limited sensitivity
constrains the null result. Sector 27 has three untouched targets selected next.

**Exploratory Sector 89:** [four usable searches](results/qlp-faint-one-reserved-sector89-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Only one of 24 in-range injections
passed screening and timing; no Earth-radius pass. Poor recovery limits the
null result. Sector 90 has three untouched targets selected next.

**Exploratory Sector 93:** [four usable searches](results/qlp-faint-one-reserved-sector93-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Two of 24 in-range injections passed
screening and timing; no Earth-radius pass. Poor sensitivity limits the null
result. Sector 89 has four untouched targets selected next.

**Exploratory Sector 99 (one reserved epoch):** [five usable searches](results/qlp-faint-one-reserved-sector99-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Three of 18 in-range injections passed
screening and timing; no Earth-radius pass. Six longer-period trials were
outside the grids. Sector 93 has four untouched targets selected next.

**Exploratory Sector 22:** [six usable discovery searches](results/qlp-faint-one-reserved-sector22-pilot-20261010/ASSESSMENT.md),
one follow-up signal favoring neighboring-source contamination. Reserved data
could not test recurrence. Five of 24 in-range injections passed screening
and timing; no Earth-radius pass. Sector 99 has five untouched targets next.

**Exploratory Sector 53:** [seven usable searches](results/qlp-faint-one-reserved-sector53-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. None of 24 in-range injections
passed screening; poor sensitivity materially limits this null result.
Sector 22 has six untouched targets selected next.

**Exploratory Sector 88:** [seven usable searches](results/qlp-faint-one-reserved-sector88-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Eight of 24 in-range injections
passed screening and timing; no Earth-radius pass. No completeness claim.
Sector 53 has seven untouched targets selected next.

**Exploratory Sector 36:** [eight usable searches](results/qlp-faint-one-reserved-sector36-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Three of 24 in-range injections
passed screening and timing, all in one control star; no Earth-radius pass.
Limited sensitivity constrains the null result. Sector 88 has seven untouched targets next.

**Exploratory Sector 37:** [seven usable searches from eight attempts](results/qlp-faint-one-reserved-sector37-pilot-20261010/ASSESSMENT.md),
no qualifying signal. One unusable QLP file also lacked a same-sector SPOC
product; it is not a nondetection. Five of 24 in-range injections passed
screening and timing; no Earth-radius pass. Sector 36 has eight untouched targets next.

**Exploratory Sector 39:** [eight usable searches](results/qlp-faint-one-reserved-sector39-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Only one of 24 in-range injections
passed screening and timing; no Earth-radius pass. Poor recovery materially
limits the null result. Sector 37 has eight untouched targets selected next.

**Exploratory Sector 71:** [eight usable searches](results/qlp-faint-one-reserved-sector71-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Only one of 24 in-range injections
passed screening and timing; no Earth-radius pass. Poor recovery materially
limits the null result. Sector 39 has eight untouched targets selected next.

**Exploratory Sector 83:** [eight usable searches](results/qlp-faint-one-reserved-sector83-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Six of 24 in-range injections passed
screening and timing; no Earth-radius pass. Limited sensitivity constrains
the null result. Sector 71 has eight untouched targets selected next.

**Exploratory Sector 38:** [nine usable searches](results/qlp-faint-one-reserved-sector38-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Five of 24 in-range injections passed
screening and timing; no Earth-radius pass. Limited sensitivity constrains
the null result. Sector 83 has eight untouched targets selected next.

**Exploratory Sector 96:** [nine usable searches](results/qlp-faint-one-reserved-sector96-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Visual review supports retaining a
deep eclipse-like signal's rejection. Four of 24 in-range injections passed
screening and timing; no Earth-radius pass. Sector 38 has nine untouched targets next.

**Exploratory Sector 75:** [nine usable searches from ten attempts](results/qlp-faint-one-reserved-sector75-pilot-20261010/ASSESSMENT.md),
no qualifying signal. One unusable QLP file also lacked a same-sector SPOC
product; it is not a nondetection. Four of 16 completed injections passed
screening and timing; eight planned trials were unavailable. No Earth-radius
pass. Sector 96 has nine untouched targets selected next.

**Exploratory Sector 17 (one reserved epoch):** [eleven usable searches](results/qlp-faint-one-reserved-sector17-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Six of 18 in-range injections passed
screening and timing; no Earth-radius pass. Six longer-period trials were
outside the grids. Sector 75 has ten untouched targets selected next.

**Exploratory Sector 79:** [eleven usable searches](results/qlp-faint-one-reserved-sector79-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Three of 24 in-range injections
passed screening and timing; no Earth-radius pass. Limited sensitivity
constrains the null result. Sector 17 has eleven untouched targets selected next.

**Exploratory Sector 13:** [14 usable searches](results/qlp-faint-one-reserved-sector13-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Four of 24 in-range injections passed
screening and timing; no Earth-radius pass. Limited sensitivity constrains
the null result. Sector 79 has eleven untouched targets selected next.

**Exploratory Sector 24:** [15 usable searches](results/qlp-faint-one-reserved-sector24-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Visual review supports retaining a
strong peak's inconsistent-depth rejection. Seventeen of 24 in-range injections
passed screening and timing; no Earth-radius pass. Sector 13 has 14 untouched targets next.

**Exploratory Sector 95:** [16 usable searches](results/qlp-faint-one-reserved-sector95-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. Three of 12 in-range injections
passed screening and timing; no Earth-radius pass. All 12 longer-period
trials were outside the search grids. Sector 24 has 15 untouched targets selected next.

**Exploratory Sector 77:** [17 usable searches](results/qlp-faint-one-reserved-sector77-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures. None of 24 in-range injections
passed screening; poor sensitivity materially limits this null result.
Sector 95 has 16 untouched targets selected next.

**Exploratory Sector 80 (one reserved epoch):** [19 usable searches](results/qlp-faint-one-reserved-sector80-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Nine of 24 in-range injections passed
screening and timing; no Earth-radius pass. No completeness claim.
Sector 77 has 17 untouched targets selected next.

**Exploratory Sector 59:** [20 usable searches](results/qlp-faint-one-reserved-sector59-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Visual review supports retaining a
broad-modulation rejection. Five of 24 in-range injections passed screening
and timing; no Earth-radius pass. Sector 80 has 19 untouched targets selected next.

**Exploratory Sector 70:** [25 usable searches](results/qlp-faint-one-reserved-sector70-pilot-20261010/ASSESSMENT.md),
all below threshold, with no data failures or qualifying signals. Six of 24
in-range injections passed screening and timing; none at Earth's radius.
No completeness claim. Sector 59 has 20 untouched targets selected next.

**Exploratory Sector 25:** [28 usable searches](results/qlp-faint-one-reserved-sector25-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Only one of 18 in-range injections
passed screening and timing; no Earth-radius pass. Six longer-period trials
were outside the search grid. Limited sensitivity constrains this null result.
Sector 70 has 25 untouched targets selected next.

**Exploratory Sector 28:** [29 usable searches](results/qlp-faint-one-reserved-sector28-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. A strong rejected peak is dominated by
irregular deep deficits. Seven of24 injections passed screening and timing;
no Earth-radius pass. Sector25 has28 untouched targets selected next.

**Exploratory Sector 64:** [33 usable searches](results/qlp-faint-one-reserved-sector64-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Seven of24 in-range injections passed
screening and timing; no Earth-radius trial passed. No completeness claim.
Sector28 has29 untouched targets selected next.

**Exploratory Sector 98 (one reserved epoch):** [37 usable searches](results/qlp-faint-one-reserved-sector98-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Seventeen of 24 in-range injections
passed screening and timing, including one Earth-radius trial. No completeness
claim. Sector 64 has 33 untouched targets selected next.

**Exploratory Sector 65:** [38 usable searches](results/qlp-faint-one-reserved-sector65-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Eight of 24 in-range injections passed
screening and timing; no Earth-radius trial passed. No completeness claim.
Sector 98 has 37 untouched targets selected next.

**Exploratory Sector 34:** [40 usable searches](results/qlp-faint-one-reserved-sector34-pilot-20261010/ASSESSMENT.md),
one signal favoring contamination from a known neighboring eclipsing system.
Four of 24 in-range injections passed screening and timing; no Earth-radius
trial passed. Sector 65 has 38 untouched targets selected next.

**Exploratory Sector 92:** [40 usable searches](results/qlp-faint-one-reserved-sector92-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Only four of 24 in-range injections
passed screening and timing; no Earth-radius trial passed. Limited sensitivity,
not an exclusion of small planets. Sector 34 has 40 untouched targets selected next.

**Exploratory Sector 19:** [50 usable searches](results/qlp-faint-one-reserved-sector19-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Eight of 24 in-range injections passed
screening and timing; no Earth-radius trial passed. No completeness claim.
Sector 92 has 40 untouched targets selected next.

**Exploratory Sector 29:** [52 usable searches, one data failure](results/qlp-faint-one-reserved-sector29-pilot-20261010/ASSESSMENT.md),
no qualifying signal. Eleven of 24 in-range injections passed screening and
timing; no Earth-radius trial passed. No completeness claim.
Sector 19 has 50 untouched targets selected next.

**Exploratory Sector 60:** [54 usable searches](results/qlp-faint-one-reserved-sector60-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Eleven of 24 in-range injections passed
screening and timing; no Earth-radius trial passed. No completeness claim.
Sector 29 has 53 untouched targets selected next.

**Exploratory Sector 18:** [60 usable searches](results/qlp-faint-one-reserved-sector18-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Nine of 18 in-range injections passed
screening and timing, including two Earth-radius trials; six trials were
outside the grid. Sector 60 has 54 untouched targets selected next.

**Exploratory Sector 87:** [62 usable searches](results/qlp-faint-one-reserved-sector87-pilot-20261010/ASSESSMENT.md),
one signal favoring neighboring-source contamination and no data failures.
Eight of 24 in-range injections passed screening and timing; no Earth-radius
trial passed. Sector 18 has 60 untouched targets selected next.

**Exploratory Sector 72:** [67 usable searches](results/qlp-faint-one-reserved-sector72-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Five of 18 in-range injections passed
screening and timing, including one Earth-radius trial; six longer-period
trials were outside the grid. Sector 87 has 62 untouched targets selected next.

**Exploratory Sector 97:** [69 usable searches](results/qlp-faint-one-reserved-sector97-pilot-20261010/ASSESSMENT.md),
two unresolved diagnostic signals, neither securely attributed to a transit.
Twenty of 24 in-range injections passed screening and timing; two were
Earth-radius trials. No completeness claim. Selection provenance was corrected
and independently verified; Sector 72 has 67 untouched targets selected next.

**Exploratory Sector 78:** [83 usable searches, one data failure](results/qlp-faint-one-reserved-sector78-pilot-20261010/ASSESSMENT.md),
no qualifying signal. Four of 12 in-range injections passed screening and
timing; all 12 longer-period trials were outside the search grid.
No completeness claim. Sector 97 has 69 untouched targets selected next.

**Exploratory Sector 85:** [96 usable searches](results/qlp-faint-one-reserved-sector85-pilot-20261010/ASSESSMENT.md),
one signal favoring neighboring-source contamination and no data failures.
Six of 24 in-range injections passed screening and timing; no Earth-radius
trial passed. No completeness claim. Sector 78 has 84 untouched targets selected next.

**Exploratory Sector 67:** [110 usable searches](results/qlp-faint-one-reserved-sector67-pilot-20261010/ASSESSMENT.md),
one signal favoring neighboring-source contamination and no data failures.
Eight of 24 in-range injections passed screening and timing; no Earth-radius
trial passed. No completeness claim. Sector 85 has 96 untouched targets selected next.

**Exploratory Sector 6 (one reserved epoch):** [116 usable searches](results/qlp-faint-one-reserved-sector6-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Ten of 18 in-range injections passed
screening and timing; six longer trials were outside their search grids.
No Earth-radius trial passed and no completeness claim is made.
Sector 67 results are recorded above.

**Exploratory Sector 84:** [179 usable searches](results/qlp-faint-one-reserved-sector84-pilot-20261010/ASSESSMENT.md),
one signal favoring neighboring-source contamination and no data failures. Nine of 24 in-range injections
passed screening and timing; no Earth-radius trial passed. No completeness claim.
The separate one-reserved Sector 6 results are recorded above.

**Exploratory Sector 47:** [190 attempted targets, 185 usable searches](results/qlp-faint-one-reserved-sector47-pilot-20261010/ASSESSMENT.md),
five explicit data failures and no qualifying signal. Twenty-one of 24 in-range
injections passed screening and timing, including three Earth-radius trials on
two stars. This is not a completeness estimate. Sector 84 results are recorded above.

**Exploratory Sector 30:** [201 usable searches](results/qlp-faint-one-reserved-sector30-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Six strong flagged dips concentrate in a
shared detector/time interval; their fitted periods are not supported.
Nine of 24 in-range injections passed screening and timing, including one
Earth-radius trial. No completeness claim. Sector 47 results are recorded above.

**Exploratory Sector 32:** [230 usable searches](results/qlp-faint-one-reserved-sector32-pilot-20261010/ASSESSMENT.md),
no qualifying signal or data failure. Visual checks support variability/eclipsing-
system flags on two strong signals. Nine of 24 in-range injections passed screening
and timing, including one Earth-radius trial; no completeness claim.
Sector 30 results are recorded above.

**Exploratory Sector 42:** [284 attempted targets, 279 usable searches](results/qlp-faint-one-reserved-sector42-pilot-20261010/ASSESSMENT.md),
with five explicit data failures and no qualifying signal. Only one of 24
in-range injections passed screening and timing; no Earth-radius trial passed.
This null result cannot rule out planets. Sector 32 results are recorded above.

**Exploratory Sector 54:** [308 attempted targets, 293 usable searches](results/qlp-faint-one-reserved-sector54-pilot-20261010/ASSESSMENT.md)
and 15 explicit data failures. One two-event diagnostic remains unresolved; no
credible planet candidate. Seven of 20 in-range injections passed screening and
timing; four other trials were outside their search grids. No completeness claim.
Sector 42 results are recorded above.

**Exploratory Sector 49:** [339 targets attempted, 331 usable searches](results/qlp-faint-one-reserved-sector49-pilot-20261010/ASSESSMENT.md),
including one recovered through SPOC. Eight data failures remain explicit. No
qualifying signal. Nine of 24 in-range injections passed screening and timing;
none of the Earth-radius trials passed. No completeness or planet-exclusion claim.
Sector 54 results are recorded above.

**Exploratory Sector 91:** [463 usable searches](results/qlp-faint-one-reserved-sector91-pilot-20261010/ASSESSMENT.md).
The main lead above favors contamination. Nine additional two-event peaks on eight
stars favor shared systematics: their final events cluster within two hours across
nearly 22 degrees of sky. [All diagnostic leads and limitations](results/qlp-faint-one-reserved-sector91-gap-diagnostic-20261010/ASSESSMENT.md)
are retained; none is promoted to a planet candidate. Seven of 24 in-range control
injections passed screening and timing, including one Earth-radius trial. No
completeness claim. Sector 49 results are recorded above.

**Exploratory Sector 48:** 481 attempted targets, 475 usable searches and six
explicit data failures. TIC 1044290 favors neighboring-source contamination after vetting. Ten of 24 in-range
control injections passed screening and timing, including two Earth-radius trials
on one star; this is not a completeness estimate.

**Exploratory Sector 55:** 486 usable searches yielded three signals for review.
TIC 466895419 remains unresolved after pixel checks; the other two signals
favor neighboring-source contamination. Three of 24 in-range control injections passed
screening and timing, all at 0.83 days and two Earth radii. No completeness claim.

**Exploratory Sector 23:** 521 usable searches, with one detrending-sensitive
diagnostic signal (TIC 390650992) now favoring neighboring-source contamination. Seven of 24 in-range
injections passed screening and timing, all at short periods; none of the longer-period
controls passed. This does not establish completeness.

**Exploratory Sector 56:** all 555 target searches are usable. The one qualifying
signal, TIC 44345170, favors neighboring-source contamination after pixel vetting,
as recorded above. Nine of 24 in-range control injections
passed screening and timing; this is not a completeness estimate.

**Exploratory Sector 31:** [632 targets attempted, 631 usable searches](results/qlp-faint-one-reserved-sector31-pilot-20261010/ASSESSMENT.md),
with no qualifying signal. TIC 23221841 remains a data failure (unusable QLP flux,
SPOC unavailable). Ten of 24 in-range control injections passed screening and timing,
including two Earth-radius cases at 0.83 days; this is not a completeness estimate.
Sector 56 is selected next with 555 untouched targets and one distant reserved sector each.

**Sector 6:** [the selected star has a usable search](results/qlp-faint-sector6-pilot-20261010/ASSESSMENT.md).
TIC 7445283 stayed below threshold. None of six in-range injections passed
screening. The current pool has no untouched targets satisfying the two-distant-sector
reservation rule; a [separate exploratory inventory](results/qlp-faint-one-reserved-inventory-20261010/coverage.json)
contains 6,206 stars with one distant reserved sector, offering weaker replication.
This is neither all-TESS coverage nor evidence of an absence of planets.

**Sector 18:** [the selected star has a usable search](results/qlp-faint-sector18-pilot-20261010/ASSESSMENT.md).
TIC 256613012 stayed below threshold. None of eight in-range injections
passed both screening and timing checks; this does not rule out planets.

**Sector 34:** [the selected star has a usable search](results/qlp-faint-sector34-pilot-20261010/ASSESSMENT.md).
TIC 154365483 stayed below threshold. None of eight in-range injections was
recovered; this null result cannot rule out planets.

**Sector 45:** [the selected star has a usable search](results/qlp-faint-sector45-pilot-20261010/ASSESSMENT.md).
TIC 87477378 stayed below threshold. Three of eight in-range injections passed
screening and timing checks, none at Earth radius; sensitivity remains limited.

**Sector 46:** [the selected star has a usable search](results/qlp-faint-sector46-pilot-20261010/ASSESSMENT.md).
TIC 184871870’s peaks failed screening. None of eight in-range injections was
recovered; the null result cannot establish absence of planets.

**Sector 48:** [the selected star has a usable search](results/qlp-faint-sector48-pilot-20261010/ASSESSMENT.md).
TIC 159158711’s peak failed screening. Two of eight in-range injections passed
screening and timing checks, both at three Earth radii; sensitivity remains limited.

**Sector 65:** [TIC 208025086’s 2.85446-day signal favors neighboring eclipsing-source contamination](results/qlp-faint-sector65-pilot-followup-20261010/208025086-peak0/ASSESSMENT.md).
The image residual lies about 3.4 pixels off target; nearby TIC 208024999 is a Gaia
eclipsing binary, and neighboring apertures show deeper dips. The exact blend remains
unresolved; no new planet candidate is promoted. None of eight injections was recovered.

**Sector 84:** [the selected star has a usable search](results/qlp-faint-sector84-pilot-20261010/ASSESSMENT.md).
TIC 240783787 stayed below threshold. None of eight in-range injections was
recovered; this null result cannot rule out planets.

**Sector 15:** [both selected stars have usable searches](results/qlp-faint-sector15-pilot-20261010/ASSESSMENT.md).
Both stayed below threshold. None of 16 injections passed screening; four
longer-period trials were outside the actual grids. Sensitivity limits remain explicit.

**Sector 85:** [both selected stars have usable searches](results/qlp-faint-sector85-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. None of 16 injections passed both screening
and the fixed phase check; one period-based screen pass narrowly failed timing.

**Sector 4:** [all three selected stars have usable searches](results/qlp-faint-sector4-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. One of 24 in-range injections passed the noncrowding
screen, at two Earth radii; sensitivity remains limited.

**Sector 36:** [all three selected stars have usable searches](results/qlp-faint-sector36-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. One of 24 in-range injections passed the noncrowding
screen, at three Earth radii; this null result cannot establish absence of planets.

**Sector 78:** [all three selected stars have usable searches](results/qlp-faint-sector78-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. No short-period injection passed screening; all 12
longer-period trials were outside the actual search grids and cannot measure sensitivity there.

**Sector 43:** [three of four selected stars have usable searches](results/qlp-faint-sector43-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. TIC 257867767 has unusable QLP data and no
available SPOC product. Both injection runs stopped at that star; missing trials remain explicit.

**Sector 54:** [all four selected stars have usable searches](results/qlp-faint-sector54-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up; two flagged stars each have only one supported event.
None of 24 injections passed, including 22 within the actual search grids.

**Sector 59:** [all four selected stars have usable searches](results/qlp-faint-sector59-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. TIC 458970710 has one supported event amid
extreme irregular variability, not a validated period. Four of 24 injections passed, all on one star.

**Sector 83:** [all four selected stars have usable searches](results/qlp-faint-sector83-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. Five of 24 in-range injections passed the
noncrowding screen, none at Earth radius; sensitivity remains limited.

**Sector 89:** [all four selected stars have usable searches](results/qlp-faint-sector89-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. Two of 24 in-range injections passed the noncrowding
screen, both on one star; sensitivity remains limited.

**Sector 24:** [all six selected stars have usable searches](results/qlp-faint-sector24-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. None of 24 in-range injections passed the
noncrowding screen; the null result cannot establish absence of planets.

**Sector 77:** [all seven selected stars have usable searches](results/qlp-faint-sector77-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. None of 24 in-range injections was recovered,
so the null result has poor sensitivity support.

**Sector 79:** [all seven selected stars have usable searches](results/qlp-faint-sector79-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. None of 24 in-range injections passed the full
noncrowding screen, limiting interpretation of this null result.

**Sector 25:** [all eight selected stars have usable searches](results/qlp-faint-sector25-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. One of 24 injections passed; four longer-period
trials were outside the actual search grids. Sensitivity limits remain explicit.

**Sector 67:** [all eight selected stars have usable searches](results/qlp-faint-sector67-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. Eight of 24 injections passed the noncrowding screen,
including one Earth-radius trial; uneven sensitivity prevents completeness claims.

**Sector 12:** [all nine selected stars have usable searches](results/qlp-faint-sector12-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. None of 24 in-range injections was recovered,
so this null result has particularly poor sensitivity support.

**Sector 32:** [all nine selected stars have usable searches](results/qlp-faint-sector32-pilot-20261010/ASSESSMENT.md).
No signal passed the screening criteria. TIC 30943870 shows broad periodic variability,
with its large-duty-cycle flag retained. Four of 24 injections passed, none at Earth radius.

**Sector 33:** [all nine selected stars have usable searches](results/qlp-faint-sector33-pilot-20261010/ASSESSMENT.md).
All stayed below threshold. Six of 24 injections passed the noncrowding screen,
none at Earth radius; this null result does not rule out smaller planets.

**Sector 42:** [all nine selected stars have usable searches](results/qlp-faint-sector42-pilot-20261010/ASSESSMENT.md).
No signal qualified for follow-up. Only three of 24 injections passed the
noncrowding screen, all at three Earth radii; smaller-planet sensitivity was poor.

**Sector 82:** [all 11 selected stars have usable searches](results/qlp-faint-sector82-pilot-20261010/ASSESSMENT.md).
All stayed below the screening threshold. Twelve of 24 injections passed
the full noncrowding screen, but none at Earth radius; this does not rule out planets.

**Sector 44:** [all 13 selected stars have usable searches](results/qlp-faint-sector44-pilot-20261010/ASSESSMENT.md).
All stayed below the screening threshold. Only four of 24 injections passed
the full screen; sensitivity limits prevent completeness claims.

**Sector 49:** [12 of 13 selected stars have usable searches](results/qlp-faint-sector49-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. TIC 165463961 has unusable QLP data
and no available SPOC product; both injection runs stopped at that star after eight trials.
Missing trials and sensitivity limits are retained explicitly.

**Sector 74:** [all 13 selected stars have usable searches](results/qlp-faint-sector74-pilot-20261010/ASSESSMENT.md).
All stayed below the screening threshold. No Earth-radius injection passed;
sensitivity limits prevent completeness or absence-of-planets claims.

**Sector 80:** [all 13 selected stars have usable searches](results/qlp-faint-sector80-pilot-20261010/ASSESSMENT.md).
[TIC 359659538](results/qlp-faint-sector80-pilot-followup-20261010/359659538-peak0/ASSESSMENT.md)
has an unresolved 2.44439-day signal (31,109 ± 1,587 ppm; five supported events).
Later-sector timing is inconclusive; an all-negative difference image cannot identify
a dimming host. No planet candidate is promoted. None of 24 injections passed screening.

**Sector 81:** [all 13 selected stars have usable searches](results/qlp-faint-sector81-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. None of 24 in-range injections
passed the full screen, sharply limiting interpretation of this null result.

**Sector 9:** [all 14 selected stars have usable searches](results/qlp-faint-sector9-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; the null result does not establish completeness.

**Sector 29:** [all 14 selected stars have usable searches](results/qlp-faint-sector29-pilot-20261010/ASSESSMENT.md).
All stayed below the screening threshold. Only three of 24 injections passed
the full screen; sensitivity limits prevent completeness claims.

**Sector 13:** [all 16 selected stars have usable searches](results/qlp-faint-sector13-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; the null result does not establish completeness.

**Sector 23:** [all 18 selected stars have usable searches](results/qlp-faint-sector23-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. None of 24 in-range injections
passed the full screen, sharply limiting interpretation of this null result.

**Sector 30:** [all 21 selected stars have usable searches](results/qlp-faint-sector30-pilot-20261010/ASSESSMENT.md).
All stayed below the screening threshold. No Earth-radius injection passed;
sensitivity limits prevent completeness or absence-of-planets claims.

**Sector 3:** [all 25 selected stars have usable searches](results/qlp-faint-sector3-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. One Earth-radius injection passed;
half the longer-period controls were outside the search grid. Completeness is not established.

**Sector 95:** [all 27 selected stars have usable searches](results/qlp-faint-sector95-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. One Earth-radius injection passed,
but all longer-period controls were outside the search grid; completeness is not established.

**Sector 41:** [all 30 selected stars have usable searches](results/qlp-faint-sector41-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; the null result does not establish completeness.

**Sector 5:** [all 38 selected stars have usable searches](results/qlp-faint-sector5-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; sensitivity varies between stars and completeness is not established.

**Sector 22:** [all 40 selected stars have usable searches](results/qlp-faint-sector22-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; the null result does not establish completeness.

**Sector 93:** [all 44 selected stars have usable searches](results/qlp-faint-sector93-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius injection passed
screening; sensitivity is uneven and the null result does not establish completeness.

**Sector 53:** [all 51 selected stars have usable searches](results/qlp-faint-sector53-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. No Earth-radius or longer-period
injection passed screening; the null result does not establish completeness.

**Sector 57:** [all 53 selected stars have usable searches](results/qlp-faint-sector57-pilot-20261010/ASSESSMENT.md).
[TIC 317166760](results/qlp-faint-sector57-pilot-followup-20261010/317166760-peak0/ASSESSMENT.md)
has an unresolved 0.77053-day signal (4,037 ± 434 ppm; 14 supported events).
Earlier-sector timing is inconclusive and weak, patchy pixel residuals do not establish
a host. No planet candidate is promoted; no Earth-radius injection passed screening.

**Sector 37:** [59 of 60 selected stars have usable searches](results/qlp-faint-sector37-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. TIC 98040225 remains unsearched
because its QLP flux is unusable and the alternate product is unavailable.
No Earth-radius injection passed screening; sensitivity limits remain explicit.

**Sector 61:** [all 68 selected stars have usable searches](results/qlp-faint-sector61-pilot-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. Injection recovery was uneven,
with no Earth-radius screen pass; this is not an absence-of-planets claim.

**Sector 73:** [all 90 selected stars were searched](results/qlp-faint-sector73-pilot-20261010/ASSESSMENT.md).
[TIC 239098567](results/qlp-faint-sector73-pilot-followup-20261010/239098567-peak0/ASSESSMENT.md)
has an unresolved 1.75685-day signal (7,714 ± 724 ppm; eight supported events).
The image residual is displaced and structured; earlier-sector timing is inconclusive.
No secure host or planet candidate is established. No Earth-radius injection passed.

**Sector 21 extension:** [all 110 selected stars have usable searches](results/qlp-faint-sector21-expanded-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal; final inventory checks passed.
Only one Earth-radius injection passed screening. Uneven sensitivity prevents
completeness or absence-of-planets claims.

**Sector 92 extension:** [all 130 selected stars have usable searches](results/qlp-faint-sector92-expanded-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal; final inventory checks passed.
No Earth-radius injection passed screening, so this null result does not exclude
smaller planets or establish completeness.

**Sector 90 extension:** [all 142 selected stars have usable searches](results/qlp-faint-sector90-expanded-20261010/ASSESSMENT.md).
The pilot found [TIC 89858935](results/qlp-faint-sector90-pilot-followup-20261010/89858935-peak0/ASSESSMENT.md),
a 2.93924-day signal favoring neighboring-source contamination near TIC 89858912.
No planet candidate is promoted. The expansion found no additional lead; final
inventory checks passed. Sensitivity and exact-source limitations remain explicit.

**Sector 31 extension:** [all 148 selected stars have usable searches](results/qlp-faint-sector31-expanded-20261010/ASSESSMENT.md).
[TIC 170590556](results/qlp-faint-sector31-pilot-followup-20261010/170590556-peak0/ASSESSMENT.md)
has an unresolved 1.24232-day signal. Its image residual is displaced from the
target, its depth depends strongly on processing, and recurrence tests are
timing-inconclusive. No planet candidate is promoted. The expansion found no
additional lead; final inventory checks passed.

**Sector 71 extension:** [186 of 189 selected stars have usable searches](results/qlp-faint-sector71-expanded-20261010/ASSESSMENT.md).
Both diagnostic fits on TIC 408642351 remain unresolved, with image/background
artifacts favored. The 5.29464-day fit failed both reserved-epoch predictions;
the 5.42912-day fit is timing-inconclusive. No planet candidate is promoted.
Three targets remain incomplete; final inventory checks passed.

**Sector 51 extension:** [211 of 215 selected stars have usable searches](results/qlp-faint-sector51-expanded-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. Four targets remain incomplete
after failed same-sector recovery attempts; these are not nondetections. Final
inventory checks passed. Controls retain weak sensitivity, including six
long-period trials outside the actual search grid.

**Sector 11 extension:** [all 252 selected stars have usable searches](results/qlp-faint-sector11-expanded-20261010/ASSESSMENT.md).
Neither follow-up policy found an eligible signal. Final inventory checks passed.
Sensitivity remains limited: no Earth-radius injection passed screening, and only
one of 12 longer-period trials passed. This does not exclude undetected planets.

**Sector 56 extension:** [all 270 selected stars have usable searches](results/qlp-faint-sector56-expanded-20261010/ASSESSMENT.md).
All three signals favor neighboring-source contamination. [TIC 387852102](results/qlp-faint-sector56-followup-20261010/387852102-peak0/ASSESSMENT.md)
has a 0.983665-day signal near a known Gaia eclipsing binary with twice that period.
[TIC 258733992](results/qlp-faint-sector56-followup-20261010/258733992-peak0/ASSESSMENT.md)
has a 3.448869-day signal localized near TIC 283675753; its physical class remains
unconfirmed. Pilot TIC 164146861 also favors a neighboring source. No planet
candidate is promoted. Final inventory checks passed; only one of six Earth-radius
injections passed, so sensitivity limitations remain substantial.

**Sector 35 extension:** [312 of 313 selected stars have usable searches](results/qlp-faint-sector35-expanded-20261010/ASSESSMENT.md).
[TIC 80269913](results/qlp-faint-sector35-followup-20261010/80269913-peak0/ASSESSMENT.md)
recurs at 3.55976 days in both reserved epochs, but processed pixels and neighbor
photometry favor contamination near TIC 80269891. TIC 141301608 remains unresolved
with image-artifact concerns. No planet candidate is promoted; one target remains
incomplete. Final inventory checks passed.

**Sector 40 extension:** [342 distinct stars have usable searches, including one adjacent-sector recovery](results/qlp-faint-sector40-expanded-20261010/ASSESSMENT.md).
[TIC 321923791](results/qlp-faint-sector40-followup-20261010/321923791-peak0/ASSESSMENT.md)
remains an unresolved blend at 3.71896 days; processed pixels favor a faint close
neighbor. TIC 317811978 favors neighboring-source contamination at 0.93508 days.
Neither is promoted to a planet candidate. Final inventory checks passed;
controls missed every Earth-radius injection.

**Sector 91 extension:** [all 366 selected stars have usable searches](results/qlp-faint-sector91-expanded-20261010/ASSESSMENT.md).
Ten diagnostic period solutions on five stars share a late dip within 43 minutes,
despite star separations of 2.5–13.5 degrees. [The timing comparison](results/qlp-faint-sector91-common-events-20261010/ASSESSMENT.md)
favors shared instrumental contamination, including the earlier unresolved
TIC 386739254 signal. None is promoted to a planet candidate. Final inventory
checks passed; sensitivity and source-attribution limitations remain explicit.

**Sector 87 extension:** [all 375 selected stars have usable searches](results/qlp-faint-sector87-expanded-20261010/ASSESSMENT.md).
Four signals were reviewed. TIC 234632130 favors off-target contamination;
TIC 151516585, TIC 299622445 and pilot TIC 25124525 remain unresolved with
variability, background or source-attribution concerns. None is promoted to a
credible planet candidate. Final inventory checks passed; limitations are retained.

**Sector 55 extension:** [all 395 selected stars have usable searches](results/qlp-faint-sector55-expanded-20261010/ASSESSMENT.md).
Its sole eligible signal, [TIC 304608681](results/qlp-faint-sector55-followup-20261010/304608681-peak0/ASSESSMENT.md),
favors contamination near a neighboring star about four pixels away. Its measured
depth also changes sign between reductions. No planet candidate is promoted.
Final inventory checks passed; sensitivity limitations remain explicit.

**Sector 58 extension:** [447 of 448 selected stars have completed usable searches](results/qlp-faint-sector58-expanded-20261010/ASSESSMENT.md).
Its sole eligible lead, [TIC 389908768](results/qlp-faint-sector58-followup-20261010/389908768-peak0/ASSESSMENT.md),
has a 0.83033-day signal whose difference image favors neighboring-star contamination
about two pixels from the target. The exact source remains unresolved; no planet
candidate is promoted. One other target has incomplete screening, retained explicitly.
Final inventory checks passed; substantial sensitivity limitations remain.

**Sector 27 extension:** [all 456 selected stars have usable searches](results/qlp-faint-sector27-expanded-20261010/ASSESSMENT.md).
The expansion finished with 293 below threshold, 63 flagged and no errors or
eligible leads. Final inventory checks passed. Controls show uneven sensitivity,
including all eight injections missed on one of three test stars.

**Sector 69 extension:** [511 of 512 selected stars have usable searches](results/qlp-faint-sector69-expanded-20261010/ASSESSMENT.md).
The expansion finished with 390 below threshold, 22 flagged and no errors or
eligible leads. One pilot target remains unusable after recovery. Final inventory
checks passed; controls retain uneven sensitivity and six out-of-grid injections.

**Sector 50 extension:** [639 of 643 selected stars have usable searches](results/qlp-faint-sector50-expanded-20261010/ASSESSMENT.md).
The expansion finished with 497 below threshold, 38 flagged and eight original
errors. Four separate adjacent-sector searches succeeded below threshold; four
stars remain unusable. Neither follow-up policy produced an eligible lead, and
final inventory checks passed. Controls retain substantial sensitivity limits,
including six longer-period injections outside the actual search window.

**Sector 75 extension:** [all 660 selected stars have usable searches](results/qlp-faint-sector75-expanded-20261010/ASSESSMENT.md).
The expansion finished with 472 below threshold, 88 flagged and no errors or
eligible leads. Final inventory and integrity checks passed; sensitivity limits
and rejected signals are retained.

**Sector 86 extension:** [all 778 selected stars have usable searches](results/qlp-faint-sector86-expanded-20261010/ASSESSMENT.md).
The expansion finished with 612 below threshold, 66 flagged and no errors.
Eight follow-up peaks on six stars were reviewed: four stars favor contamination;
TIC 393024259 and TIC 408885974 remain unresolved. None is promoted to a new
planet candidate. Zero longer-period controls passed all non-crowding gates,
so sensitivity limitations remain substantial.

**Sector 7 extension:** [all 801 selected stars have usable searches](results/qlp-faint-sector7-expanded-20261010/ASSESSMENT.md).
The expansion finished with 626 below threshold, 75 flagged and no errors or
eligible leads. Limited controls and their misses are retained; this does not
establish completeness or exclude planets below the search sensitivity.

**Sector 28 extension:** [all 881 selected stars have usable searches](results/qlp-faint-sector28-expanded-20261010/ASSESSMENT.md),
including one separate Sector 29 recovery whose original failure is retained.
The expansion finished with 697 below threshold, 83 flagged and one original
error. Both reviewed leads favor contamination: TIC 183494855 near a neighboring
blend, and TIC 147201125 from a known eclipsing binary with a matching period.
Neither is promoted to a new planet candidate.

**Sector 17 extension:** [all 923 selected stars were attempted](results/qlp-faint-sector17-expanded-20261010/ASSESSMENT.md).
The expansion finished with 734 below threshold, 84 flagged and five unusable
products. Including three pilot failures, 915 stars have usable searches.
Same-epoch recovery attempts failed for all eight unusable products. Both reviewed
signals, TIC 322396623 and TIC 419253850, favor neighboring-star contamination;
exact components and physical periods remain unresolved. Neither is promoted.

**Sector 60 extension:** [all 1,172 selected stars have usable searches](results/qlp-faint-sector60-expanded-20261010/ASSESSMENT.md).
The expansion finished with 1,002 below threshold, 70 flagged and no errors.
Its sole reviewed lead, TIC 453330136, favors off-target contamination.

**Sector 76 extension:** [all 1,301 selected stars were attempted](results/qlp-faint-sector76-expanded-20261010/ASSESSMENT.md).
The 1,201-target expansion finished with 997 below threshold, 202 flagged and
two original errors. One separate recovery succeeded, bringing the usable total
including the pilot to 1,300. Eleven peaks on ten stars were reviewed: five stars now
favor off-target contamination after an adjacent-epoch check; the others remain unresolved or noise-dominated.
None is promoted to a new planet candidate.

**Sector 52 extension:** [all 1,507 selected stars were attempted](results/qlp-faint-sector52-expanded-20261010/ASSESSMENT.md).
The expansion finished with 1,198 below threshold, 202 flagged and seven original
errors. Two separate recovery searches succeeded, bringing the usable total
including the pilot to 1,502. Three signals were reviewed: two favor neighboring
binary contamination; TIC 115351953 remains a weak, processing-dependent diagnostic.

**Sector 72 extension:** all 1,805 selected stars have usable searches,
including two separate recovery attempts whose original failures are retained.
The [1,705-target expansion](results/qlp-faint-sector72-expanded-20261010/ASSESSMENT.md)
finished with 1,517 below threshold, 186 flagged and two original errors.
Seven pilot/expansion follow-up peaks were reviewed without planet promotion.
The recovered single event in TIC 26587095 favors neighbor contamination.

**Sector 70 extension:** the [1,831-target expansion](results/qlp-faint-sector70-expanded-20261010/ASSESSMENT.md)
is complete: 1,646 below threshold, 183 flagged and two unusable targets whose
recovery attempts also failed. Including the pilot, 1,929 of 1,931 selected
stars were successfully searched. Both reviewed leads favor binary signals.

**Sector 97 extension:** all 1,100 selected stars have been searched. The
100-star pilot had 69 below threshold and 31 flagged; the
[1,000-star expansion](results/qlp-faint-sector97-expanded-20261010/ASSESSMENT.md)
had 794 below threshold, 206 flagged and no errors. Seven follow-up peaks on
six stars were reviewed; none is promoted. TIC 32495864 remains unresolved.
A [remaining-coverage audit](results/qlp-faint-remaining-after91-20261010/ASSESSMENT.md)
identified 2,909 unused stars after excluding the full Sector 91 selection, with reserved epochs across
the archived sectors; these counts do not imply novelty or survey completeness.

**Sector 103 extension:** 209 unused targets were selected. The 100-star pilot
finished with 70 below threshold, 29 flagged and one unusable light curve,
searched separately in Sector 96 with no qualifying signal. Its one follow-up
lead is off-target near TIC 144325911. The 109-star expansion is complete: 83 below threshold, 26 flagged, no errors.
One diagnostic harmonic remains unpromoted.

**Sector 102 extension:** the [100-star pilot](results/qlp-faint-sector102-pilot-20261010/ASSESSMENT.md)
finished with 84 below threshold, 16 flagged, and no eligible leads. The
[308-star expansion](results/qlp-faint-sector102-expanded-20261010/ASSESSMENT.md) is complete:
292 below threshold, 16 flagged, no errors or eligible leads. Limited controls recovered nine
of 12 injected periods, with seven passing non-crowding gates.

**Sector 101 extension:** 606 unused targets were selected after excluding all
7,863 prior selections. The [100-star pilot](results/qlp-faint-sector101-pilot-20261010/ASSESSMENT.md)
finished with 79 below threshold, 21 flagged, and no eligible follow-up lead.
The [506-star expansion](results/qlp-faint-sector101-expanded-20261010/ASSESSMENT.md)
is also complete: 431 below threshold, 75 flagged, no errors or eligible leads.

**Sector 99 extension:** 829 previously unsearched targets were selected after
excluding all prior samples and cached target photometry. The [100-star pilot](results/qlp-faint-sector99-pilot-20261010/ASSESSMENT.md) finished:
90 below threshold, 10 flagged, one lead resolved to known eclipsing-binary contamination.
The 729-star expansion is complete; its one follow-up lead is off-target
contamination with an unresolved close-pair source.

**Sector 100 extension:** the [100-star pilot](results/qlp-faint-sector100-pilot-20261010/ASSESSMENT.md)
finished with 85 below threshold, 15 flagged, and no eligible follow-up signal.
The [1,499-star expansion](results/qlp-faint-sector100-expanded-20261010/ASSESSMENT.md)
is complete: 1,408 below threshold, 91 flagged, and no data errors. Two of
its three follow-up signals resolve to known eclipsing-binary contamination;
the third has an unresolved off-target source. All 12 synthetic
signals recovered their periods and checked phases; nine passed non-crowding
gates. These limited controls do not establish completeness.

**Sector 104 extension:** the [100-star pilot](results/qlp-faint-sector104-pilot-20261010/ASSESSMENT.md)
finished with 72 below threshold, 28 flagged, and no eligible follow-up signal.
The [1,855-star expansion](results/qlp-faint-sector104-expanded-20261010/ASSESSMENT.md)
is also complete: 1,682 below threshold, 172 flagged, and one failed target
searched separately in Sector 103 with no qualifying signal. Both follow-up
leads remain unpromoted. Synthetic controls show
useful but incomplete short-period recovery; usable baselines restrict the
period range, and out-of-range controls are explicitly retained.

**Sector 98 extension:** a new [100-star pilot](results/qlp-faint-sector98-pilot-20261010/ASSESSMENT.md)
finished with 73 below threshold, 27 flagged, and no qualifying follow-up.
The remaining [1,435-star search](results/qlp-faint-sector98-expanded-20261010/ASSESSMENT.md)
is also complete: 1,288 below threshold, 147 flagged, and no data errors.
Its sole follow-up lead resolves to contamination from known planet host TIC 46432937.
No new likely planet candidate emerged from these 1,535 stars.
[Injection checks](results/qlp-faint-sector98-injections-20261010/ASSESSMENT.md)
recovered 12/12 injected periods and checked phases, with 8/12 passing signal-quality gates.
These limited controls do not establish completeness or novelty.
[Longer-period controls](results/qlp-faint-sector98-long-injections-20261010/ASSESSMENT.md)
recovered all 12 injected periods and checked phases but **none passed the full gates**;
coverage and detrending checks limit sensitivity. The separate diagnostic review
for strong signals with coverage-related flags finished with no eligible peaks.

| Target | Signal | Current status | Evidence |
|---|---|---|---|
| **TIC 280625681** | **2.872-day** signal | **Likely known-binary contamination:** pixels near TIC 280625668 with a closely matching Gaia period. | [Assessment](results/qlp-faint-sector86-followup-20261010/280625681-peak0/ASSESSMENT.md) |
| **TIC 408885974** | **2.966 / 4.948-day** diagnostics | **Unresolved:** background-dominated pixel maps, blended target region and ambiguous period; no SPOC comparison. | [Assessment](results/qlp-faint-sector86-followup-20261010/408885974-peak0/ASSESSMENT.md) |
| **TIC 428260264** | **1.143-day** signal | **Likely close-binary contamination:** TIC 643593883 is less than one pixel away with a closely matching Gaia period; target-centered apertures cannot separate it. | [Assessment](results/qlp-faint-sector86-followup-20261010/428260264-peak0/ASSESSMENT.md) |
| **TIC 2433753** | **1.672 / 4.458-day** diagnostics | **Likely off-target contamination:** pixel residuals near TIC 2433754 / 2433756; exact component and physical period unresolved. | [Short-period assessment](results/qlp-faint-sector86-followup-20261010/2433753-peak0/ASSESSMENT.md), [two-event assessment](results/qlp-faint-sector86-coverage-followup-20261010/2433753-peak2/ASSESSMENT.md) |
| **TIC 393024259** | **1.576-day** signal | **Unresolved:** weak off-target pixel patch near TIC 393024226 on structured background; timing checks inconclusive and SPOC unavailable. | [Assessment](results/qlp-faint-sector86-pilot-followup-20261010/393024259-peak0/ASSESSMENT.md) |
| **TIC 428538275** | **2.850-day** diagnostic | **Known neighboring binary contamination:** TIC 428538335 has a 0.95008-day Gaia period; this peak is a three-period alias. | [Assessment](results/qlp-faint-sector86-pilot-followup-20261010/428538275-peak2/ASSESSMENT.md) |
| **TIC 147201125** | **1.880-day** signal | **Known neighboring binary contamination:** pixel source near TIC 147201138; deep neighbor eclipses and closely matching Gaia period. | [Assessment](results/qlp-faint-sector28-followup-20261010/147201125-peak0/ASSESSMENT.md) |
| **TIC 183494855** | **3.066-day** signal | **Likely off-target contamination:** compact pixel signal near TIC 183494856, with a fainter blend unresolved; much weaker in SPOC. | [Assessment](results/qlp-faint-sector28-pilot-followup-20261010/183494855-peak0/ASSESSMENT.md) |
| **TIC 419253850** | **5.284-day** diagnostic | **Likely off-target contamination:** adjacent-sector pixels place the source near TIC 419246494 / 419246493, about five pixels away; two original events and inconsistent neighbor epochs leave the physical period unresolved. | [Assessment](results/qlp-faint-sector17-coverage-followup-20261010/419253850-peak0/ASSESSMENT.md) |
| **TIC 322396623** | **3.251-day** signal | **Likely contamination near a known binary:** off-target near TIC 322396629; its Gaia period is 2.779 days, so exact source identification remains unresolved. | [Assessment](results/qlp-faint-sector17-pilot-followup-20261010/322396623-peak0/ASSESSMENT.md) |
| **TIC 453330136** | **1.628-day** signal | **Likely off-target contamination:** pixel residual near TIC 453330129 / 453330128; exact component and class unresolved. | [Assessment](results/qlp-faint-sector60-followup-20261010/453330136-peak0/ASSESSMENT.md) |
| **TIC 276393079** | **2.886-day** signal | Unresolved: raw pixel map is entirely negative; recurrence and source unestablished. | [Assessment](results/qlp-faint-sector76-followup-20261010/276393079-peak0/ASSESSMENT.md) |
| **TIC 469995081** | **6.228-day** signal | **Likely contamination:** adjacent-sector pixels favor a close neighboring group containing a Gaia binary with approximately triple the TESS period. | [Updated assessment](results/tesscut-469995081-s77-20261010/ASSESSMENT.md), [original checks](results/qlp-faint-sector76-followup-20261010/469995081-peak0/ASSESSMENT.md) |
| **TIC 84021791** | **1.063-day** signal | Unresolved: nearly uniform positive pixel background cannot localize the source. | [Assessment](results/qlp-faint-sector76-followup-20261010/84021791-peak0/ASSESSMENT.md) |
| **TIC 375498412** | **0.640-day** signal | **Likely known-binary contamination:** off-target near TIC 375498359, with a closely matching Gaia binary period. | [Assessment](results/qlp-faint-sector76-followup-20261010/375498412-peak0/ASSESSMENT.md) |
| **TIC 326710738** | **9.09 / 8.81-day** aliases | Noise-dominated two-event fits; no clean repeated transit or independent-reduction confirmation. | [Peak 0](results/qlp-faint-sector76-coverage-followup-20261010/326710738-peak0/ASSESSMENT.md), [peak 2](results/qlp-faint-sector76-coverage-followup-20261010/326710738-peak2/ASSESSMENT.md) |
| **TIC 166864803** | **0.888-day** signal | **Likely known-binary contamination:** off-target near TIC 166864758; Gaia period differs by 0.168%, and neighbor eclipses are deeper. | [Assessment](results/qlp-faint-sector76-followup-20261010/166864803-peak0/ASSESSMENT.md) |
| **TIC 354034635** | **4.464-day** harmonic | **Likely off-target contamination:** near TIC 354034637 / 950486341; exact component and period unresolved. | [Assessment](results/qlp-faint-sector76-followup-20261010/354034635-peak2/ASSESSMENT.md) |
| **TIC 376079066** | **2.827-day** signal | **Likely neighboring eclipse contamination:** pixels favor TIC 376079048, whose QLP dips reach 6.5%. | [Assessment](results/qlp-faint-sector76-followup-20261010/376079066-peak0/ASSESSMENT.md) |
| **TIC 260172556** | **6.084-day** diagnostic | Unresolved: competing harmonic periods; adjacent-sector pixels suggest a neighbor, but background and blends prevent secure attribution. | [Original checks](results/qlp-faint-sector76-followup-20261010/260172556-peak1/ASSESSMENT.md), [adjacent-epoch check](results/tesscut-260172556-s77-20261010/ASSESSMENT.md) |
| **TIC 154205325** | **6.350-day** two-event diagnostic | Strong QLP excursions, but unstable detrending, gaps and no positive pixel localization. Not promoted. | [Assessment](results/qlp-faint-sector76-coverage-followup-20261010/154205325-peak0/ASSESSMENT.md) |
| **TIC 115351953** | **8.258-day** two-event signal | **Weak diagnostic:** noisy QLP signal substantially weaker in SPOC; recurrence and host unestablished. | [Assessment](results/qlp-faint-sector52-coverage-followup-20261010/115351953-peak0/ASSESSMENT.md) |
| **TIC 429001850** | **1.055-day** signal | **Likely known-binary contamination:** two pixel epochs favor TIC 429001844, whose Gaia binary period closely matches. | [Assessment](results/qlp-faint-sector52-followup-20261010/429001850-peak0/ASSESSMENT.md) |
| **TIC 461579141** | **2.253-day** signal | **Likely contamination near a known binary:** pixels favor TIC 461579142, but its Gaia period is 2.552 days; the discrepancy remains unresolved. | [Assessment](results/qlp-faint-sector52-followup-20261010/461579141-peak0/ASSESSMENT.md) |
| **TIC 153685705** | **0.953-day** signal | **Unresolved:** background-dominated, all-negative pixel difference cannot identify a source; held-out timing is inconclusive. Not promoted. | [Assessment](results/qlp-faint-sector72-followup-20261010/153685705-peak0/ASSESSMENT.md) |
| **TIC 26587095** | Single dip in **Sector 71** | **Likely neighbor contamination:** a single-event pixel image favors TIC 26587084, whose extraction has a 20% dip. Period and exact component remain unconfirmed. | [Assessment](results/qlp-faint-sector72-recovery-20261010/26587095/ASSESSMENT.md) |
| **TIC 386489835** | **2.550-day** signal | **Likely neighbor binary contamination:** pixels favor TIC 337384325, whose extraction shows 9.35% eclipses. | [Assessment](results/qlp-faint-sector72-followup-20261010/386489835-peak0/ASSESSMENT.md) |
| **TIC 387149074** | **2.623-day** signal | **Likely off-target contamination:** pixels favor TIC 387149063; physical classification remains unresolved. | [Assessment](results/qlp-faint-sector72-followup-20261010/387149074-peak0/ASSESSMENT.md) |
| **TIC 17597778** | Competing **8.260/8.077-day** fits | **Not reproduced in TESS-SPOC:** QLP has extreme changing scatter; neither fit is promoted. | [Assessment](results/qlp-faint-sector72-followup-20261010/17597778-peak0/ASSESSMENT.md) |
| **TIC 16488471** | **2.137-day** signal | **Likely contamination:** two pixel epochs favor nearby TIC 16488473, a Gaia binary. Its catalog period differs; exact source remains uncertain. | [Assessment](results/qlp-faint-sector72-followup-20261010/16488471-peak0/ASSESSMENT.md) |
| **TIC 70665830** | **3.466-day** signal | **Likely neighbor binary contamination:** pixels favor TIC 70665829 or a close neighbor; its extraction shows 14–27% eclipses at the same timing in three sectors. | [Assessment](results/qlp-faint-sector72-pilot-followup-20261010/70665830-peak0/ASSESSMENT.md) |
| **TIC 337010700** | **1.408-day** signal | **Likely neighbor eclipsing-binary contamination:** pixels favor TIC 337010705, whose extraction shows a 29% eclipse at the same timing. | [Assessment](results/qlp-faint-sector70-followup-20261010/337010700-peak0/ASSESSMENT.md) |
| **TIC 347416701** | **3.514-day** signal | **Likely eclipsing binary:** roughly 5% primary and 2.5% secondary dips; pixels near target and a close faint neighbor. Exact host unresolved. | [Assessment](results/qlp-faint-sector70-followup-20261010/347416701-peak0/ASSESSMENT.md) |
| **TIC 439405270** | **14.732-day** two-event diagnostic | **Unresolved:** detrending-sensitive, broad structure and inconclusive held-out timing. Not promoted. | [Assessment](results/qlp-faint-sector97-coverage-followup-20261010/439405270-peak0/ASSESSMENT.md) |
| **TIC 32495864** | **13.816-day** signal; competing **14.360-day** fit | **Unresolved:** four-event QLP fit passes initial filters, but a separate pixel extraction falls to SNR 1.95–2.96. Broad shape, competing periods and uncertain held-out timing prevent promotion. | [Assessment](results/qlp-faint-sector97-followup-20261010/32495864-peak1/ASSESSMENT.md) |
| **TIC 209405949** | **13.741-day** diagnostic | **Unresolved:** broad, detrending-sensitive signal with inconclusive held-out timing. Not promoted. | [Assessment](results/qlp-faint-sector97-followup-20261010/209405949-peak0/ASSESSMENT.md) |
| **TIC 250389607** | **13.427-day** two-event diagnostic | **Weak unresolved signal:** significance is point-sensitive, alternative detrending favors another period, and held-out timing is inconclusive. Not promoted. | [Assessment](results/qlp-faint-sector97-coverage-followup-20261010/250389607-peak0/ASSESSMENT.md) |
| **TIC 269573079** | **10.775-day** two-event diagnostic | **Not robust:** removing one point lowers fixed-timing SNR from 7.48 to 2.15. Not promoted. | [Assessment](results/qlp-faint-sector97-coverage-followup-20261010/269573079-peak0/ASSESSMENT.md) |
| **TIC 268687730** | **14.284-day** two-event diagnostic | **Weak unresolved signal:** survives individual-point removal, but period depends on detrending and held-out timing is inconclusive. Not promoted. | [Assessment](results/qlp-faint-sector97-coverage-followup-20261010/268687730-peak0/ASSESSMENT.md) |
| **TIC 176456470** | **2.735-day** diagnostic harmonic | **Likely off-target binary contamination.** Pixels favor TIC 176456469; its extraction shows alternating 8–9% eclipses. Exact source and binary classification remain unconfirmed. | [Assessment](results/qlp-faint-sector103-followup-20261010/176456470-peak2/ASSESSMENT.md) |
| **TIC 144325909** | **3.849-day** QLP dimming | **Not promoted; contamination concern.** Pixel signal is 1.93 pixels off target near TIC 144325911; exact variable source remains unresolved. | [Assessment](results/qlp-faint-sector103-pilot-followup-20261010/144325909-peak0/ASSESSMENT.md) |
| **TIC 464190279** | **1.257-day** QLP dimming | **Off-target contamination; not promoted.** Two pixel epochs favor the close pair TIC 861857428/464190342; their Sector 99 extractions are identical, and the exact source remains unresolved. | [Assessment](results/qlp-faint-sector99-followup-20261010/464190279-peak0/ASSESSMENT.md) |
| **TIC 220440079** | **2.979-day** QLP dimming | **Known eclipsing-binary contamination.** Off-target pixels locate the signal near TIC 220439648, whose Gaia binary period matches. | [Assessment](results/qlp-faint-sector99-pilot-followup-20261010/220440079-peak0/ASSESSMENT.md) |
| **TIC 459258444** | **2.918-day** QLP dimming | **Known eclipsing-binary contamination.** Off-target pixels, matching Gaia period, and an 11.6% neighbor dip identify TIC 459258383. | [Assessment](results/qlp-faint-sector100-followup-20261010/459258444-peak0/ASSESSMENT.md) |
| **TIC 383941028** | **1.516-day** QLP dimming | **Not promoted; contamination concern.** Two sectors show pixel signals 1.77/1.41 pixels off target, near TIC 383941039; exact variable source remains unresolved. | [Assessment](results/qlp-faint-sector100-followup-20261010/383941028-peak0/ASSESSMENT.md) |
| **TIC 164293311** | **0.991-day** QLP dimming | **Known eclipsing-binary contamination.** Two pixel epochs locate the signal near TIC 164299149, which Gaia catalogs as an eclipsing binary with a matching period. | [Assessment](results/qlp-faint-sector100-followup-20261010/164293311-peak0/ASSESSMENT.md) |
| **TIC 306101698** | **2.870-day** QLP screening lead | **Not promoted; persistent contamination concern.** Both event groups retain an off-target pixel signal; neighboring sources lack separate light curves, and reserved timing is inconclusive. | [Assessment](results/qlp-faint-sector104-followup-20261010/306101698-peak0/ASSESSMENT.md) |
| **TIC 201228641** | **8.660-day** QLP diagnostic peak | **Not promoted.** Only two supported discovery events; reserved timing is inconclusive, flux is structured, and SPOC is unavailable. | [Assessment](results/qlp-faint-sector104-coverage-followup-20261010/201228641-peak0/ASSESSMENT.md) |
| **TIC 46432934** | **1.4404-day** deep QLP dip | **Known-neighbor contamination.** Pixel difference centers on TIC 46432937, whose confirmed planet has the matching period. Not a new candidate. | [Assessment](results/qlp-faint-sector98-followup-20261010/46432934-peak0/ASSESSMENT.md) |
| **TIC 342076351** | **0.603-day** QLP screening lead | **Not promoted.** Reserved timing inconclusive; matched-exposure SPOC raw and corrected flux do not reproduce the QLP dip. | [Assessment](results/qlp-faint-expanded-followup-20261010/342076351-peak0/ASSESSMENT.md) |
| **TIC 233194992** | **13.287-day** QLP diagnostic peak | **Not promoted.** Detrending inconsistency, structured noise, inconclusive reserved tests, and unavailable SPOC files; comparison with TIC 198186473 does not establish shared dips. | [Assessment](results/qlp-faint-expanded-followup-20261010/233194992-peak0/ASSESSMENT.md) |
| **TIC 31869709** | **1.130-day** diagnostic peak; possible **0.3767-day** repetition | **Likely off-target contamination.** Two difference images lie 2.12/2.76 pixels off target near TIC 31869705/31869706; neither has an exact-name QLP/SPOC light curve, so the precise source remains unresolved. | [Assessment](results/qlp-faint-expanded-followup-20261010/31869709-peak2/ASSESSMENT.md) |
| **TIC 198186473** | **13.281-day** QLP dimming | **Screening lead; not promoted.** Structured noise and inconclusive reserved timing; matched-exposure SPOC raw and corrected flux do not reproduce the strong QLP dip. | [Assessment](results/qlp-faint-expanded-followup-20261010/198186473-peak0/ASSESSMENT.md) |
| **TIC 207468582** | **4.613-day** QLP dimming; ten supported discovery events | **Suspected contamination.** Pixel offsets favor neighbor TIC 207468583; its dip repeats in Sector 83. Ground-based ZTF coverage is insufficient; host attribution and binary/planet classification remain unresolved. | [Assessment](results/qlp-faint-expanded-followup-20261010/207468582-peak0/ASSESSMENT.md) |
| **TIC 219846123** | **14.435-day** QLP dimming | **Diagnostic lead; not promoted.** Detrending inconsistency; weak native and SPOC support, with inconclusive reserved timing. | [Assessment](results/qlp-faint-expanded-followup-20261010/219846123-peak2/ASSESSMENT.md) |
| **TIC 353895145** | **12.858-day** QLP dimming | **Diagnostic lead; not promoted.** Detrending inconsistency and severe structured noise; reserved tests and SPOC evidence are inadequate. | [Assessment](results/qlp-faint-expanded-followup-20261010/353895145-peak2/ASSESSMENT.md) |
| **TIC 356346889** | **14.998-day** QLP dimming | **Diagnostic lead; not promoted.** Fails detrending consistency; reserved timing inconclusive and usable SPOC sector does not recover the dip. | [Assessment](results/qlp-faint-expanded-followup-20261010/356346889-peak0/ASSESSMENT.md) |
| **TIC 160438697** | **14.226-day** QLP dimming | **Screening lead; not promoted.** Structured discovery noise; reserved timing tests inconclusive, without qualifying recurrence. | [Assessment](results/qlp-faint-expanded-followup-20261010/160438697-peak0/ASSESSMENT.md) |
| **TIC 233096878** | **14.044-day** QLP dimming | **Screening lead; not promoted.** Structured discovery noise; reserved timing tests inconclusive, without qualifying recurrence. | [Assessment](results/qlp-faint-expanded-followup-20261010/233096878-peak1/ASSESSMENT.md) |
| **TIC 353936060** | **12.781-day** QLP dimming | **Diagnostic lead; not promoted.** Positive Sector 14 and modest Sector 75 measurements, with weak same-image SPOC support; detrending inconsistency, broad timing uncertainty, and comparable phase controls prevent promotion. | [Assessment](results/qlp-faint-expanded-followup-20261010/353936060-peak0/ASSESSMENT.md) |
| **TIC 320504102** | **~13.39-day** QLP dimming | **Screening lead; not promoted.** Modest positive Sector 75 evidence; timing gates fail and SPOC event coverage is inadequate. | [Assessment](results/qlp-faint-expanded-followup-20261010/320504102-peak0/ASSESSMENT.md) |
| **TIC 278410520** | **2.982-day** QLP dimming; 30 supported discovery events | **Likely off-target contamination.** Two pixel epochs locate the dip near TIC 278410515, about two pixels from the target; direct neighbor light curve unavailable; exact source remains unverified. | [Assessment](results/qlp-faint-expanded-followup-20261010/278410520-peak0/ASSESSMENT.md) |
| **TIC 356109440** | **13.676-day** QLP dimming | **Diagnostic lead; not promoted.** Fails detrending consistency; reserved tests lack usable event measurements and precise timing. | [Assessment](results/qlp-faint-expanded-followup-20261010/356109440-peak0/ASSESSMENT.md) |
| **TIC 167307093** | **~14.02-day** QLP dimming | **Diagnostic lead; not promoted.** Fails detrending consistency; reserved-sector timing is inconclusive. | [Assessment](results/qlp-faint-expanded-followup-20261010/167307093-peak0/ASSESSMENT.md) |
| **TIC 287530678** | **13.476-day** QLP dimming | **Screening lead; not promoted.** Reserved-sector timing is inconclusive; matched-exposure SPOC raw and corrected flux do not reproduce the dip. | [Assessment](results/qlp-faint-expanded-followup-20261010/287530678-peak0/ASSESSMENT.md) |
| **TIC 314649431** | **1.14381-day** dimming | **Rejected as a planet around the target.** Off-target TESScut signal and ~0.4mag ZTF eclipses identify neighbor TIC314649408. | [Full evidence](results/qlp-314649431-posthoc-20261010/ASSESSMENT.md) |
| **TIC 25324731** | **1.69626-day** dimming; passes new sector89 | **Rejected as a planet around the target.** Two pixel epochs and 28–31% eclipses identify neighbor TIC25318752. | [Full evidence](results/qlp-25324731-expanded-20261010/ASSESSMENT.md) |
| **TIC 240023401** | **2.07538-day** dimming; passes new sectors71/72 | **Rejected as a planet around the target.** Off-target TESS pixels and ~0.19–0.23mag ZTF eclipses identify neighbor TIC240023393. | [Full evidence](results/qlp-240023401-expanded-20261010/ASSESSMENT.md) |
| **TIC 378761120** | **1.32724-day** dimming, ~1,000 ppm; passes new Sector78/85 predictions | **Rejected as a planet around the target.** Two pixel epochs locate it off-target; **neighbor TIC378761130 shows ~0.24mag ZTF eclipses at the frozen phase**. | [Full evidence](results/qlp-378761120-expanded-20261010/ASSESSMENT.md) |
| **TIC 80387959** | **4.19217-day** transit-like dimming; roughly 620–1,000 ppm across reductions/sectors | **Unresolved candidate signal.** Recovers in previously unopened Sectors 90/100, but PRF fits disagree about the host. Nearby eclipsing stars remain viable. Conditional radius ~2.5–2.6 Earth radii only if the catalog target hosts it. | [Held-out tests](results/followup-80387959-qlp90-100-20261009/heldout.json), [PRF assessment](results/prf-80387959-20261009/ASSESSMENT.md) |
| **TIC 286607959** | **10.45924-day** dimming | **Rejected as a planet around the target.** Two pixel epochs and ~21% eclipses in neighbor TIC286608026 explain the signal. | [Contamination evidence](results/qlp-286607959-expanded-20261010/ASSESSMENT.md) |
| **HD 297396 / TOI-6263** | **4.2689-day** RV signal, distinct from the already-listed **3.0179-day TOI candidate** | **Unresolved; not promoted.** Mask-aware RV prediction is weak/model-dependent. A fitted 4.27-day transit did not recur in TESS Sectors35/36. The host is already a known candidate system. | [Identity](results/hd297396-identity-20261010/ASSESSMENT.md), [RV sensitivity](results/hd297396-mask-followup-20261010/ASSESSMENT.md), [TESS check](results/hd297396-tess-20261010/ASSESSMENT.md) |

**External lead independently reanalyzed:** **HD 32564** — HARPS signals near
**2.5566, 11.061, and 23.597 days**, plus a weaker ~49.1-day component.
Our archival fit reproduces the main signal family. The three shorter components
still improve omitted-year predictions after [linear activity adjustments](results/rv-hd32564-activity-20261010/ASSESSMENT.md).
**The ~49-day component is model-sensitive:** wider period fitting worsens the
2012 DRS prediction in three tested model variants. [Selected alias checks](results/rv-hd32564-alias-20261010/ASSESSMENT.md)
also leave it ambiguous; the three shorter periods predict better overall than
the tested alternatives. An [initial TESS transit screen](results/hd32564-tess-screen-20261010/ASSESSMENT.md)
found no qualifying signal; its short baseline did not test the longer RV periods.
An [additional Sector 32 screen](results/hd32564-tess-sector32-20261010/ASSESSMENT.md)
also found no qualifying signal in QLP or SPOC. A subsequent
[Sector 98 discovery search](results/hd32564-tess-sector98-20261010/ASSESSMENT.md)
was below threshold in QLP; SPOC returned HTTP 404. A
[targeted 23.597-day check](results/hd32564-tess-rv23-20261010/ASSESSMENT.md)
found only a weak single-event fit. No transit exclusion is claimed.
Correlated activity noise and broader alias checks remain incomplete. **Not our discovery or a confirmation.**
[Replication evidence](results/rv-hd32564-20261010/ASSESSMENT.md) ·
[Original report](https://x.com/mehran__jalali/status/2108708424079024520).

**Fainter-star expansion:** the [100-star pilot](results/qlp-faint-pilot-20261010/ASSESSMENT.md)
is complete: 46 below threshold, 54 flagged, no qualifying verification targets.
The remaining **1,845 stars** have finished their frozen four-sector search:
950 below threshold, 888 flagged, and seven original data failures.
[Final reconciliation](results/qlp-faint-expanded-20261010/ASSESSMENT.md) accounts
for all 1,845 targets, 1,844 usable searches after recovery, and 17 completed
peak follow-ups. The newest lead’s matched-exposure check weakens its QLP signal.
Eight stars passed the non-crowding screen. TIC 278410520 and diagnostic lead TIC 31869709 now have strong
off-target evidence. Nine additional peaks received diagnostic-only follow-up, including a
three-times-period peak on TIC 207468582; peaks are not separate planets.
No likely new planet is established. Separate
three-sector recoveries of six failed targets yielded no qualifying signal,
including [TIC 139359550](results/qlp-faint-expanded-recovery-20261010/139359550/ASSESSMENT.md)
and [TIC 172933634](results/qlp-faint-expanded-recovery-20261010/172933634/ASSESSMENT.md).
[One failed target](results/qlp-faint-expanded-recovery-20261010/423088347/ASSESSMENT.md)
has only two usable training sectors and remains unsearchable under this plan.
All come from a metadata audit of 38,822 eligible stars; this is not a complete
TESS search or evidence of novelty.
[Known-planet controls](results/qlp-faint-positive-controls-20261010/ASSESSMENT.md)
show limited sensitivity; [12 synthetic injections](results/qlp-faint-injections-20261010/ASSESSMENT.md)
recover their periods/phases, with 10 passing signal-quality checks. These are
controls, not discoveries or a completeness estimate.

**Latest completed searches:** [1,322 late-sector stars](results/audit-late-sectors-20261010/ASSESSMENT.md)
and [287 usable QLP-selected stars](results/audit-qlp-expanded-20261010/ASSESSMENT.md),
with one additional QLP target unsearchable. Seven late-sector screening passes
were investigated: one has strong binary evidence; six remain unsupported after
follow-up. **No additional likely planet candidate was established.**
**Additional search complete:** all **5,619** selected QLP targets were attempted;
**5,613** were usable after separate recovery, with six remaining data failures.
[Final audit](results/audit-qlp-full-pool-20261010/ASSESSMENT.md): 25 screening passes,
five resolved contaminants, one already-published signal, and 19 unsupported or
timing-inconclusive leads. **No likely new planet candidate established.**
[Residual searches](results/audit-qlp-residuals-20261010/ASSESSMENT.md) also completed:
**534 stars, 705 additional searches, four screening passes**, all followed up.
None established an additional likely planet; original masks and failed checks retained.

A [SkyMapper check of TIC80387959](results/skymapper-80387959-20261010/ASSESSMENT.md)
found sparse, single-event coverage and did not resolve its host. A
[NOIRLab check](results/nsc-80387959-q3c-20261010/ASSESSMENT.md) found no observations
in the predicted event windows; nearby faint alternatives remain unexcluded.

Reported leads from other researchers will be labeled separately and will not be
counted as our discoveries. Candidate entries will retain failed checks and change
status when new evidence warrants it.

Private research workspace for reproducible transit searches in public NASA TESS
photometry and radial-velocity searches in public HARPS spectroscopy. **No planet discovery or validated new candidate is claimed.** The project searches selected multi-sector full-frame light curves, records
failures, and saves diagnostic rankings for further investigation.

Current results: [all 11,851 selected stars searched](results/CAMPAIGN-11851-20261009.md)
(11,847 SPOC, four QLP-only). Those original discovery searches are complete; original
failures and recovery evidence are preserved. TIC 80387959 is the strongest
unresolved lead, passing frozen predictions in QLP Sectors90/100, with host-star
attribution still uncertain. TIC399450592 now has strong evidence for an eclipsing
neighbor. No likely new planet or novelty is established.
The [mission PRF follow-up](results/prf-80387959-20261009/ASSESSMENT.md)
also leaves the host unresolved. A new [off-phase eclipse check](results/secondary-companion-20261010/ASSESSMENT.md)
finds no convincing secondary for TIC80387959, which does not resolve its host. The initial scoped investigation is complete; further archival searches resumed
on 2026-10-10. Coverage is not exhaustive across all TESS sectors or stars.
A [refreshed binary-catalog cross-check](results/eb-catalog-refresh-20261010/ASSESSMENT.md)
found no listed binary near the new targets or TIC80387959; this does not exclude
unlisted contaminants.
See [investigation state](GOAL_PROGRESS.md), the [recovery audit](results/RECOVERY-AUDIT-20261009.md)
and the [exposure-model audit](results/EXPOSURE-MODEL-AUDIT-20261009.md).

## First result

[The 2026-10-09 pilot report](results/REPORT.md) records **96 stars searched and
zero signals surviving the final heuristic screen**. No new exoplanet candidate
is established. One preliminary pass was rejected after inspecting its periodic
variability; the original and revised results are retained for audit.

## Run

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked
uv run pytest
uv run exoplanet-search --sector 14 --limit 96 --seed 20261009 \
  --output results/my-new-run
```

Choose a new output directory for each run; existing evidence is not overwritten.
The default sample is 64 stars, with at most 1,000 per invocation and at most eight
workers. Raw FITS files, bulk URL manifests, and cached catalogs stay in ignored
`data/`. Only selected files are downloaded; the bulk shell script is parsed as
text and **never executed**. Downloads use HTTPS and bounded request timeouts.
The source URLs, retrieval times, sizes, and SHA-256 hashes are recorded.
FITS HDU checksums are verified directly over original header/data bytes,
including when `DATASUM` is absent; invalid checksums stop that target. Cached
files are checksum-verified. Delete or relocate nothing from agent histories.

The TOI and confirmed-planet catalogs are fetched from NASA's Exoplanet Archive
TAP service and copied into each run as snapshots. Retrieval failures abort the
run. Reusing `data/` reuses those snapshots: the timestamps in `run.json` state
their age. To refresh, choose a new `--data` directory. Exact TIC matches are
excluded **before** random selection. A non-match does not establish novelty;
community candidates, eclipsing binaries, aliases, nearby sources, published
searches and recent announcements require additional investigation.

## Pilot method

1. Read the official TESS-SPOC light-curve manifest for the requested sector.
2. Exclude TOI/confirmed TIC IDs, sort remaining TIC IDs, and sample without
   replacement with NumPy's seeded generator. This pilot is not restricted to
   nearby stars or small stars, and low cadence does not imply unsearched data.
3. Use PDCSAP flux, keep finite positive flux/error with `QUALITY == 0`, sort and
   deduplicate time. Split at gaps longer than 0.3 days. Median detrend with a
   1.5-day window and trim half-window edges. Clip extreme positive excursions
   only; retain dips. Use a robust point-to-point scatter floor on flux errors.
4. Run Astropy Box Least Squares on periods 0.7 days to the smaller of 10 days or
   cleaned baseline/2.5, with trial durations 0.06, 0.09, 0.13, 0.18 and 0.24 days.
   Rank each star's strongest likelihood peak; this is not a complete multi-planet
   search. Times are BTJD (BJD TDB minus 2457000).
5. Measure local individual events, odd/even depth differences, a phase-0.5
   secondary, and the strongest peak in the sign-inverted curve. Repeat the
   entire period search with a 2.5-day detrending window. Search sinusoidal
   variability with Lomb–Scargle from 0.1 cycles/day to the smaller of 10
   cycles/day or the median-cadence Nyquist frequency.
6. Flag formal S/N <8, fewer than three local events with S/N >=2, odd/even
   differences >3 sigma, secondaries >3 sigma, inverted power >=80% of dip power,
   duty cycle >15%, period changes >2%, and crowding fraction <0.8 or missing.
   Missing odd/even or secondary measurements are also flagged. Flag sinusoidal
   likelihood improvements larger than the BLS box improvement. This is a
   heuristic comparison, not Bayesian evidence or a false-alarm probability. A flag is a
   heuristic reason for caution, not definitive astrophysical classification.

`needs_followup` means only that these simple cuts passed. It does **not** mean
planet candidate, novel object, validated detection or calibrated significance.
`flagged` includes noise, instrumental/stellar variability, eclipsing systems,
and potentially real transits that these conservative checks reject.

## Evidence

Each run writes:

- `run.json`: exact selection, settings, source hashes and catalog provenance.
- `results.json`: every target, download errors, star metadata and diagnostics.
- `ranking.csv`: strongest peaks ranked by **formal**, white-noise S/N.
- `tic-*.png`: light curves and folded views for the five strongest peaks.
- `catalog_*.csv`: the actual catalog snapshots used for exclusion.

The quick radius estimate uses `sqrt(depth) * stellar_radius * 109.076` Earth
radii, assumes an on-target undiluted transit and ignores uncertainties, impact
parameter and limb darkening. PDCSAP includes pipeline crowding corrections;
these are not proof that a dip originated on the target. Radius is not a gate.

## Scientific limits and follow-up

One inverted search is a diagnostic, **not a false-alarm probability**. Formal
BLS S/N ignores red noise and the number of periods/stars tried. Median filtering
can distort transit depths and induce artifacts. The trial grid and 30-minute
cadence can miss short or shallow Earth-size events; a null pilot result says
nothing about their absence. The synthetic tests exercise algorithm behavior,
not survey completeness. Only one sector and one processing product are searched
per run, so there is no independent-year prediction test in this implementation.

Before proposing a candidate:

- Cross-match current ExoFOP TOIs/CTOIs, confirmed planets, TESS eclipsing-binary
  catalogs, Gaia variability and literature, including positional neighbors.
- Inspect raw SAP versus PDCSAP, quality flags, momentum dumps, background,
  centroid shifts, pixels and apertures; rule out nearby eclipsing binaries.
- Recover the same ephemeris in other sectors and a separate extraction (e.g.
  QLP/TGLC). These share telescope images and are not independent observations.
- Freeze an ephemeris on training sectors and test held-out observations without
  refitting them. Report propagated timing uncertainty and missed predictions.
- Run injection/recovery over periods, radii and noise levels; calibrate detection
  thresholds with time-correlated nulls and account for survey-wide trial counts.
- Fit a physical transit model with stellar-property uncertainties and request
  expert follow-up before any public claim or external candidate submission.

No messages or submissions to ExoFOP are made by this project.

## Sources

- [MAST TESS-SPOC data, provenance and search coverage](https://archive.stsci.edu/hlsp/tess-spoc)
  ([Caldwell et al. 2020 dataset](https://doi.org/10.17909/t9-wpz1-8s54)).
- [NASA TESS data products](https://heasarc.gsfc.nasa.gov/docs/tess/data-products.html).
- [NASA Exoplanet Archive TAP](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html).
- [Astropy Box Least Squares](https://docs.astropy.org/en/stable/timeseries/bls.html).

Please credit TESS, MAST and the product authors when using these data. Existing
cataloged signals can be useful positive controls but must not be presented as
new discoveries.

## Active multi-sector campaign

[The expanded campaign report](results/CAMPAIGN-20261009.md) records a complete
85-sector coverage inventory, 11,851 eligible small stars, and the first 300-star
batch. 299 were searched successfully; two preliminary filter passes remain
unvalidated after stronger checks. The broader search goal is still active.

```sh
# Inventory currently published TESS-SPOC sectors and select small stars.
uv run python -m exoplanet.targeting --inventory \
  --output results/new-selection --limit 300
# Discover using only the selected older training sectors.
uv run python -m exoplanet.campaign \
  --selection results/new-selection/selected.json \
  --output results/new-campaign --workers 4 --limit 300
# Freeze a selected discovery peak before opening later observations.
uv run python -m exoplanet.followup \
  --discovery results/new-campaign/targets/TIC_ID.json \
  --output results/new-followup --peak-index 0
# Limited injection/recovery audit on real training data.
uv run python -m exoplanet.sensitivity --campaign results/new-campaign \
  --output results/new-sensitivity --limit 20
```

The campaign timing model is deliberately labeled provisional: a box-profile
range is not a physical transit posterior. A `followup_priority` result is a
screening label only. The committed campaign report records which later sectors
have already been inspected so future work does not accidentally reuse them as
blind validation data.
