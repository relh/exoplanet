# TIC 354475391: unresolved screening signal

Native refinement: P=6.177497042 days, duration=0.216000 days, box depth=0.02088841 ± 0.00149201 (formal). Training sectors [85]; 2 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Broad irregular gap-adjacent depression with large positive and negative excursions in the time series. Two supported events; not an isolated stable transit. The other seed refines to essentially the same period and depth, not an independent candidate.

Reserved-sector timing tests: sector 18: timing_prediction_inconclusive, timing spread 20.381910 days; sector 58: timing_prediction_inconclusive, timing spread 8.256342 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 4.140781233102946. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Initial source check

The unchanged frozen fit was applied to sector 85 raw TESScut pixels with the existing quality-zero and event-coverage gates. The stack and all four usable event maps (−1, 0, 1, 3) were inspected for each fit. Strong changing positive/negative features occur around the brighter neighboring blend near TIC354475402/354475393, approximately three pixels from the target. Event −1 has a large negative field offset and positive-above/negative-below structure at that blend; events 0 and 1 reverse the dominant orientation, and event 3 again has positive-above/right and negative-below/left structure. These are not consistent isolated target-host dimmings. Instrumental/motion residuals and neighbor contamination remain plausible; the exact cause is not proven.

The stack moment is about3.16 pixels from the target and near TIC354475393, but the mixed-sign blend prevents a unique stellar assignment. Formal maximum pixel SNRs37.28/35.54 for the two fits are not calibrated host probabilities or discovery significance. Gaia DR2-to-DR3 lookups for all21 TIC neighbors within3 pixels of the first fit's moment returned21 mappings and21 sources, with no classifier or eclipsing-binary rows. All selected entries had Gaia identifiers. These nonmatches do not exclude variability or prove novelty; no epoch-photometry confirmation was performed.

Usable inside counts are69–93 for peak0 and69–94 for peak1; quality-zero baselines186–349. Event1 excludes two quality32 and one quality168 exposures. Event2 has79 inside exposures, all quality2048, so is excluded. Four pixel-image windows do not mean four independently supported QLP transits. The two fits share348 quality-zero inside exposures out of348/349 total: they are almost the same selection and do not independently validate a planet. The overlap audit is retained with the second fit's pixel artifacts.

The exact requested processed sector85 target-pixel product returned HTTP404; request and child failure are preserved. This is not a nondetection or proof that all products are absent. Both source verifiers passed ZIP/FITS byte equality and hashes, frozen-fit and neighbor identity, map shapes/counts, independently counted coverage gates, plot hashes and Gaia raw-download hashes. Existing science algorithms were reused; no new full-suite test claim.

[Stack](../../tesscut-354475391-s85-20261011/difference.png) · [All four event maps](../../tesscut-354475391-s85-20261011/events-1.png) · [Coverage](../../tesscut-354475391-s85-20261011/coverage.json) · [Exposure overlap](../../tesscut-354475391-peak1-s85-20261011/window-overlap.json) · [Gaia results](../../gaia-354475391-scene-20261011/results.json) · [Verification](source_review.json).

Disposition: weakened as a target-host planet; mixed-sign neighbor-region residuals dominate. Initial source inspection is complete, physical classification remains unresolved. The original sector18/58 timing predictions remain inconclusive. No likely new planet claimed.
