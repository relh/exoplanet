# TIC 142396584, peak 0: unresolved signal

Training sectors [75, 76]. Native refinement: period 14.188273690 days, duration 0.216000 days, depth 2097 ± 224 ppm (formal selected-fit error), 4 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Broad shallow central depression amid substantial scatter; the full phase fold contains a large coverage gap. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 15: timing_prediction_inconclusive, timing spread 3.0664 days. Sector 21: timing_prediction_inconclusive, timing spread 2.7815 days.

The training-only off-phase scan selects phase 0.282092, depth 2048 ± 413 ppm, formal SNR 4.96. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. Catalog checks remain incomplete. No secure host, novelty or credible planet claim.


## Source and same-exposure checks

Raw difference images from sectors 75 and 76 (two events each) were visually inspected: both are dominated by field-wide background changes. Their flux moments cannot identify a host. Processed SPOC difference images were also inspected: sector 75 has a strong image-edge feature and mixed target region; sector 76 is weak and mixed, with its formal maximum near TIC 142396578. There is no repeatable isolated target source. Formal image significance is not calibrated source confidence. See [verified source evidence](source_review.json).

Exact native CADENCENO matching retains each pipeline's original timestamps (approximately 1.92–1.94 seconds apart). Sector 75 has 6,338 common processed exposures but no surviving in-event points. Sector 76 has 5,600 common exposures and one surviving event with 94 points: QLP depth 2734 ± 504 ppm, SPOC PDCSAP 2368 ± 527 ppm, SAP 2609 ± 509 ppm (formal fixed-box errors). This one dip survives different processing of the same photons; it is not independent-epoch validation.

The [preprocessing audit](../../spoc-quality-142396584-s75-20261011/preprocessing-audit.json) explains the other three unavailable comparisons. Before detrending, events 0 and 1 each have 58 finite positive quality-zero SPOC points, and event 2 has 93. All are removed by the unchanged 0.75-day gap-edge trimming. Event 3 retains all 94. Missing processed coverage is not a nondetection. Sector 75 also has nonzero-quality exposures in both windows (22/20 flagged 4096 and 14/15 flagged 32768); sector 76's two windows are entirely quality zero. No quality or detrending gates were relaxed.

[Sector 75 comparison](../../qlp-faint-142396584-cadence-s75-20261011/results.json), [sector 76 comparison](../../qlp-faint-142396584-cadence-s76-20261011/results.json), and [provenance verification](../../spoc-quality-142396584-s75-20261011/comparison-verification.json) retain scripts, identities and hashes. Assessment: unresolved signal with background/source-systematics concerns, not a secure planet candidate or a demonstrated physical false-positive mechanism. Reserved-sector timing remains inconclusive. Better source and background modeling is needed before host attribution.
