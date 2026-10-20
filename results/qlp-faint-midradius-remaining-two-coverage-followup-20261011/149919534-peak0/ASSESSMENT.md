# TIC 149919534, peak 0: diagnostic only

Training sectors [74, 75] select seed period 16.10945333 days. Native refinement gives period 16.04290680 days, duration 0.216000 days and depth 2327 ± 249 ppm (formal selected fit error). 2 individual events meet the support threshold. Retained discovery flags: fewer_than_3_supported_events, crowding_or_missing_crowding. Admitted only under a diagnostic follow-up policy; original failed gates are not waived.

Sector 14: timing_prediction_inconclusive, spread 8.2888 days; Sector 21: timing_prediction_inconclusive, spread 7.3493 days. Inconclusive prediction neither confirms nor reliably excludes the proposed signal. Off-phase selected dip SNR 4.98 is an uncalibrated maximum, not a false-alarm probability or binary classification.

The discovery plot was inspected: Broad asymmetric depression with large phase gaps. The source checks below leave attribution unresolved. Host attribution and novelty are unestablished. No credible new planet claim or external submission.

## Pixel review

Raw and processed sector 75 stacks and both individual images in each processing were inspected. The raw images are positive across the field with background gradients. Both individual events also contain relative positive structure near the target, visible in the processed images as well, but mixed residuals and a gradient remain. The processed stack has formal maximum pixel SNR 4.56, an uncalibrated diagnostic rather than source confidence. These tentative target-region residuals merit background/source modeling if pursued; they do not securely identify the host. Same photons in different processing are not independent confirmation.

Sector 74 raw events have 93/0 quality-zero inside exposures and 187/0 baseline exposures; all 94 exposures in event 0 carry flag 2048. Both processed sector 74 windows are fully flagged 4096 (93/94 exposures), with no quality-zero baseline. Both sector 74 image analyses fail the unchanged two-event gate. Sector 75 raw inside counts are 93/93 and baseline counts 373/373; processed counts are 93/94 and 353/374 respectively, all quality zero. Missing usable coverage is not a nondetection.

The 24-row neighboring-star query and all downloads, errors, scripts, plots and coverage audits are retained, with hash verification in `verify_pixels.py`. No Gaia host inference was made from unreliable moments. The held-sector timing remains inconclusive and novelty unestablished. This remains an unresolved diagnostic, not a likely new planet candidate.


## Background and common-motion sensitivity

Two fixed planar-background fits exclude all catalog sources with T<17 using radii 1.5 and 2 pixels, leaving 89 and 78 background pixels. All six [comparison panels](../../background-149919534-20261011/comparison.png) were inspected. Target-region positive residuals persist in both processed sector 75 events. Target aperture sums are 2.17–2.28 and 3.23–3.38 in residual flux units, not transit depths or detection significance. Positive residuals also remain near TIC149919536 and TIC149919530; overlapping apertures cannot establish separate variable sources.

A second diagnostic uses fixed x/y gradients of the archived median image plus a plane, excluding a target circle of radius 2 or 2.5 pixels (110/100 fitted pixels). This approximates a small common image displacement, without a physical attitude or PRF model. All six [motion panels](../../motion-149919534-20261011/comparison.png) were inspected. Target aperture sums remain positive at 1.96–2.16 and 3.04–3.34, but the residual shape depends on the mask. The wider mask introduces a stronger positive/negative structure near the target in event 1. This is not evidence that motion is fully excluded or that an isolated target transit has been identified.

On identical fit pixels, adding gradient terms reduces plane-only RSS from 3.20 to 3.15 / 2.74 to 2.47 for event 1, and 2.96 to 2.94 / 2.17 to 2.10 for event 2. A nested-model RSS decrease is expected and is not calibrated significance. Neighbor residuals persist, and the gradients can absorb source variability or processing artifacts. No selected fit is treated as the true background.

Four exact-plane/compact-source synthetic checks recover residuals within 1e-10. Exact derivative-plus-plane null controls leave residuals below 1e-9; a fixed Gaussian target injection retains 93.4%/99.5% of its total flux for the two masks. These check implementation and attenuation for one assumed shape, not realistic PRF mismatch, correlated noise, host attribution or false-alarm rates. Source hashes, masks and recorded aperture arithmetic were verified; the original processed data and failed sector 74 quality gates remain unchanged.

The target-region feature survives these simple models, but host attribution, independent recurrence and novelty remain unestablished. A joint stellar PRF scene with matched off-event controls is the useful next diagnostic; a more elaborate background fit alone is insufficient for candidate promotion.


## Joint mission-PRF scene and matched controls

A six-star scene uses the mission PRF grids bracketing the sector 75 stamp, T<17 catalog neighbors within three pixels beyond the image, and a common registration fitted only to the out-of-event median. The registration is (+0.0551, −0.0477) pixels, away from its search bound. Scene residual RMS is 0.433% of the brightest scene pixel, but localized structure remains. TIC positions are not proper-motion propagated, and no PRF uncertainty is modeled. All nine [scene/event panels](../../prf-149919534-20261011/comparison.png) were inspected.

Signed simultaneous source coefficients with scene gradients and a plane give target flux changes of 1.86 and 3.66 in events 1/2. Nearby TIC149919536 receives 1.36 and 1.75; TIC149919530 receives 0.076 and 1.23. Omitting gradients gives target coefficients 2.25/3.95 and neighbor536 coefficients 0.50/1.07, showing model-dependent flux assignment. Formal chi-squared with gradients is 136.62/176.79 for 110 degrees of freedom, and structured residuals remain, especially around the second event's central pixels. These are conditional fluxes and diagnostic fit statistics, not depths, source probabilities or physical error bars.

The previously used backward/forward control schedule (fractions 0.1–0.9 of a period, excluding all true-event windows from the comparison) was transferred before inspecting this fit. It retains 36 attempts: 13 measurable rows, 23 with insufficient coverage. Exact inside/outside exposure-mask hashes identify eight distinct measured windows; five rows are duplicates. Target control coefficients span −0.80 to +2.02, so one exceeds event 1's +1.86; event 2's +3.66 exceeds this small control set. Neighbor536 controls span −1.97 to +0.54, and neighbor530 controls −0.59 to +1.15. The selected events cannot be assigned uniquely to a star from those comparisons. Controls are sparse, overlapping and unevenly covered, and do not give a false-alarm rate or establish absence of larger systematics elsewhere.

Six exact-template source injections recover the intended signed coefficients within 1e-6; added target flux 5 is also recovered within 1e-6 on every measured control. These linear-model identities test implementation, not misspecified PRFs, motion, catalog astrometry or correlated errors. Pixel/grid download hashes and all model/control provenance were verified, including duplicate masks and retained insufficient windows.

No host or planet promotion follows. Useful next work is catalog astrometry/neighbor classification and limited registration/PRF sensitivity with the same controls, while preserving the failed sector 74 quality gates and inconclusive independent-sector timing.


## Gaia mapping and proper-motion refit

The six scene stars each have one returned DR2-to-DR3 mapping and a source row with usable proper motion. No rows were returned from the queried Gaia variability-classifier or eclipsing-binary tables. This is a catalog nonmatch, not evidence against uncataloged variability, binaries or contamination. All queries, returned rows and raw-response hashes are retained in [the Gaia audit](../../gaia-149919534-scene-20261011/astrometry-audit.json).

Linear proper-motion propagation to the median sector 75 epoch moves positions by 0.006–0.044 pixels relative to TIC, including 0.0242 at the target, 0.00692 at neighbor536 and 0.0441 at neighbor530. The approximation ignores parallax and radial perspective; comparison with Astropy angular propagation agrees within 0.001 arcsec for all six stars. This checks arithmetic rather than match correctness. The same six scene stars remain in the refit.

All nine [propagated-scene panels](../../prf-149919534-astrometry-20261011/comparison.png) were inspected. Scene residual RMS changes from 0.433% to 0.393% of peak; registration becomes (+0.0712, −0.0365) pixels, away from its bound. With scene gradients, target event coefficients are 1.83/3.62 and neighbor536 coefficients 1.41/1.80. Formal chi-squared is 136.14/175.79 for 110 degrees of freedom. Central structured residuals persist, so the better scene agreement does not identify a unique variable source.

The identical off-event schedule is rerun with the propagated scene: 13 measured rows, eight distinct exposure masks, five duplicates and 23 insufficient attempts. Target control coefficients span −0.82 to +2.00; the positive maximum still exceeds the first selected dip. Neighbor536 controls span −2.27 to +0.55, and neighbor530 −0.67 to +0.99. These are conditional flux comparisons in a small, unevenly covered control set, not false-alarm probabilities. Six exact-template injections and all measured-window linearity checks still pass, without calibrating model mismatch.

Astrometry correction therefore leaves the scientific status unchanged: unresolved host and planetary interpretation, with inconclusive independent-sector timing. Limited registration/PRF perturbations should use these same control windows; catalog absence and positive fitted target coefficients alone are insufficient for promotion.


## Matched registration and PRF sensitivity

All 18 prescribed variants combine common x/y offsets −0.1/0/+0.1 pixel with sampled-PRF Gaussian broadening sigma 0/0.4 pixel, retaining the six Gaia-propagated stars. Every variant refits the scene, both selected events and the same eight distinct off-event windows. All 36 attempted control rows remain recorded, including five duplicate measurable windows and 23 insufficient rows. The reference setting reproduces all six source coefficients in both events and eight controls within 1e-8. Model settings are sensitivity choices, not posterior samples; no variant is selected by a favorable event outcome.

Both [comparison panels](../../prf-149919534-sensitivity-20261011/controls.png) were inspected. Target coefficients remain positive: event 1 spans 1.68–2.08 and event 2 spans 3.43–4.11. Control coefficients across models span −1.93 to +2.26. In every variant, event 1 is below that model's largest positive control; event 2 exceeds both its positive and absolute control maxima. Neighbor536 coefficients span 1.34–1.66 and 1.52–2.29, exceeding positive controls in all variants but remaining below the largest absolute negative excursion. Neighbor controls span −2.95 to +0.71. Neither eight windows nor 18 model settings establish independent trials or a false-alarm probability.

Across 72 deterministic cross-model injections, original target-template flux 5 is recovered as 4.92–5.35 at the target, with −0.24 to +0.04 assigned to neighbor536. Original neighbor536-template flux 5 gives 4.49–5.80 at that neighbor and −0.63 to +0.48 at the target. This tests one restricted family of model mismatch; it omits realistic noise, PRF evolution and other contaminants. Scene residual RMS spans 0.393–1.718% of peak, and some perturbations intentionally fit worse. These ranges are conditional fluxes, not physical error bars.

The second target-region event remains interesting, but the two-event recurring target-transit interpretation lacks a clean first event and unique source attribution. No promotion to a likely planet candidate. Further small model perturbations alone are unlikely to resolve the source; time-resolved target/neighbor photometry or other-sector source diagnostics would provide more useful evidence. Original independent-sector timing remains inconclusive.


## Time profiles and baseline-side sensitivity

A posthoc morphology check keeps the propagated stellar scene fixed and uses quarter-duration bins over ±3 durations around both frozen event centers. The strongest positive and negative target controls from the previous fixed-model analysis are included explicitly as selected controls, not new independent tests. Each of the four windows has all 24 bins measurable. Positive flux means fainter than its local baseline. Difference variances include the negative covariance term when bin and baseline share exposures; correlations across bins and pixels remain uncalibrated.

All four [time-profile panels](../../prf-149919534-timeprofiles-20261011/profiles.png) were inspected. Event 1 has a central rise in both target and neighbor536 coefficients, with substantial surrounding variability. The positive control also shows a central target rise. Event 2's target profile changes from negative before the selected window to positive afterward and remains elevated well beyond the nominal dip. Neighbor536 has its own central structure. These profiles do not isolate a stable target-only transit.

Motivated by that visible trend, an explicitly posthoc comparison retains before-only, after-only and both-side baselines for every window, with unchanged central interval and fixed scene. Target coefficients are:

| Window | Before-only | After-only | Both sides |
| --- | ---: | ---: | ---: |
| Event 1 | 1.59 | 2.06 | 1.83 |
| Event 2 | 5.94 | 1.29 | 3.62 |
| Selected positive control | 3.04 | 0.97 | 2.00 |
| Selected negative control | −0.22 | −1.42 | −0.82 |

These are conditional flux coefficients, not depths or physical confidence intervals. Event 2's large baseline dependence shows that the earlier positive two-sided measurement is strongly affected by the surrounding change. Neither side is selected as correct; a real transit could coexist with variability. Neighbor536 remains positive in event 2 (1.58/2.04 before/after baselines), further preventing unique host attribution. The existing all-model comparison held this baseline choice fixed and therefore did not capture this uncertainty.

Ninety-six exact-template box/gradient controls and 24 box-plus-linear-trend controls verify the contrast arithmetic within 1e-8. The expanded overlapping-exposure variance identity was checked in every bin. All four both-side integrated fits reproduce previous six-source coefficients within 1e-8. These checks do not calibrate real astrophysical or instrumental trends. This lead is weakened and remains diagnostic only. Further work should require evidence from additional usable epochs or a demonstrably reliable variability treatment, rather than refining the same selected dip's positive coefficient.
