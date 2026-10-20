# Two targeted source tests: TIC 5546257 and TIC 402358350

## TIC 5546257: resolved-neighbor eclipses align with the refined TESS clock

Newly opened Gaia epoch photometry of the favored contaminating neighbor, **TIC 5546242 / Gaia DR 3 5426593326262323968**, provides a meaningful new clue. At the unchanged expanded TESS period and epoch, all five nominal in-window Gaia observations are dimmed. A sixth dim point lies just outside the frozen duration. This supports further investigation of that neighbor as the source, including the possibility that its published 7.2483-day period is an alias. It does **not** settle the period or override the failed timing-precision gate.

The original investigation's statement that the saved Gaia catalog orbit does not explain the TESS train remains valid. What is new is direct inspection of the resolved neighbor's individual measurements: the actual dimmings may support a different clock from the catalog fit. The catalog period mismatch should no longer be read as evidence against all variability on this neighbor at the TESS period.

The [plan](plan.json) froze the exact source, catalog model, discovery seed and expanded pre-sector62 TESS clocks before [archive access](epoch-source.json). There were 58 raw rows and 54 accepted G-band measurements. All source IDs match; both rejection flags must be false and flux/error finite and positive. No other source or new TESS epoch was opened for this experiment.

| Fixed TESS clock | In-window Gaia points | Relative depth ± formal error | Timing status |
|---|---:|---:|---|
| Original discovery seed |4 in 3 cycles|−0.398 ±0.203%|Uncertainty profile unavailable; inconclusive|
| Expanded pre-sector 62 |5 in 5 cycles|16.343 ±0.192%|Backward spread 0.1292 d exceeds half-duration 0.06653 d; inconclusive|

The large nominal expanded-clock significance is **not** a planet probability, a calibrated false-alarm probability, or a passed frozen validation. Sparse sampling and clock uncertainty remain material. Across all 13 saved period/epoch profile pairs, only 2–6 of the six conspicuously dim observations fall inside the nominal width. Those profiles are retained in full, without choosing whichever best fits Gaia.

An explicitly post-inspection [supplement](supplement-plan.json) records every point, flags and phases. The six points fainter than G=16.80 have refined TESS phases between−0.04381 and+0.02684; the magnitude threshold was chosen descriptively after inspection. Five lie inside the frozen phase half-width~0.03764. The original seed does not show the same concentration. Three fixed Gaussian widths at the refined clock reduce magnitude-space chi-square from7460 for a constant to1088,719 and1586, without fitting period or epoch. All alternatives are retained; these imperfect descriptive models do not calibrate detection significance. [Point table and model alternatives](gaia-supplement.json), [both unchanged-clock plots](gaia-candidate-clocks.png).

### What the catalog model does and does not explain

The published two-Gaussian model at exactly 7.248263937 TCB days reproduces most dimmings: chi-square falls from 7460 for a constant to 315.6 without changing the published parameters. Fitting only a magnitude intercept and scale gives amplitude 0.99873 times the published shape and chi-square 315.4. This is reproduction on the same Gaia observations used by the catalog, **not independent binary confirmation**. Its lower residual than our simple fixed Gaussian does not establish its period: its model was fitted to Gaia with more freedom, and the sparse samples allow competing arrangements.

Four nominal TESS-window points are explained by the published primary or secondary eclipses. The fifth, Gaia TCB time2625.682355, is **0.1859mag fainter than the published model** at catalog phase0.09588; it is near refined TESS phase0.02178. Its BP and RP magnitudes are also dimmer than the nearby typical levels, with both band rejection flags false. G `other_flags=1023` is retained without an unsupported interpretation. A single discrepant transit can reflect additional variability, model inadequacy or measurement problems; it is not silently removed. [Published-model reproduction](gaia-results.json), [plot](gaia-model.png).

The catalog's frequency/phase errors give formal three-sigma timing ranges within Gaia's span; covariance, evolution and model selection error are unavailable. The TESS profiles propagated backward are wider and fail the original gate. No clock was retuned to these Gaia data, and no new period search was run. Resolving the possible alias requires a separately scoped test with discriminating coverage or a predictive model comparison; repeatedly fitting these same sparse points cannot turn them into a fresh holdout.

## TIC 402358350: the known 1.05067-day pulsation does not remove the selected dip

The newly recovered published pulsation frequency of neighbor TIC 402358249, **0.9517724/day**, motivated a test not performed in the earlier telemetry analysis. Only already-opened sectors 40/41/54/81 were used. The expanded primary TESS clock was unchanged. Both SAP and PDCSAP, with 1.5/2.5-day detrending, were retained.

Local fixed-clock box fits use separate event baselines; adding sine and cosine terms at the published pulsation frequency separately for each sector permits arbitrary local pulsation phase/amplitude. The resulting combined depths are:

| Reduction | Event baselines only, ppm | With fixed-frequency nuisance terms, ppm |
|---|---:|---:|
| SAP,1.5 d |659 ±38|578 ±45|
| SAP,2.5 d |685 ±40|578 ±47|
| PDCSAP,1.5 d |626 ±38|621 ±44|
| PDCSAP,2.5 d |609 ±41|610 ±46|

Thus the simple sinusoidal nuisance model changes SAP by about 80–107 ppm while leaving PDCSAP nearly unchanged. Every sector retains a positive fitted depth; formal errors do not include full red noise or broad-baseline uncertainty. These fits show that this particular fixed-frequency model does not absorb the selected signal. They do not identify the host or exclude multiple pulsation modes, nonlinear corrections or other contaminants.

To check sampling and processing sensitivity,64 deterministic injections multiply the selected archived SAP/PDCSAP flux by a 1000 ppm sinusoid: four fixed phases, four sectors, both reductions and both detrending windows. They use the same raw masks and original flattening implementation, retain all outcomes, and compare depths on common cleaned cadences with baseline errors. No baseline cadence was lost. A sector's apparent fixed-clock depth can change by up to**1209 ppm**. This substantial transfer describes our sampling and flattening response. It does not rerun SPOC/PDC or model the instrument’s mapping from blended sources into each archived product. Poorly sampled events and our detrending can mix smooth variation into a box measurement. Four phases at one amplitude do not bound all possible nonlinear responses. Actual neighbor amplitude in the TESS aperture remains unknown; Gaia magnitude amplitude does not determine TESS throughput.

[All40 fits and64 injections](pulsator-results.json), [comparison plot](pulsator-tests.png). This is retrospective sensitivity analysis using already-inspected data, not a new independent recovery or false-alarm experiment.

## Verification and provenance

[verify.py](verify.py) passed305 checks: frozen hashes and opening chronology, Gaia identities/masks, two-part-JD TCB-to-TDB conversion, periodic catalog model, independent QR depth/error reconstruction, timing propagation, fixed Gaussian alternatives, all profile memberships, all40 nuisance fits and64 independently event-demeaned injection changes. Existing `flatten` and Astropy are shared implementations; the verifier does not independently validate their physics. The three figures were inspected and retain unfavorable alternatives.

Raw Gaia data are in ignored `data/extension-402358350-5546257-20261012/`, with URL/time/SHA-256 in the source manifest. All scientific inputs, clocks and selected cached FITS files are hashed in the plan. No shared scientific code or documents were changed. These two tests are complete; later QLP-sector investigation is a separate planned run and must not be conflated with this report.
