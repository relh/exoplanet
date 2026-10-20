# TIC 156001092: unresolved diagnostic

Training sectors [68, 69]. Native refinement: period 13.423921391 days, duration 0.216000 days, depth 2176 ± 199 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: A broad asymmetric depression with a large folded gap after the selected event. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 2: timing_prediction_inconclusive, timing spread 7.7958 days. Sector 28: timing_prediction_inconclusive, timing spread 4.8105 days.

Training off-phase scan's selected maximum has formal SNR 2.74; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source and quality checks below leave attribution unresolved; novelty remains unestablished. No secure host, novelty, or credible planet claim; retain for further review.

## Source and quality review

Both raw stacks, all four raw individual maps, and the sector 69 processed stack and both individual maps were inspected. Raw maps have positive field-wide backgrounds, with a strong gradient in sector 68. Both processed sector 69 events have a positive target-adjacent residual, but also positive residuals at TIC156001093 and negative residuals at TIC156001088. This recurring multi-star pattern warrants background/motion/source modeling; it does not securely attribute the dip to one host. The formal maximum pixel SNR9.80 is not calibrated source confidence. Same photons across processing are not independent confirmation. No Gaia host inference was made.

Raw sector 68 inside counts are 93/93 and baseline counts372/372; sector69 counts are93/94 and373/374, all quality zero. All186 processed sector68 inside exposures are flagged (184flag4096, twoflag32768), with0/183 quality-zero baseline exposures; its aggregate analysis fails the unchanged two-event gate. Processed sector69 inside93/94 and baseline242/289 are quality zero. Missing usable data is not a nondetection.

The39-row neighbor query, downloaded pixel provenance, scripts, counts, maps and failures are retained and verified by `verify_pixels.py`. This remains an unresolved diagnostic with tentative sector69 target-region structure and substantial background/quality concerns, not a likely planet candidate.

## Masked-plane sensitivity diagnostic

A posthoc sector69 processed-image check fits an unweighted plane outside all catalog sources brighter than T17, with source exclusion radii1.5 and2.0 pixels (83/59 background pixels). It uses the existing `fit_templates` routine with no source templates, unchanged event maps, and no tuning of masks after viewing results. All six [comparison panels](../../background-156001092-20261011/comparison.png) were inspected.

The target-adjacent positive feature survives both masks in events2/3. Sums inside a fixed1.5-pixel target aperture are2.05–2.23 and3.46–3.79 in residual flux units. TIC156001093 remains positive (0.35–0.46 and1.84–2.26), while TIC156001088 remains negative (−5.67 to−5.57 and−2.73 to−2.41). These are sums, not transit depths or detection significances. The recurring multi-star pattern survives removal of this simple background model. A planar offset/gradient alone is insufficient; source/PRF/motion effects and blends remain plausible. The target source still is not securely identified.

Four deterministic controls (pure plane and plane with positive/negative compact sources, each under both masks) recover the input residuals to below1e−10 absolute error. These check arithmetic only, not realistic PSF wings, red noise, nonlinear background or motion. Source wings outside masks can bias the fitted plane. No probabilities or new independent recurrence evidence are inferred. Next useful test is a joint stellar-scene/motion model with realistic injections and controls, not planet promotion.

## First-order common-motion diagnostic

A separate posthoc check adds the x/y gradients of the archived processed median image to a plane, using the unchanged linear fitter. The target is excluded with radii2.0/2.5pixels (108/101 fitting pixels); the remaining scene constrains coefficients. This is an empirical first-order shift model, not a mission-PRF scene fit or measured spacecraft displacement. All six [panels](../../motion-156001092-20261011/comparison.png) were inspected.

Target-adjacent residuals persist in both events and masks, with1.5-pixel aperture sums2.96–3.13 and3.89–4.05 residual-flux units. The positive residual at156001093 and negative residual at156001088 also persist. Outside-mask residual sums of squares decrease only modestly relative to a plane on identical pixels: event2 10.25→9.60 and9.73→9.02; event3 6.64→6.28 and6.14→5.71. Improvement is expected for a nested model and is not calibrated significance. A single first-order common shift does not explain the full pattern under these assumptions. No unique host or physical cause is established.

Deterministic controls recover pure derivative-plus-plane scenes to below1e−9 and retain95.996%/99.169% of a unit-normalized Gaussian target injection's total flux. Gaussian width0.8pixel and amplitude3 were fixed; this tests one injection shape, not realistic PRF mismatch, nonlinear motion, blended variability or red-noise calibration. Real stellar wings can bias the fit. The next useful extension is a mission-PRF scene model with per-source signed changes and matched off-event controls; neither current correction justifies planet promotion.

## Initial mission-PRF scene fit

Four bracketing mission PRF grids were downloaded with URLs and hashes. A seven-star T<17 scene uses unpropagated TIC positions and a common shift fitted only to the out-of-event median. Registration is(−0.0090,−0.0047)pixels, not at its bound. Scene residual RMS is3.27% of the peak scene pixel, with a large structured edge residual. All nine [scene/event panels](../../prf-156001092-20261011/comparison.png) were inspected. This initial scene is imperfect; missing edge sources, proper motion and PRF mismatch require testing before source attribution.

Simultaneous signed source amplitudes plus a plane give target coefficients3.68/6.19 for events2/3; adding derivatives of the registered scene gives2.95/5.86. Nearby156001090 gets1.40/0.40 in the latter fit;156001093 remains positive1.11/3.85 and156001088 negative−8.67/−4.35. These conditional flux coefficients are not transit depths or source probabilities. Motion fits retain structured residuals, with formal chi-squared229.62/227.39 for109 degrees of freedom. Error correlations and model mismatch make those statistics uncalibrated. The model does not establish a unique host.

Six exact mission-template injections (target, nearby156001090, and156001088 in both event error maps) recover signed input coefficients to below1e−6. This tests the linear solver, not wrong PRFs/registration. Ten forward shifted event-window controls were attempted at fixed fractions0.15/0.35/0.55/0.75/0.95 of the period, excluding true windows. Four have usable coverage, all associated with event2; six failures are retained. Control target coefficients range−0.70 to+0.28, below selected-event coefficients, but this small overlapping set is not a false-alarm calibration. Target injections of flux5 into those controls are recovered algebraically; that does not validate the host model.

**Next:** expand/test the edge scene and catalog astrometry, then compare PRF and registration perturbations with broader matched controls. Target-region structure remains interesting but unresolved; no planet promotion or new independent recurrence claim.

## Expanded edge-scene sensitivity

Expanding the fixed T<17 catalog selection to three pixels beyond the stamp adds six sources (13 total), with unchanged fitting algorithms and the same cached mission grids. All nine new scene/event panels were inspected. The out-of-event scene residual RMS drops from3.27% to0.563% of the brightest scene pixel, substantially reducing the previously prominent edge mismatch. Registration(−0.00745,−0.00837)pixels remains away from its bound; TIC positions are still unpropagated.

With simultaneous signed source amplitudes, scene derivatives and a plane, target coefficients remain positive2.67/5.69 in events2/3, versus2.95/5.86 in the smaller scene. Formal fit statistics are194.83/207.02 for103 degrees of freedom, with structured event residuals still visible. Large signed coefficients on partially off-stamp sources should not be interpreted as measured physical variability; such columns are weakly constrained and may absorb model error. No calibrated host probability follows from improved fit quality. Six exact-template controls still pass, but omit PRF/astrometric mismatch.

The original forward-window control schedule is preserved and rerun with the expanded model: four usable, six unavailable. A separately recorded exploratory expansion uses backward/forward fractions0.1–0.9, retaining all36 attempted rows. There are21 measured rows but only14 distinct time centers (seven duplicate windows), plus15 unavailable rows. Target coefficients span−6.59 to+2.11, while selected-event coefficients are+2.67/+5.69. The negative excursion and overlapping/selected controls prevent assigning a false-alarm rate or treating every row as independent. Target-injection recovery is an algebraic matched-model check, not source validation.

The improved edge scene preserves the target-region lead, but host attribution remains unresolved. Next tests should propagate catalog astrometry and perturb registration/PRF assumptions, retaining the nearby156001090 alternative and signed neighboring residuals.

## Gaia astrometry sensitivity

Gaia queries for the13 scene stars return13 DR2-to-DR3 mapping rows and13 source rows. Eleven stars have unique mappings with usable proper motions. TIC156001088 has two mappings, both preserved as ambiguous; TIC156001098 has no TIC Gaia identifier. Those two retain original TIC positions in this sensitivity fit rather than being removed or assigned an arbitrary match. Unique mapped positions are linearly propagated to the median S69 epoch; target displacement from the original TIC position is0.0550pixel and nearby156001090 displacement0.0215pixel. Parallax/perspective and mapping uncertainty are not modeled. The calculation agrees with Astropy angular propagation within0.001arcsec for all returned mappings; this checks arithmetic, not catalog-match validity.

The target Gaia DR3 source4925004329347726976 has a SOLAR_LIKE classifier row (score0.56447, not a probability for this transit source). No queried eclipsing-binary rows were returned. This does not exclude uncataloged binary/stellar variability or prove novelty.

All nine propagated-scene/event panels were inspected. Scene RMS becomes0.475% of its peak, versus0.563% previously; common registration is(−0.0198,−0.0397)pixels. Target coefficients with scene gradients remain positive2.81/5.64; nearby156001090 coefficients1.26/0.49. Structured residuals persist, with formal chi-squared196.78/207.61 for103 degrees of freedom. Six exact-template controls pass, but these do not calibrate PRF mismatch, ambiguous astrometry or correlated errors. Prior off-event controls belong to earlier scene configurations and were not rerun for this variant. Host attribution remains unresolved; registration/PRF perturbations and ambiguous-match variants remain useful tests.

## Registration, PRF and ambiguous-match grid

All36 prespecified sensitivity variants were evaluated: both Gaia mappings for156001088, common x/y registration offsets−0.1/0/+0.1pixel around the propagated-scene alignment, and sampled PRFs with Gaussian broadening sigma0/0.4pixel. Scene fluxes are refitted nonnegative plus a plane; event fluxes are signed with scene derivatives and a plane. No variant was dropped for an unfavorable outcome. These settings are not a probability distribution or estimated uncertainty range. Off-stamp template flux is not renormalized.

The two [coefficient plots](../../prf-156001092-sensitivity-20261011/sensitivity.png) were inspected. Target coefficients remain positive in all variants: event2 spans1.90–3.74, event3 spans5.04–6.44. Nearby156001090 spans0.94–1.74 and0.12–1.14 respectively, trading flux with the target as registration changes. Scene fractional RMS spans0.468–2.756% of peak; some perturbations deliberately fit worse. These are conditional flux coefficients, not depth/error bars or proof of an on-target transit.

Across144 deterministic cross-model fits, injected original target flux5 is recovered as4.76–5.33 at the target, with up to about0.29 assigned in either sign to090. Injecting original090 flux5 gives4.41–5.81 at090 and−0.75 to+0.72 at the target. This measures cross-talk for the chosen mismatch settings; it omits realistic noise/PSF evolution and cannot bound every contaminant. Original models are retained. Off-event controls have not yet been refitted through this36-model grid, so the earlier control range is not a calibrated comparator for every new configuration.

The lead survives the tested small perturbations, but source/flux assignment remains model-dependent. No secure host or planet promotion. Matched controls across the same model grid and epoch-level checks remain necessary.


## Off-event controls through the same 36 models

The archived 36-model grid and prior broader off-event schedule were reused without changing the ephemeris or choosing windows by their results. All 72 selected-event fits reproduce the archived coefficients and fit statistics within 1e-8. Of 36 attempted control rows, 21 have enough coverage and 15 remain unavailable. Exact inside/outside exposure-mask hashes identify only 14 distinct measured windows; seven rows duplicate earlier windows. There are 504 unique-window/model fits, not 504 independent controls.

Both panels of the [matched-control comparison](../../prf-156001092-matched-controls-20261011/controls.png) were inspected. Across the grid, target control coefficients range from −12.00 to +8.21, versus selected-event coefficients of +1.90–3.74 and +5.04–6.44. Comparing each event only with controls from its own model, events 2/3 exceed the largest positive control in 20/36 and 28/36 models. They exceed the largest absolute control excursion in 0/36 and 4/36 models. The positive-control comparisons are identical within each broadening subgroup (10/18 and 14/18), so the issue is not confined to the broadened templates. Neighbor 156001090 control coefficients range from −7.47 to +5.52; its selected-event coefficients exceed the positive-control maximum in only 10/36 and 0/36 models.

These counts describe sensitivity, not probabilities, false-alarm rates or a calibrated detection threshold. Controls share one sector and have uneven exposure/baseline coverage; neighboring windows and pixels may be correlated. Large negative excursions are diagnostic of unstable source/background separation, not planetary transits. Some scene variants fit poorly by construction, and none is assigned a posterior weight. The two dips remain positive under these settings, but their separation from off-event variability is not robust across the tested models. This weakens the lead; host attribution and a planetary explanation remain unestablished.

Reproduction checks, exact-mask deduplication, complete-grid checks, input hashes and recomputed summary comparisons pass. The existing deterministic injection tests are retained; no new astrophysical calibration is claimed. Further useful work is epoch-level target/neighbor photometry with fixed source assumptions and assessment of the large off-event excursions, or redirecting effort to another unresolved lead. Repeating small variants of this same scene fit alone will not establish a planet.
