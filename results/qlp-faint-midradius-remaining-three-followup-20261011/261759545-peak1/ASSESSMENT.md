# TIC 261759545: likely cataloged-binary contamination and period alias

Training sectors [99, 100, 101]. Native refinement: period 1.399025292 days, duration 0.048000 days, depth 4091 ± 298 ppm (formal selected-fit error), 21 supported events. Original flags: alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Three similarly spaced dips per selected cycle suggest a period alias; detrending-sensitive, source unresolved. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 11: timing_prediction_inconclusive, timing spread 0.4288 days. Sector 37: timing_prediction_inconclusive, timing spread 0.3093 days.

Training off-phase scan's selected maximum has formal SNR 11.89; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Initial source and catalog checks are below; full quality and unique-source validation remains incomplete. No secure host, novelty, or credible planet claim; retain for further review.

The fixed-phase-thirds check at the selected native period gives: phase 0.000: 4409±327 ppm, 21 supported events; phase 0.333: 3871±340 ppm, 16 supported events; phase 0.667: 3806±335 ppm, 16 supported events. One third of the selected period is 0.466341764 days. This supports a period-alias concern; it is post-selection evidence, not independent validation, a unique fundamental period, or three planets.


## Source-image diagnostics

The frozen-ephemeris raw difference images contain 14/19/19 events in sectors 99/100/101. All three small-cutout plots were inspected. Sectors 99/100 show a compact near-target but offset feature over a positive background. Sector 101 has a near-target feature plus strong structure around bright neighbors over a field-wide positive offset. Raw diagnostic moments are 0.706/0.818/1.081 pixels from the target; these are not calibrated PRF confidence or a unique host measurement. All three exact processed TESS-SPOC target-pixel requests returned HTTP 404; failures and URLs are retained rather than treated as nondetections.

Wider 31×31-pixel cutouts were examined with the unchanged spatial-plane helper. All six wide difference/background plots were inspected. The field is too crowded for either registered mask: every 2-pixel mask leaves only one background pixel and every 3-pixel mask leaves zero. All six fits therefore fail. No background-corrected image or stable localization follows; no mask was relaxed. The wide sector 100 global maximum is a stronger remote feature and cannot be used as the target localization. See source_review.json and background_review.json.

## Close binary and the other two dip phases

The catalog check included all 39 TIC entries within 42 arcseconds, independently of raw centroids. Gaia returned 41 mapping rows and 39 unique DR3 sources; two distant ambiguous crosslinks are retained. TIC **261759559**, 19.38 arcseconds from the target and Tmag 17.4705, maps to Gaia DR3 **6074099018099500928** and has an eclipsing-binary period **0.932762221 days**. Half that period, **0.466381111 days**, differs from one third of the selected QLP period by only **+3.40 seconds**. The comparison uses the already-measured three dips per selected cycle; it is not a calibrated chance-match probability or independent ephemeris fit.

The extra dip phases were imaged in the first discovery sector (99) at fixed offsets of exactly one third and two thirds of the frozen period, retaining the original period and duration. Both plots were inspected: compact positive features recur in the same near-target neighboring group as phase zero. Each includes 14 image events. Target offsets are 1.046/0.953 pixels, with TIC 261759559 nearest at 0.186/0.267 pixels. At phase zero in sector 99, TIC 261759559 is 0.253 pixels from the diagnostic moment, but faint TIC 990477584 is slightly closer (0.206 pixels). The binary is nearest in sector 100 at 0.115 pixels; sector 101 remains especially affected by background and bright-source structure. Faint companions are not resolved.

Together, the repeated offset structure and close binary-period relationship support **likely contamination by a known neighboring eclipsing binary**, with a period alias rather than three planets. This does not uniquely attribute every photon, overcome the failed background fits, or establish calibrated joint host confidence. These post-selection images share the QLP photons. Reserved-sector timing remains inconclusive; no shorter-period independent recovery or new planet candidate is claimed.

[Catalog verification](../../gaia-261759545-neighbors-20261011/verification.json) and [fixed-third source verification](../../tesscut-261759545-s99-thirds-20261011/verification.json) retain source hashes and limitations.
