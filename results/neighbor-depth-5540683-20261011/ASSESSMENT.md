# TIC5540683: percent-level neighboring eclipses favored

The off-target source responsible for TIC5540688's shallow discovery dip has a much deeper signal in apertures centered on neighbor5540683. Existing discovery pixels support approximately3% intrinsic dimming under the tested scene models. A stellar eclipse is a plausible, favored interpretation when combined with the neighbor's nominal TIC radius, but its physical classification is not confirmed.

| Sector | 1-pixel radius aperture depth | 1.5-pixel radius aperture depth | Intrinsic depth: fixed catalog ratios | Intrinsic depth: neighbor normalization free |
|---|---|---|---|---|
|8|2.669 ±0.021%|2.038 ±0.013%|2.963%|3.296%|
|9|2.150 ±0.012%|1.583 ±0.008%|2.897%|2.719%|

Aperture uncertainties are propagated formal pixel errors, not total uncertainties. All15 parent image events were retained:6 in sector8 and9 in sector9. Event-to-event variation exceeds formal errors in places; the inspected figure retains it. No event was removed to improve agreement.

## What these depths mean

Direct measurements sum the neighbor-centered aperture flux in each original event's inside window and compare it with the same local outside window used by the parent image test. The clock is the unchanged image-analysis period2.5206000663days, duration0.132day and epoch1519.746297965. We did not use the slightly different morphology-review clock or optimize timing.

The aperture depths are **conditional lower bounds** on neighbor fractional dimming only if that neighbor supplies the variable flux, other aperture light is stable and nonnegative, and background subtraction and pointing do not introduce the deficit. Background-subtracted pixel products alone do not prove these assumptions. The larger apertures are more diluted, explaining why their apparent dips are shallower. These values are averages inside a fixed box, not fitted central eclipse depths.

The intrinsic estimates divide the parent difference-image neighbor amplitude by its inferred out-of-event flux coefficient. First, one shared amplitude and a plane fit the full catalog-ratio scene; second, the neighbor amplitude is free while other sources retain their relative ratios. Registration, PRFs and scene membership remain fixed. Both models retain positive neighbor flux. Scene residual RMS relative to peak is1.394%/1.384% for sector8 and0.206%/0.190% for sector9 (fixed/free). Their difference is a sensitivity test, not a confidence interval; errors in catalog fluxes, PRFs, unresolved companions and background can affect both models together.

The cached TIC entry for5540683 lists radius1.95124solar radii, mass1.13solar masses, Teff6063.4K and distance711.216pc. These are catalog estimates, not independently validated stellar properties. If that radius describes the actual host and an opaque dark occulter crosses a uniform stellar disk, the2.72–3.30% depth range corresponds approximately to a blocking radius0.32–0.35solar radii. That is a stellar-scale size argument under restrictive assumptions, not a measured companion mass or proof of a binary. A smaller unresolved host, erroneous radius, different geometry, limb darkening and luminosity dilution can change the interpretation. Percent-level depth alone does not exclude a planet around a smaller star.

The target5540688 planet interpretation remains strongly disfavored by the [parent localization](../prf-5540688-20261011/ASSESSMENT.md). This test supplies physical context for the contaminant; it does not turn5540683 into a new validated binary or planet. No Gaia variability classification was found in the existing catalog review, which does not contradict an uncataloged eclipsing source. Source-centered stellar characterization and eclipse-shape/secondary diagnostics would be more informative than blind validation of the contaminated target light curve.

## Provenance and verification

Only previously opened sector8/9 target pixel files, parent catalog, cached PRFs and templates were used. plan.json records the source hashes, unchanged clock inputs, both apertures and both model conventions. results.json retains every inside/outside mean, propagated variance, pixel mask, event depth and fitted coefficient. run.py and plot.py reproduce the calculations and inspected depths.png.

verify.py independently reconstructs all30 event/aperture depths from hashed raw pixels, checks four aggregate aperture estimates and uses a separate QR solver for four baseline scene fits and two difference fits. It also verifies parent-array hashes, input and script hashes, exact FITS identity, and unopened35/36/62 caches. No new observations or source-code changes were made. This is arithmetic/provenance verification, not calibration of dilution or physical classification.
