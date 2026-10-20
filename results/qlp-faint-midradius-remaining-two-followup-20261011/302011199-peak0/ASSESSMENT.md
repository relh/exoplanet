# TIC 302011199, peak 0: unresolved signal

Training sectors [17, 18]. Native refinement: period 0.804754609 days, duration 0.092736 days, depth 1883 ± 218 ppm (formal selected-fit error), 9 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Central depression visible in sparse, noisy data with broad baseline structure. The duration occupies a substantial fraction of the short period. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 58: timing_prediction_inconclusive, timing spread 0.7662 days. Sector 85: timing_prediction_inconclusive, timing spread 1.2431 days.

The training-only off-phase scan selects phase 0.457143, depth 576 ± 334 ppm, formal SNR 1.72. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. Initial source and background diagnostics are below; full quality and host validation remains incomplete. No secure host, novelty or credible planet claim.


## Source and background diagnostics

Raw sector 17/18 difference images include 23/27 events at the frozen ephemeris. Both small-cutout plots were inspected: field-wide positive offsets with target and bright-neighbor enhancements. Raw small-map moments of 0.515/0.242 pixels from the target are not calibrated host confidence. Both exact processed TESS-SPOC pixel requests returned HTTP 404; errors and URLs are retained, not interpreted as nondetections.

Wider 31×31-pixel cutouts were examined with the unchanged weighted spatial-plane helper. Both source-exclusion masks were retained: 2/3-pixel masks fit 380/98 background pixels in sector 17 and 376/110 in sector 18. All four wide difference/background plots were inspected. The brightest residuals are around remote bright TIC 302011203, with positive/negative structure and additional features near other stars. These global maxima are not valid target localizations or a unique contaminant identification.

A small feature near the target persists after both corrections. The corrected local four-panel view was inspected using the catalog target position as the fixed moment anchor, rather than choosing the remote wide-field peak. Diagnostic target offsets are 0.514/0.528 pixels in sector 17 and 0.214/0.221 in sector 18. TIC 621500528 is closest in sector 17 (0.271/0.275 pixels), while the target is closest in sector 18 and TIC 621500528 remains only 0.246/0.237 pixels away. TIC 621500525 is another nearby unresolved source. This does not distinguish target variability, blended variability, or source-dependent instrumental effects.

The simple background model does not remove source-dependent effects. These images share the QLP photons; they are not independent observations. Moments and formal pixel errors are not calibrated PRF confidence, and catalog positions are not proper-motion propagated. See source_review.json and background_review.json for input hashes and verification. The source, recurrence, and planetary origin remain unresolved.


## Gaia neighboring-source check

The target and faint neighbors TIC 621500528/621500525 map to three Gaia DR3 sources. TIC 621500528 maps to DR3 342378991653611520 and is cataloged as an eclipsing binary with period **0.941217995 days**. That is **different from the QLP period 0.804754609 days**: the lookup does not identify a matching-period contaminant or prove an alias relationship. The close cataloged binary adds a contamination concern, while the image residuals and exact origin of the selected QLP signal remain unresolved. Catalog labels and classifier scores are not calibrated joint host confidence; no label on another source excludes variability. [Catalog provenance](../../gaia-302011199-neighbors-20261011/verification.json).
