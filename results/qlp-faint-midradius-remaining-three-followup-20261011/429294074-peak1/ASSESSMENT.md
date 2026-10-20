# TIC 429294074: likely cataloged-binary contamination and period alias

Training sectors [99, 100, 101] select seed period1.48485461days. Native refinement gives 1.48492910days, duration0.048000days, depth2518±171ppm (formal selected fit error), with 26 individually supported events. Original flags retained: alternative_detrending_prefers_other_period, crowding_or_missing_crowding. Screening or diagnostic admission is not planet validation.

Three similarly deep dips per selected cycle. The fixed-third check measures depths 2748±188, 2504±193 and 2594±196 ppm, with 26/20/19 supported events. A period of one third (0.49497637 days) lies just below the original 0.5-day search bound. This is post-selection evidence for an alias, not a uniquely established fundamental period or three planets.

Sector10: timing_prediction_inconclusive, spread0.5659days; Sector11: timing_prediction_inconclusive, spread0.5597days. Inconclusive timing neither confirms nor reliably rejects the ephemeris. Initial source and catalog checks are below; full quality and unique-source validation remains incomplete. No host or novelty established; no credible new planet claim or external submission.


## Source images and background limits

The frozen-ephemeris raw images include 13/18/17 events in sectors 99/100/101. All three small-cutout plots were inspected: sector 99 has a compact off-target positive feature; sector 100 is negative across the field with a relative target-region enhancement; sector 101 has a field-wide positive background and target/neighbor structure. Raw moments across these backgrounds are not reliable host confidence. All three exact processed TESS-SPOC target-pixel requests returned HTTP 404, retained as missing products rather than nondetections.

Wider 31×31-pixel images were checked with the unchanged spatial-plane helper. All six wide difference/background plots were inspected. The 2-pixel source masks leave only 15/20/11 background pixels; every 3-pixel mask leaves zero and fails. The sparse fits retain structure near the target and other stars. Both mask outcomes are preserved without relaxing the masks. These are not robust background-independent localizations; wide-field maxima are not target localizations. See source_review.json and background_review.json.

## Cataloged binary and fixed-third check

All 31 TIC entries within 42 arcseconds of the target were checked, independently of the invalid raw centroids. Gaia returned 33 DR2-to-DR3 mapping rows covering 31 unique DR3 sources, retaining two distant ambiguous crosslinks. The first verifier incorrectly expected 31 mapping rows; that failure and script are retained, and the corrected verifier checks all 33 rows.

TIC **429294064**, 27.84 arcseconds from the target and Tmag 17.5403, maps to Gaia DR3 **6125563343462988160** and has an eclipsing-binary period **0.989860779 days**. Its half-period is **0.494930389 days**, approximately **3.97 seconds shorter** than one third of the native QLP period (0.494976368 days). This comparison is motivated by the previously measured three dips per selected cycle. It is not a calibrated chance-match probability or an independent ephemeris fit.

The two already-measured extra dip phases were imaged in sector 99 with the period/duration fixed and epoch offsets of exactly one third and two thirds of the frozen period. Both additional plots were inspected: they show compact positive features in the same off-target region as phase zero. There are 13/14 image events, target offsets 1.621/1.564 pixels, and distances to TIC 429294064 of 0.241/0.180 pixels. Phase zero contains 13 image events, offset 1.695 pixels, with TIC 429294064 the nearest entry at 0.329 pixels. Faint neighboring entries remain unresolved. See ../../tesscut-429294074-s99-thirds-20261011/verification.json and ../../gaia-429294074-neighbors-20261011/verification.json.

The consistent three-phase offset in sector 99 plus the close catalog-period relationship supports **likely contamination by a known neighboring eclipsing binary**, with a selected period alias rather than three planets. It does not uniquely attribute every photon, establish calibrated joint confidence, or resolve the background problems in the other two sectors. The shorter-period source has not been independently refit or recovered in the reserved sectors; their inconclusive timing remains retained. No new planet candidate is claimed.
