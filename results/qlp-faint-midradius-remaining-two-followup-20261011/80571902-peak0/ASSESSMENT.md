# TIC 80571902: unresolved signal with competing features

Training sectors [71, 72]. Native refinement: period 10.950770879 days, duration 0.110400 days, depth 5293 ± 602 ppm (formal selected-fit error), 3 supported events. Original flags: alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Central depression amid substantial scatter and gaps; additional off-phase structure. Alternative detrending prefers another period. Source checks pending. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 6: timing_prediction_inconclusive, timing spread 1.2511 days. Sector 33: timing_prediction_inconclusive, timing spread 0.7584 days.

Inconclusive timing neither confirms nor reliably rejects recurrence. Further source and quality checks remain incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.378804, depth 6369 ± 821 ppm, formal SNR 7.76, 3 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.


## Initial source checks

Both raw sector difference plots and all four individual-event panels were visually inspected. Sector 72's two events (3 and 4) show a compact positive difference displaced from the target: the stacked moment lies 1.044 pixels from the target and 0.133 pixels from TIC 80571910 (T=15.2306), with fainter TIC 715946563 also nearby. Sector 71 event 0 shows a similar displaced feature in the neighboring group. These are the three photometrically supported events. Sector 71 image event 1 is instead dominated by a field-wide negative background; the stacked sector-71 moment near the edge cannot identify a source. Individual arrays were inspected without background correction or a new significance test.

This favors neighboring-source contamination of the 10.950771-day signal; the exact variable and physical cause remain unresolved. Moments are not calibrated PRF confidence, and catalog positions were not proper-motion propagated. Both attempted processed SPOC target-pixel products returned HTTP404; these exact-product failures are not nondetections or proof that every alternative product is absent.

The competing 17.762186-day fit shares a dip near BTJD3282.65 with the original fit (centers differ by about493seconds). Its other event has now received a separate source check and also shows a displaced feature near the same neighboring group; see the linked update below. These fits are not independent evidence for two planets, and source attribution for one fit does not automatically resolve the other.

[Source verification](source_review.json) and [individual-event plot](../../tesscut-80571902-s72-20261011/individual-events.png) preserve evidence. [Gaia query](../../gaia-80571902-neighbors-20261011/results.json) maps the target and two sources within one pixel of the sector72 moment to three DR3 sources; no variability-classifier or eclipsing-binary records were returned. This does not exclude an uncataloged variable or prove novelty. Gaia provenance verified. Reserved timing remains inconclusive. No secure new planet candidate.


Update: [separate coverage-fit source check](../../qlp-faint-midradius-remaining-two-coverage-followup-20261011/80571902-peak1/ASSESSMENT.md) finds displaced structure in both of its events. Likely neighboring-source contamination now applies to both fits, with exact host and true period unresolved.
