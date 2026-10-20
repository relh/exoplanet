# TIC 307925590: background/source-systematics concern

Training sectors [62, 63, 64, 65] select seed period5.19287878days. Native refinement gives 5.19277419days, duration0.059520days, depth2581±271ppm (formal selected fit error), with 11 individually supported events. Original flags retained: alternative_detrending_prefers_other_period, crowding_or_missing_crowding. Screening or diagnostic admission is not planet validation.

The inspected folded depression is shallow and scattered. Alternative detrending prefers another period. An off-phase feature near phase0.50072 has selected SNR4.07, which is not a calibrated binary diagnosis.

Sector5: timing_prediction_inconclusive, spread0.2849days; Sector9: timing_prediction_inconclusive, spread0.2677days. Inconclusive timing neither confirms nor reliably rejects the ephemeris. Initial source and catalog checks are below; full quality and unique-host validation remains incomplete. No host or novelty established; no credible new planet claim or external submission.


## Raw source diagnostics

The frozen-ephemeris raw difference images contain 5/6/5/5 image events in sectors 62/63/64/65. All four small-cutout plots were inspected. Sector 62 is entirely negative across the field. Sector 63 shows positive/negative structure around bright TIC 307925559; sector 64 shows an offset positive group near the same neighbor; sector 65 combines positive background with positive/negative structure around that bright neighbor. The neighbor is Tmag 10.9237, 52.58 arcseconds from the target. No repeatable isolated target source is established, and moments of these background/dipole maps are not reliable host confidence.

All four exact processed TESS-SPOC pixel requests returned HTTP 404. These errors and URLs are retained rather than converted into nondetections. See source_review.json for raw file, fit and plot hashes.

## Catalog check

The Gaia lookup included all 54 TIC entries within 84 arcseconds of the target, covering the bright neighbor and surrounding group independently of invalid raw centroids. All map to 54 DR3 sources. TIC 806088902 maps to Gaia DR3 5272772779107327616 and is a cataloged eclipsing binary with period **3.192603187 days**, DIFFERENT from the selected QLP period **5.192774190 days**. This is not a matching-period identification or an established alias relationship. No label for another source excludes uncataloged variability or proves novelty. [Catalog provenance](../../gaia-307925590-neighbors-20261011/verification.json).

The observed structure raises background and source-dependent instrumental concerns; it does not identify a physical cause or exclude astrophysical variability. These raw images share QLP photons, use local temporal subtraction, and do not calibrate PRF confidence. Reserved timing remains inconclusive and the alternative-detrending flag remains. No new planet candidate is claimed.


## Wider-background checks

All four 31×31-pixel cutouts were inspected using the unchanged weighted spatial-plane helper and both predeclared source masks. The original sector 62 analysis failed in the centroid helper with “No positive difference flux”; that traceback, script and status are preserved. A separate diagnostic reused the same event extraction without computing a source centroid, allowing raw images and background fits to be inspected. Its catalog distances are to the target coordinate, not to an inferred source. No event gate was relaxed.

All eight wide raw/background plots were inspected. Background-pixel counts for 2/3-pixel masks are 87/15 (sector 62), 47/1 (63), 75/6 (64), and 103/17 (65). Six plane fits completed; the 3-pixel masks in sectors 63/64 failed for insufficient pixels and were retained without relaxation.

The corrected images retain mixed positive/negative structure around bright TIC 307925559, particularly in sectors 62/63/65, while sector 64 retains a positive offset group. Stronger remote and edge residuals elsewhere in the wide field cannot be used as target localizations. Plane subtraction therefore does not establish a clean, repeatable isolated signal on the target or a uniquely identified contaminant. This strengthens background/source-systematics concerns, without proving a particular instrumental or astrophysical cause. See background_review.json for verified inputs, mask outcomes and the preserved centroid failure.
