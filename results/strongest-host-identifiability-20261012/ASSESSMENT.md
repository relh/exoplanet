# Raw aperture contrast fails the shallow known-host control

A new, template-free paired-aperture diagnostic correctly recognizes the obvious offset contaminant but fails to identify known Kepler-93's host consistently. **Five of eight predeclared cases pass; three fail. No candidate-event photometry was evaluated with this method.** This does not resolve or reject TIC80387959 or402358350, and the earlier failed pointing-correction gate was not relaxed or bypassed.

## Concrete real-control test

At each archived, proper-motion-propagated catalog position, circular apertures with radii1.0 and1.5 pixels select pixel centers. Shared pixels are excluded from both sides. For every unchanged-clock event, the diagnostic is the mean out-minus-in flux per exclusive expected-host pixel minus the corresponding mean for the competing region. Equal area normalization cancels a spatially constant background difference. It does not cancel gradients, scene motion or correlated pixel noise. No fitted registration, PRF, pointing correction, timing search or transit-depth model is used.

Kepler-93/TIC137151335 is compared with137151319, the earlier wrong preferred source in sector41. The resolved contaminant control compares region780959515 near106583444 with target106583384; that region's exact close-component identity remains unresolved. These adversarial pairs were selected from earlier reports, so this is a retrospective method check, not a blind calibration sample.

[plan.json](plan.json) froze all raw/clock/position hashes and the complete gate before measurements: every sector/radius must have nonempty exclusive regions, positive precision-weighted contrast with formal SNR≥3, and positive contrast after **every** single-event omission. All events are retained; individual and omission outcomes are recorded. No favorable radius replaces a failed radius.

| Control | Sector | Radius, pixels | Contrast formal SNR | Gate |
|---|---:|---:|---:|---|
| Kepler-93 |40|1.0|2.82|fail: below threshold|
| Kepler-93 |40|1.5|3.88|pass|
| Kepler-93 |41|1.0|−2.35|fail: wrong preferred region|
| Kepler-93 |41|1.5|−2.01|fail: wrong preferred region|
| Resolved contaminant |33|1.0|122.86|pass|
| Resolved contaminant |33|1.5|113.11|pass|
| Resolved contaminant |34|1.0|180.27|pass|
| Resolved contaminant |34|1.5|144.83|pass|

Six events per Kepler-93 sector and ten per contaminant sector are included. The plot exposes strong event-to-event deviations in Kepler-93 sector41. This was not repaired by removing early events. The formal contrast error propagates supplied pixel errors assuming independence; empirical event-scatter errors are also saved and are not a calibrated covariance model. Success on a large displaced signal does not calibrate a shallow blended signal.

The metric measures **differential variable flux per pixel**, not diluted fractional transit depth, full aperture throughput or an unbiased centroid. Aperture median fluxes are preserved for context but not converted into planet sizes. Source-response asymmetry alone can undermine a simple expected-sign rule; the gate is an empirical diagnostic requirement, not a theorem about every host's light distribution.

## Useful geometry bounds without candidate flux application

After the failed real-control gate, a separately labeled geometry-only calculation examines archived candidate positions and11×11 stamp boundaries. It opens no candidate event arrays and compares no candidate fit amplitudes or χ² values. The same1.0/1.5pixel aperture masks demonstrate how little independent spatial information such comparisons can contain:

| Target | Archived candidate-region comparisons across sectors/radii | Identical masks | One or both exclusive regions empty |
|---|---:|---:|---:|
|80387959|30|2|12|
|402358350|744|6|22|

The803 comparisons cover three neighboring hypotheses in each of five sectors; projected separations are only0.351–0.637pixels. The402 set includes the archived hypothesis list in four sectors and separations0.201–2.995pixels. Counts describe individual sector/radius masks, **not independent sources, trials or probabilities**. An empty exclusive region makes this particular contrast undefined; identical masks give literally identical aperture sums. This is a finite geometric limitation of these pixel-center apertures, not proof that all subpixel source inference is impossible. Nonempty masks do not imply enough signal or reliable response calibration.

These bounds explain why simply shrinking or shifting circular apertures is not an assured route to identifying the two strongest hosts. More elaborate fractional-pixel apertures, common-response models or covariance weighting impose additional assumptions and would need their own real-control validation; none was tuned after seeing these failures.

## Verification and decision

[verify.py](verify.py) independently reconstructs all raw event maps with nearest-cycle arithmetic, masks, equal-area contrasts, variances, precision sums and every leave-one-out result. It checks every frozen input hash and all eight gates. [verification.json](verification.json) passes. [verify-geometry.py](verify-geometry.py) independently checks774 geometric comparisons with scalar pixel-set intersections; [geometry-verification.json](geometry-verification.json) passes. [controls.png](controls.png) was visually inspected and retains the wrong-host control outcomes.

Stop this diagnostic before candidate photometric application. A source-specific conclusion for80387959/402358350 still requires a method that passes shallow real-host controls or independently resolved evidence. No new raw data, downloads, shared source/document edits or submissions occurred. The current candidate assessments are unchanged.
