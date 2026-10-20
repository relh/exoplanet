# Scientific status and resumption

**The original searches and planned vetting are complete. The decisive-evidence objective remains scientifically incomplete and blocked on observing access or outreach authorization.** Six signals retain internal ambiguous planetary candidate (APC) assessments; no securely attributed new planet was established. Scientific state: 13 October 2026. The research is prepared for public release after the [privacy cleanup](docs/RELEASE-AUDIT.md); the user controls the visibility change.

Use [README.md](README.md) for the shortlist, [CHECKED-RESULTS.md](CHECKED-RESULTS.md) for evidence, and [CODE-ORGANIZATION.md](CODE-ORGANIZATION.md) for implementation and data-access rules. Historical reports can contain superseded next steps.

## Active goal — decisive evidence for the two priority signals

Requested on 13 October 2026: determine whether the investigated dips around TIC 80387959 and TIC 402358350 have a planetary origin, prioritizing TIC 80387959.

Completion requires independently reviewed evidence sufficient for planetary validation/confirmation or a reproducible nonplanetary explanation that quantitatively accounts for the measured signal. A planetary conclusion needs reliable source attribution, repeatable transits and adequate constraints on companions, blends, instrumental effects and stellar variability. A non-detection without adequate timing coverage and sensitivity is inconclusive. Excluding one neighbor, obtaining a large model weight or preparing an observing plan does not complete the goal. Conclusions concern the investigated signal, not every possible planet around the star.

| Signal | Needed evidence | Existing limits |
|---|---|---|
| TIC 80387959 | Resolved photometry of the target and viable neighbors; unresolved-companion constraints | Provisional 5.6-hour tracks; host uncertain. A target-centered dip alone would not exclude an unresolved stellar companion. |
| TIC 402358350 | Timing recovery, source attribution and companion constraints | Expanded-clock windows require 17.5–18.5 hours; older clocks disagree more. A short targeted non-detection would be inconclusive. |

Read the [resolved follow-up overview](results/followup-overview-20261013/ASSESSMENT.md), [TRICERATOPS review](results/triceratops-review-20261013/ASSESSMENT.md) and [remaining-evidence audit](results/remaining-evidence-audit-20261013/ASSESSMENT.md) before another test. SkyMapper/ZTF neighbor measurements are already inspected evidence. No candidate-investigation process was running when this objective began; inspect live processes again before resuming.

### Completed access and archive checks

| Check | Outcome and dependency |
|---|---|
| [Five-site visibility](results/site-visibility-20261013/ASSESSMENT.md) and [access assessment](results/observing-access-20261013/ASSESSMENT.md) | No robust full LCO one-meter track. The 20 March 2027 CTIO window has only 82 sidereal seconds of margin and fails the conservative mount-margin test. No full TIC 402358350 window in the tested network. |
| [T17 geometry](results/t17-feasibility-20261013/ASSESSMENT.md) and [review](results/t17-review-20261013/ASSESSMENT.md) | 28 March 2027, 12:05–17:43 UTC is the sole full sky-gate pass among 47 windows. The actual horizon, mount/meridian limits, access and precision remain unverified. The [operator inquiry](results/t17-access-inquiry-20261013/ASSESSMENT.md) is reviewed and unsent. |
| [LCO images](results/lco-archive-metadata-20261013/ASSESSMENT.md) | Nine science exposures precede the predicted event; two opened baseline frames saturate the target and principal neighbor. The apparent second-candidate spectrum points about 5.3 degrees away. Do not redownload the other seven frames without a new scientific justification. |
| [ESO raw metadata](results/eso-raw-metadata-20261013/ASSESSMENT.md) and [CHEOPS visits](results/cheops-metadata-20261013/ASSESSMENT.md) | No returned pointings within the frozen 120-arcsecond cones. Bounded metadata nonmatches do not exclude companions or exhaust off-axis footprints. No flux opened. |
| [SuperWASP](results/superwasp-metadata-20261013/ASSESSMENT.md) and [early-epoch timing](results/old-epoch-timing-20261013/ASSESSMENT.md) | Only six or seven points per returned first-candidate source over about 37 minutes; no second-candidate source. No flux opened. All original timing gates fail at the four tested 2004–2009 epochs. This does not rule out long, independently sampled observations. |

The [observation protocol](results/decisive-observation-protocol-20261013/ASSESSMENT.md) is a draft pending instrument performance and access; its precision objectives are untested. These checks do not exhaust all archives or classify either signal. Do not repeat completed queries without changed data, release or scope.

Resume with instrument/access details, authorization for the exact unsent inquiry, a relevant new dataset, or an operator response enabling a feasible experiment. Public archival queries, analysis and planning are authorized. External submissions, outreach, telescope bookings and spending require explicit authorization. Inquiry approval does not authorize a purchase or booking. Do not force a verdict, relax failed gates or invent a planet probability while these dependencies remain unmet.

## Completed extensions

All are complete within their declared boundaries, without candidate promotion. Original measurements, failed checks and contrary evidence remain in the [evidence index](CHECKED-RESULTS.md).

| Scope | Retained outcome |
|---|---|
| Original searches and vetting | [Completion audit](results/scoped-completion-20261012/ASSESSMENT.md); [companion metadata](results/companion-constraints-shortlist-20261012/ASSESSMENT.md) cannot exclude binaries. |
| Resolved-source follow-up | [SkyMapper](results/resolved-followup-803-20261013/ASSESSMENT.md) weakens one neighbor-eclipse hypothesis but fails repeated-event clearance; all 72 [ZTF](results/resolved-followup-402-20261013/ASSESSMENT.md) comparisons remain inconclusive. The [planning packet](results/followup-planning-20261013/ASSESSMENT.md) retains 64 nominal events and ten neighbors. |
| TRICERATOPS | [17 runs and three provenance replays complete](results/triceratops-20261013/ASSESSMENT.md). Million-draw target-planet weights 92.43% and 97.68% are conditional; neither passes joint validation thresholds. One million-draw seed per candidate leaves original convergence unmet. Superseded inputs, interrupted logs and recovery reasons remain archived. |
| Refereed-workflow comparison | [Noise and brightness budgets](results/refereed-vetting-20261012/ASSESSMENT.md) retain possible contaminating hosts and weaker conditional precision; no new observing epochs. |
| Web-led candidate extension | [80387959 spectroscopy](results/web-80387959-20261012/ASSESSMENT.md), [402358350 neighbor variability](results/web-402358350-20261012/ASSESSMENT.md), [241928959 literature](results/web-241928959-20261012/ASSESSMENT.md) and [spectroscopy searches](results/web-spectroscopy-20261012/ASSESSMENT.md) add context without decisive attribution or binary exclusion. |

### Strongest-lead robustness extension

[80387959 shape tests](results/strongest-80387959-shape-20261012/ASSESSMENT.md) retain dips in six sectors; the [paired-pipeline comparison](results/strongest-80387959-shape-20261012/paired-products/ASSESSMENT.md) establishes neither a universal offset nor physical depth evolution. [402358350 baseline tests](results/strongest-402358350-baselines-20261012/ASSESSMENT.md) retain eight events across twelve methods, with unfavorable controls preserved.

[Pointing correction](results/pointing-correction-controls-20261012/ASSESSMENT.md) passes three of four controls; [aperture contrast](results/strongest-host-identifiability-20261012/ASSESSMENT.md) passes five of eight. Neither met its gate for candidate application. [ASAS-SN access](results/strongest-external-access-20261012/ASSESSMENT.md) remains limited. Repeating poor source fits to already inspected observations is not independent progress.

A future source-attribution method needs independently calibrated response information or successful shallow known-host controls. Favorable fits to inspected candidate pixels alone are insufficient.

### Six-candidate continuation

[Event baselines](results/event-baseline-six-20261012/ASSESSMENT.md), [orbital modulation](results/extension-80387959-241928959-20261012/ASSESSMENT.md), [pulsation/neighbor tests](results/extension-402358350-5546257-20261012/ASSESSMENT.md) and [literature checks](results/extension-469309982-96166003-20261012/ASSESSMENT.md) are complete. Preserve newly opened observations:

- TIC 80387959 sectors 64/99 contain collateral pixels, not usable stellar observations or transit non-detections. [Geometry audit](results/new-epochs-80387959-20261012/ASSESSMENT.md).
- TIC 469309982/90 and TIC 96166003/86 remain weak and timing-inconclusive. [New-epoch tests](results/new-epochs-469309982-96166003-20261012/ASSESSMENT.md).
- TIC 5546257/89/99 show nominal-clock dips but fail timing precision. [New epochs](results/new-epochs-5546257-20261012/ASSESSMENT.md). Opened Gaia neighbor epochs strengthen contamination; the [catalog-clock mismatch](results/contaminant-clock-5546257-20261012/ASSESSMENT.md) remains unresolved.

Metadata-only footprints 96166003/71 and 5546257/8/63 were not opened. Coverage does not establish usable science pixels. Apply the detector-geometry preflight before any attempt.

## Closed queues and holdouts

| Scope | Completed state | Record |
|---|---|---|
| Solar-radius pool | 7,004 attempts; all 28 passes reviewed | [Frozen selection](results/solar-radius-pilot-selection-20261011/eligible.json) · [Ledger](results/solar-radius-lead-audit-20261011/audit.json) |
| Resumed solar queue | Ranks 4432–7003 finished; do not restart over existing outputs | [Execution](results/solar-radius-remaining-resume4432-20261011/execution.json) · [Terminal audit](results/solar-radius-terminal-audit-20261012/ASSESSMENT.md) |
| Weak-seed pool | 689 attempts; all 23 flags reviewed | [Ledger](results/weak-seed-audit-20261011/audit.json) |
| Fainter QLP expansion | 1,845 targets reconciled, including recoveries | [Report](results/qlp-faint-expanded-20261010/ASSESSMENT.md) |

The original solar queue stopped after ranks 3920–4431 because follow-up opened TIC 5546257 reserved data before its terminal audit. Retain the [exception and recovery](results/solar-radius-ranks3920-4432-20261011/ASSESSMENT.md). Historical cache-absence assertions no longer apply after observations are opened. Selections overlap; do not sum their denominators.

Before an extension, inspect the worktree, fetch origin, read current evidence and check actual live processes, manifests and caches. Missing handles, stale progress files and timeouts do not establish whether a queue is running. Use a fresh result directory and explicit ownership; do not change shared scientific code beneath a live queue.

Complete the [data-opening preflight](CODE-ORGANIZATION.md#before-opening-additional-observations) before access. Freeze inputs, clock, timing envelope, coverage, sensitivity and decision rules. The generic follow-up command automatically opens reserved data. Already inspected epochs and reductions of the same photons cannot become fresh independent holdouts. Omitted-year tests must disclose original selection history. Preserve all negative outcomes and label refits or altered gates exploratory.

## Handoff

Update existing candidate rows and link detailed measurements, aliases, failures and limitations. Keep source identity, planet plausibility and novelty separate. Qualitative priorities and agent agreement are not calibrated probabilities or scientific validation. The [model-feasibility review](results/probability-feasibility-20261011/ASSESSMENT.md) records additional assumptions and missing constraints.

Before closing an extension, reconcile attempts, passes and errors, verify adopted results, update the index and synchronize private main. Record actual process state if interrupted. Preserve raw evidence and protected agent histories. [README-HISTORY.md](README-HISTORY.md) and [GOAL_PROGRESS.md](GOAL_PROGRESS.md) are historical snapshots, not restart instructions. [External leads and method inspirations](results/user-posts-20261010/NOTES.md), including HD 32564, remain distinct from our findings.
