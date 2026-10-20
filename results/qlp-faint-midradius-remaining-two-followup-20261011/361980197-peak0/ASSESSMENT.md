# TIC 361980197: likely neighboring-source contamination

Training sectors [46, 47]. Native refinement: period 17.352626636 days, duration 0.133056 days, depth 44305 ± 418 ppm (formal selected-fit error), 3 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Deep primary and a second prominent off-phase dip. Eclipsing-system or contamination suspect; neither the variable nor its host is established. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 20: timing_prediction_inconclusive, timing spread 0.2245 days. Sector 60: timing_prediction_inconclusive, timing spread 0.1298 days.

Training off-phase scan's selected maximum has formal SNR 60.04; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. The source and catalog checks below supersede the initial pending status; a full quality and host validation is incomplete. No secure host, novelty, or credible planet claim; retain for further review.

The selected off-phase dip occurs at phase 0.801331, with depth 28248±471 ppm and two supported events, compared with native primary depth 44305±418 ppm. This strengthens the eclipsing-system/contamination concern, without confirming a binary or its host. The scan significance remains selected and uncalibrated.

## Source check

At the frozen native ephemeris, raw sector-46 and sector-47 difference images each include two events. All three available difference plots were visually inspected. A compact positive feature appears on a neighboring blend, with moments 3.746 and 3.636 pixels from the target. The nearest entries include TIC 361980195 / 740774088 (identical catalog position and Gaia identifier), 740774089, and the fainter 361980198. Nearest-entry distances change between sectors; these data cannot select an individual component.

The sector-47 processed TESS-SPOC pixels give a similar feature 3.776 pixels from the target, near the same blend. The raw sector-47 peak is at the cutout boundary and the processed peak is also near an edge, limiting precise localization. The large displacement in both sectors supports likely contamination despite those limitations. Moments and formal pixel significance are not calibrated PRF confidence. QLP, raw FFIs, and processed pixels share photons within a sector. The exact sector-46 processed-product request returned HTTP 404, retained in its run directory; this is not a nondetection.

A Gaia DR2-to-DR3 lookup of the target and every neighbor within one pixel of either raw moment maps five TIC entries to four unique sources. The target has a SOLAR_LIKE classifier entry; there are no eclipsing-binary table rows for the mapped group. This does not exclude an uncataloged binary or identify the contaminating variable. The deep primary plus off-phase dip remain suggestive of an eclipsing system, without binary confirmation. No credible planet candidate or novelty claim.

Reproducible source hashes and checks: `verify_pixels.py` / `source_review.json`; catalog query and verification: `../../gaia-361980197-neighbors-20261011/`.
