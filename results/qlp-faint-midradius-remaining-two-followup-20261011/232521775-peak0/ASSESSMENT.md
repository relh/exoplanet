# TIC 232521775, peak 0: unresolved signal

Training sectors [74, 75]. Native refinement: period 14.331655640 days, duration 0.181440 days, depth 1818 ± 216 ppm (formal selected-fit error), 2 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Shallow central depression with nearby structure and noisy binned points. Native refinement has only two supported events despite the original screen qualifying for follow-up. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 14: timing_prediction_inconclusive, timing spread 3.0754 days. Sector 15: timing_prediction_inconclusive, timing spread 3.0230 days.

The training-only off-phase scan selects phase 0.817896, depth 1080 ± 226 ppm, formal SNR 4.78. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. Further source and catalog checks remain incomplete. No secure host, novelty or credible planet claim.


## Initial source and coverage checks

Sector74 raw and processed SPOC difference plots were visually inspected (two accepted events each). The raw difference is dominated by field-wide positive background with target-region structure; its formal maximum and 2.292pixel moment offset cannot identify a host. The processed difference has mixed positive and negative target-region structure, including a negative feature adjacent to the positive feature. It does not provide a clean isolated source or reliable host attribution. The reductions share photons; this is not independent-epoch validation. No Gaia inference was made from these unreliable moments.

Both sector75 image analyses fail the unchanged requirement for at least two accepted events. An exposure audit explains this: event2 has78quality-zero in-event and218baseline exposures in both products; event3 has only3in-event exposures and none are quality zero (raw flags32×2,168×1; processed32×2,160×1), with314quality-zero baseline exposures. This missing accepted coverage is not a nondetection. Sector74 processed events0/1 have78/79quality-zero in-event and156/193baseline exposures. No quality or event gates were relaxed; original failures retained.

[Source verification](source_review.json), [raw sector75 coverage](../../tesscut-232521775-s75-20261011/coverage.json), [processed sector75 coverage](../../spoc-pixels-232521775-s75-20261011/coverage.json). Classification: unresolved signal with background/source-systematics concerns, not a demonstrated physical false positive or a credible new planet candidate. Reserved timing remains inconclusive, and only two native training events satisfy the original support threshold.
