# TIC 373414832: unresolved screening signal

Native refinement: P=14.428025926 days, duration=0.216000 days, box depth=0.00189997 ± 0.00016157 (formal). Training sectors [98]; 4 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Shallow central depression with nearly half the phase coverage absent and broad irregular structure in the zoom. Four supported native events do not repair missing secondary coverage or alternate-detrending ambiguity.

Reserved-sector timing tests: sector 5: timing_prediction_inconclusive, timing spread 6.575234 days; sector 71: timing_prediction_inconclusive, timing spread 2.049830 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 2.9042541713088026. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Initial source check

Sector98 raw TESScut images were evaluated with the unchanged frozen clock and duration, original quality-zero selection, and existing event gates. The stack and all four event maps (0–3) were inspected. Every event has strong positive/negative lobes near the much brighter neighbor TIC373414837 (Tmag9.50018), roughly three pixels from the target. Event0 is positive below and negative above the bright neighbor; events1–3 reverse the dominant direction. These patterns favor contamination/instrumental residuals over an isolated target-host transit. Motion is a plausible explanation, not a proven cause, and the maps do not establish a clean eclipse in the neighbor either. Small target-region residuals do not establish an embedded target signal.

The stack's positive moment lies2.9204 pixels from the target,1.1514 pixels from bright TIC373414837 and0.5594 pixels from faint TIC373414833 (Tmag19.0289). The signed lobes and unresolved scene prevent interpreting the nearest catalog entry as the host. Formal maximum pixel SNR301.96 is not a calibrated astrophysical significance or source probability.

The four windows contain8/84/57/93 quality-zero inside exposures and372/336/348/305 baseline exposures. Event0 is especially sparsely sampled. Event1 excludes two quality32 exposures; event2 excludes two quality32 and one quality40 exposure. No gate was relaxed. Raw pixel images and QLP use the same photons and do not independently validate the signal. Reserved-sector5/71 timing predictions remain inconclusive.

The TIC cone returned70 entries. Gaia lookup of all11 entries within3 pixels of the raw moment found identifiers for all11,11 DR2-to-DR3 mappings and11 sources. One classifier row is for the target itself, Gaia3293091617872694144, SOLAR_LIKE score0.72996396. There are no eclipsing-binary rows. That label is not a probability that target variability caused the TESS feature; catalog nonmatches do not exclude unlisted variability, and no epoch-photometry match was tested.

The exact requested processed sector98 target-pixel product returned HTTP404. Request, stderr and child exit status are retained. This neither proves all products absent nor represents a nondetection. Source verification passed raw ZIP/FITS byte equality/hashes, frozen/neighbor inputs, map count/shape, independently counted event gates, plot hashes and raw Gaia download hashes. Existing science algorithms were reused; no new full-suite test claim.

[Stack](../../tesscut-373414832-s98-20261011/difference.png) · [All four maps](../../tesscut-373414832-s98-20261011/events-1.png) · [Coverage](../../tesscut-373414832-s98-20261011/coverage.json) · [Gaia lookup](../../gaia-373414832-scene-20261011/results.json) · [Verification](source_review.json).

Disposition: weakened as a target-host planet. Initial source inspection is complete; exact physical cause remains unresolved. No likely new planet claimed.
