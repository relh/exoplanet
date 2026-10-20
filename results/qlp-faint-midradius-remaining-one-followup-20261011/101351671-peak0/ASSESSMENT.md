# TIC 101351671: unresolved screening signal

Native refinement: P=6.457586415 days, duration=0.216000 days, box depth=0.00258476 ± 0.00026578 (formal). Training sectors [85]; 3 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Broad asymmetric depression with a sharper leading edge and positive structure before it. Large time-series gap and alternate-detrending ambiguity remain; no source attribution or reliable independent recurrence.

Reserved-sector timing tests: sector 18: timing_prediction_inconclusive, timing spread 6.899824 days; sector 58: timing_prediction_inconclusive, timing spread 2.853622 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 3.0018792698502246. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Initial source check: weakened by background and mixed residuals

The raw sector85 stack and all four individual event maps (−1,0,1,2) were inspected. Events−1 and1 have large positive field offsets, approximately200 and56 in the image flux units. Around the target, positive and negative residuals alternate spatially; event0 has a negative target pixel with offset positive features, and event2 has a stronger positive feature above the target with a negative lobe to its left/below. This does not establish a repeatable isolated dimming source. Motion/background-related residuals are plausible but not uniquely diagnosed.

The aggregate formal pixel SNR reaches834 and the algorithm reports a moment6.31pixels from the target. The stack is positive almost everywhere and its formal-SNR maximum falls in the background near the cutout edge. Neither number is meaningful evidence for a neighboring eclipsing source or a host probability. A Gaia lookup centered on that spurious moment would not answer the source question, so no such localization-based catalog query was run. The TIC neighborhood query returned109 rows; novelty and physical classification remain unestablished.

The four usable raw windows contain31–94 quality-zero inside exposures and187–326 outside exposures. Event0 also contains two quality32 and one quality40 inside exposures, excluded by the unchanged gate. Four image windows are not the three supported QLP events. The requested exact TESS-SPOC pixel product returned HTTP404, retained in the status/error evidence; this is not absence of all processed products or a photometric nondetection. Raw and QLP diagnostics share photons.

Disposition: the isolated target-host transit interpretation is weakened. No reliable source attribution or likely new planet is established. Original sector18/58 timing predictions remain inconclusive. [All event maps](../../tesscut-101351671-s85-20261011/events-1.png) · [Stack](../../tesscut-101351671-s85-20261011/difference.png) · [Coverage](../../tesscut-101351671-s85-20261011/coverage.json). Raw ZIP/FITS, frozen inputs, coverage gate, image hashes and processed404 provenance passed verification. Initial source checks are complete; catalog/physical vetting is not.
