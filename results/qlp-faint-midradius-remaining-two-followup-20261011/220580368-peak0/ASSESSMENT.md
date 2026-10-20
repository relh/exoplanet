# TIC 220580368: likely neighboring-source contamination

Training sectors [71, 72]. Native refinement: period 4.446673590 days, duration 0.181440 days, depth 10961 ± 480 ppm (formal selected-fit error), 7 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Broad central depression with pronounced bright shoulders on either side. Variability, blending or processing remain concerns. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 7: timing_prediction_inconclusive, timing spread 2.3053 days. Sector 34: timing_prediction_inconclusive, timing spread 1.3559 days.

The training-only off-phase scan selects phase 0.378788, depth 2884 ± 758 ppm, formal SNR 3.80. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. The source checks below supersede the initial pending status; full quality and host validation remains incomplete. No secure host, novelty or credible planet claim.

## Source check

Raw sector-71 and sector-72 difference images include six and five events at the frozen ephemeris. Both plots were visually inspected and show a compact positive feature near the same neighboring group, displaced 3.960 and 3.724 pixels from the target. TIC 220580389 is closest to the moments, at 0.108 and 0.287 pixels; TIC 220580386 and fainter companions remain unresolved. Sector72 is near the cutout edge, limiting precise localization. The repeated large displacement supports likely contamination, without uniquely identifying a host. Raw images share photons with QLP, lack full background modeling, and moments/formal pixel significance are not calibrated PRF confidence.

Both exact processed TESS-SPOC pixel requests returned HTTP404; failures and URLs are retained, not treated as nondetections. Source hashes and checks are in `verify_pixels.py` and `source_review.json`.

Gaia DR2-to-DR3 lookup maps the four selected TIC sources to four DR3 sources. TIC 220580389 maps to DR3 3148810300463465344, classified ECL and listed in the eclipsing-binary table with period 19.974279385 days. This differs from the QLP 4.446673590-day signal; the label is not a matching-period identification of its source. A blended variable, a catalog-period issue, or another source in the group remains possible. The image evidence supports contamination, but the exact variable and period remain unresolved. Catalog provenance: `../../gaia-220580368-neighbors-20261011/`.
