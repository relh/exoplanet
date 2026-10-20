# TIC 15736353: likely neighboring-source contamination

Training sectors [70, 71]. Native refinement: period 7.235772431 days, duration 0.092736 days, depth 4890 ± 376 ppm (formal selected-fit error), 6 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Visible central depression amid substantial scatter, with an irregular bottom and nearby baseline structure. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 43: timing_prediction_inconclusive, timing spread 0.3344 days. Sector 44: timing_prediction_inconclusive, timing spread 0.3254 days.

The training-only off-phase scan selects phase 0.490476, depth 2384 ± 473 ppm, formal SNR 5.04. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. The source checks below supersede the initial pending status; full quality and host validation remains incomplete. No secure host, novelty or credible planet claim.

## Pixel-source check

Raw sector70 and sector71 difference images include two and four events at the frozen ephemeris. Both plots were visually inspected: a compact positive feature is displaced from the target toward the same faint neighboring group. Diagnostic target offsets are1.604 and1.784pixels. TIC15736352 (Tmag17.0072) is closest to the moments, at0.249 and0.075pixels; TIC15736348 and other fainter entries remain possible blended contributors. This supports likely contamination, not a unique host identification.

Both exact processed TESS-SPOC target-pixel requests returned HTTP404, retained with URLs and errors rather than treated as nondetections. The raw images share photons with QLP and use temporal subtraction without full background modeling. Moments and formal pixel errors are not calibrated PRF confidence; catalog positions are not proper-motion propagated. Source hashes, fit identity and retained failures pass verify_pixels.py / source_review.json. No credible planet candidate or novelty claim.

Gaia DR2-to-DR3 lookup mapped the target and neighbors TIC15736352/15736348 to three DR3 sources. No classifier or eclipsing-binary rows returned; this does not exclude an uncataloged variable or establish novelty. [Catalog provenance](../../gaia-15736353-neighbors-20261011/verification.json).
