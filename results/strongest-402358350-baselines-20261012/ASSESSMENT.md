# TIC 402358350: the localized dip survives raw-flux baseline tests

**All eight usable events remain positive in both SAP and PDCSAP across the entire frozen baseline matrix, without running-median flattening.** Combined depths are 590–659 ppm. This strengthens the interpretation of a recurring, localized dimming feature rather than a feature manufactured by our median detrending. It does not establish the host, distinguish a planet from a blended eclipse, or repair the previously failed timing-precision gate.

This is a new method check on already-opened sectors 40/41/54/81, not another independent observing epoch. Previous physical fits and sinusoidal nuisance tests used median-flattened products; the present experiment works directly from the archived SAP/PDCSAP series. These streams still share exposures, and PDCSAP retains its upstream pipeline corrections.

## Frozen choices and coverage

The [plan](plan.json) records the immutable expanded pre-sector81 clock, with duration D=0.144day, input FITS hashes and the full method matrix before calculation. The period, epoch and duration were not retuned. For each event, constant, linear and quadratic polynomials are fitted only outside±D and inside either±3D or±5D. At least10 points on each side and3 inside the fixed half-duration are required. No data-dependent outlier rejection or running median is used.

Both streams use the same quality-zero finite positive input mask, normalized by their own sector median. Supplied errors receive a robust adjacent-difference floor derived only from baseline points. Depth errors include uncertainty from extrapolating the fitted baseline into the dip; a second error multiplies by the baseline residual-scatter factor when that factor exceeds one. Results below use these scatter-scaled errors. Correlated noise is not fully modeled.

Nine nominal event centers fall inside the overall sector spans. Sector 40 event 1 lies in a gap and fails coverage for all twelve methods. It remains recorded, rather than silently omitted. The other eight events provide 96 successful event measurements across both streams and six baselines.

## Every baseline retains the dimming

| Baseline degree | Outer radius | SAP depth, ppm | PDCSAP depth, ppm |
|---|---|---:|---:|
|Constant|3 D|627 ±44|609 ±42|
|Constant|5 D|602 ±41|591 ±40|
|Linear|3 D|642 ±41|610 ±42|
|Linear|5 D|614 ±39|590 ±39|
|Quadratic|3 D|659 ±53|647 ±54|
|Quadratic|5 D|633 ±43|621 ±43|

Every individual usable event is positive under every method. Leaving out each event in turn gives combined depths 569–706 ppm across the full matrix, so no single event creates the recurrence. SAP event depths vary more than PDCSAP: heterogeneity chi-square is 11.7–15.8 versus 2.2–5.1 for seven degrees of freedom under the stated error model. These descriptive comparisons do not prove perfectly stable eclipse depths or calibrate planet likelihood.

The [event-shape figure](event-shapes.png) shows all eight events using linear±3D baselines as an illustration, not a retrospectively selected winner. The complete matrix is retained in [results.json](results.json) and [summary.json](summary.json).

## Localization in time, duration sensitivity and controls

All six fixed averaging widths, from0.5D to2D, are retained for every event and method. Combined depths are nearly flat between0.5D andD, then decline as the averaging window includes the shoulders. The average depressions in the protected adjacent intervals, −D to−D/2 and+D/2 to+D, are much smaller: SAP5–125ppm and PDCSAP35–161ppm across methods. For example, the linear3D PDC fit gives610 ±42ppm in the central window, versus72 ±56 and125 ±56ppm on the two sides. This supports localization on a few-hour timescale. It is not a fitted transit-duration posterior, and weaker wings remain possible. [Full width matrix](width-matrix.png).

Each event also has four predetermined offset controls at±0.25 P and±0.4 P. Controls must match the original in-window and both baseline-side counts within 20%. All insufficient or unmatched windows remain recorded. Each method has 15 matched event/control comparisons; these repeat many of the same observations across methods and are not independent trials. No matched PDC control is as deep as its corresponding event. One SAP control exceeds its event under five of six baselines; that unfavorable comparison is retained. Sector 54 event 34 has no matched controls, preventing a local empirical comparison for that event.

For each matched comparison, additive−600 ppm and+600 ppm boxes were injected into the selected normalized archived product at the control position and the complete local fit repeated. All 360 signed injections reproduce the added depth within numerical precision. This verifies that the masked linear baseline machinery preserves dimming and brightening symmetrically, including baseline-error propagation. Because injections lie inside the excluded baseline region, accurate recovery is expected; it is not a realistic transit false-alarm calibration. The test does not rerun SPOC/PDC, simulate detector contamination, or establish how a nearby source enters the aperture.

## Verification and limits

[verify.py](verify.py) passed13,615 checks covering all756 successful event, control and injected fits. It reconstructs masks and normalized/injected arrays from hashed raw FITS files, independently solves baseline coefficients/covariance by QR, reproduces the noise floors, depth/annular/width estimates and propagated uncertainties, verifies all coverage/matching decisions, and checks signed injection transfer. The raw FITS reader and NumPy remain shared infrastructure. [Verification record](verification.json).

Both figures were inspected. Numerical arrays and all unsuccessful coverage records are retained. No new data were opened, no shared scientific code changed, and no current candidate clock was replaced. The remaining obstacle is source attribution: a robust localized feature can still be an off-target stellar eclipse or another contaminant. This result addresses a specific detrending concern and should not be reported as planet confirmation.
