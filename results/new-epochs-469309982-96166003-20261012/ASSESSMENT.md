# Two new QLP epochs: neither supplies a precise frozen-clock recovery

The newly accessed sector90 for TIC469309982 and sector86 for TIC96166003 do not validate either signal. Every historical clock fails the frozen timing-precision gate; expected formal sensitivity is also below5σ in every comparison. The results therefore cannot decisively exclude planets either. Both epochs are now opened and cannot be reused as fresh holdouts.

The primary469 prediction has negative measured depth, while961 is only weakly positive and disagrees with the secondary expanded clock. Positive values at alternative clocks are retained without replacing the primary predictions.

## All predeclared measurements

Depth is out-of-window minus in-window weighted flux, with formal independent-point errors. Both detrendings use the same new QLP photons. Event counts are measurable local windows / individual depth SNR≥2; they are not independently confirmed transits.

| TIC / sector | Historical clock | Detrending days | Depth ± error, ppm | Formal SNR | Events / supported | Timing spread, days | Expected formal SNR |
|---|---|---:|---:|---:|---:|---:|---:|
|469 /90|Refined9/10/36/37, **primary**|1.5|−54.3 ±31.6|−1.72|8 /0|0.1683|4.38|
|469 /90|Original seed reference|1.5|91.6 ±28.2|3.25|8 /1|unprofiled|4.28|
|469 /90|Refined9/10/36/37|2.5|14.1 ±33.8|0.42|7 /0|0.2461|4.16|
|469 /90|Original seed reference|2.5|90.2 ±30.0|3.00|7 /1|unprofiled|4.03|
|961 /86|Expanded19/43/44, **primary**|1.5|248.2 ±100.7|2.46|9 /1|1.9512|2.36|
|961 /86|Original43/44 refinement|1.5|214.1 ±91.4|2.34|10 /2|0.9380|3.08|
|961 /86|Original seed reference|1.5|221.0 ±97.4|2.27|10 /0|unprofiled|3.02|
|961 /86|Expanded19/43/44|2.5|7.2 ±134.0|0.05|7 /0|0.3702|1.87|
|961 /86|Original43/44 refinement|2.5|270.2 ±104.7|2.58|7 /1|1.0535|2.49|
|961 /86|Original seed reference|2.5|163.6 ±114.6|1.43|10 /0|unprofiled|2.56|

469 abbreviates TIC469309982;961 abbreviates TIC96166003. Every row's conclusion is `timing_prediction_inconclusive`. Profile spreads are conditional historical box-model heuristics propagated to the actual timestamps, not calibrated confidence intervals. Some961 spreads approach or exceed an orbit: that is an explicit loss of predictive specificity, not a precise negative transit prediction. Seed references have no timing profile and were ineligible for recovery by construction.

The [fixed-clock plot](fixed-clocks.png) was visually inspected.469 shows an off-primary-phase depression that partly overlaps its originally frozen seed reference; this does not authorize an adopted shifted epoch.961 has noisy folded structure and appreciable event scatter. No peak, timing offset or favorable event was selected after inspecting these figures.

## Freeze, data and processing

[PREPARATION.md](PREPARATION.md) records the no-record-of-prior-access finding: coordinator review of this thread/GOAL/CHECKED and local cache/manifests found neither product opened. This is not proof about all possible external sessions. The metadata, runner, historical clock/profile inputs and scientific source were hashed in [plan.json](plan.json) before either download. All older sectors had already been opened; no retrospective season-out clock was substituted for the historical primary.

The runner verifies exact TIC/sector and BTJD reference, uses native cadence, quality0, DET_FLUX and published positive DET_FLUX_ERR, then the predeclared1.5/2.5day flattening. No error estimation, period search, timing fit, event removal or retry occurred.469 retains9711/8890 cleaned points;961 retains3977/2887. Different detrending masks naturally alter event coverage, and all such losses remain in the results.

These products use QLP whereas the historical timing/strength estimates used SPOC. Differences in aperture dilution, reduction and reported errors limit a literal same-depth forecast. Formal errors do not include correlated noise or processing uncertainty. Each primary expected SNR is below5, so even a precisely timed absence would not satisfy the predeclared strong non-recovery sensitivity criterion here.

## Verification and disposition

[verify.py](verify.py) reconstructs all four reductions from raw FITS, checks raw identity/hash/columns and all frozen source/input hashes, independently recomputes precision-sum total and per-event measurements, verifies profile propagation and every decision, and checks plan-before-download chronology. It uses the existing detrending implementation; it does not independently validate flattening physics or white-noise assumptions. [verification.json](verification.json) passes all10 clocks. The run completed without execution failures.

Keep both candidates unresolved with weak/mixed recurrence. Do not report a successful sector90/86 prediction or interpret the alternative seed's modest positive depth as a replacement validation. These are genuine newly evaluated epochs under documented access-history limits, but their clocks and sensitivity were inadequate for decisive tests. Any future use of90/86 for timing refinement is training on opened data and needs a separately declared plan and genuinely separate later validation.

Raw files and retrieval manifests are isolated in `data/new-epochs-469309982-96166003-20261012/qlp/`; committed manifests retain URLs and SHA-256. No new source images, source-model fits, shared scientific edits or external submissions occurred.
