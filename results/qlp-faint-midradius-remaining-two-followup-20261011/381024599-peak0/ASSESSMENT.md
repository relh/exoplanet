# TIC 381024599: likely neighboring-source contamination

Training sectors [70, 71]. Native refinement: period 5.398956122 days, duration 0.073600 days, depth 9618 ± 650 ppm (formal selected-fit error), 5 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: A visible central depression with sloping sides and substantial scatter. Five supported training events; the source checks below supersede the initial pending status. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 4: timing_prediction_inconclusive, timing spread 1.1431 days. Sector 31: timing_prediction_inconclusive, timing spread 0.6866 days.

Inconclusive timing neither confirms nor reliably rejects recurrence. Initial pixel-source and catalog checks are below; full quality and host validation remains incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.485106, depth 3084 ± 666 ppm, formal SNR 4.63, 3 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.


## Pixel-source and background checks

The frozen-ephemeris raw difference images contain five events in each of sectors 70 and 71. Both small-cutout plots were visually inspected: sector 70 has a compact positive feature away from the target near TIC 381024603; sector 71 has a similar feature superposed on a strong positive field-wide background. Small-map moments alone are insufficient attribution evidence. Both exact processed TESS-SPOC target-pixel requests returned HTTP 404; retained failures are not nondetections.

Wider 31×31-pixel cutouts were checked with the unchanged weighted spatial-plane helper, excluding catalog sources brighter than Tmag 17 and the target with both 2- and 3-pixel masks. Both masks fit in both sectors (background pixels 638/353 in sector 70 and 642/368 in sector 71). All four wide difference/background plots and the corrected local four-panel view were inspected. The compact offset feature persists under both corrections, with diagnostic moments 2.758/2.759 pixels off target in sector 70 and 2.588/2.588 in sector 71. TIC 381024603 is the nearest catalog entry at 0.017/0.017 and 0.424/0.423 pixels. TIC 381024600 and fainter sources remain possible blended contributors. Sector 71 also retains structure near the target and bright TIC 381024607, so simple background removal does not eliminate all source-dependent instrumental effects.

This supports likely contamination near TIC 381024603, without uniquely identifying the variable. These are the same photons as QLP, not independent epochs; moments and formal errors are not calibrated PRF confidence. Positions are not proper-motion propagated. See source_review.json and background_review.json for input hashes and verification.

## Catalog check

The target and neighbors TIC 381024600/381024603 map to three Gaia DR3 sources. The target (19447783715197952) has a SOLAR_LIKE classifier label; TIC 381024603 (19447818074802816) has an RS label with reported score 0.08453491. These automated labels and scores do not confirm a source or period and are not posterior probabilities. No eclipsing-binary rows were returned, which does not exclude an uncataloged binary or establish novelty. [Catalog provenance](../../gaia-381024599-neighbors-20261011/verification.json).

No secure host or credible new planet candidate follows from this diagnostic.
