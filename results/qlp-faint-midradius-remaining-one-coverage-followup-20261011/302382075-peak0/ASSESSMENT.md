# TIC 302382075: unresolved screening signal

Native refinement: P=15.880479615 days, duration=0.032000 days, box depth=0.46683174 ± 0.06071512 (formal). Training sectors [97]; 2 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Enormous variable scatter reaches order-unity flux changes, including negative normalized residuals near minus one and positive excursions above one. The narrow selected box is not a credible isolated shallow transit. Secondary scan also selects a large nearby dip and brightening; physical interpretation is unreliable without data/source diagnostics.

Reserved-sector timing tests: sector 4: timing_prediction_inconclusive, timing spread 2.394269 days; sector 30: timing_prediction_inconclusive, timing spread 1.737462 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 5.64050507389717. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Initial source and QLP data checks

The raw sector97 stack and all three individual maps were inspected. Events0/1 show weak positive target-region features with similarly sized field fluctuations; event2 has a positive field-wide offset around3.2 in image flux units. There is no strong isolated source that accounts for the enormous selected light-curve depth. Weak residuals do not exclude a smaller real signal. The stack is positive across the field and its moment1.61pixels from the target is not a reliable host assignment. No Gaia query centered on this uncertain moment was run; the TIC neighborhood contains21 rows.

Each usable window contains13–14 quality-zero inside exposures and55–56 outside exposures. Gates and original timing remain unchanged. Three raw image windows are not the two supported QLP events. The exact requested TESS-SPOC pixel product returned HTTP404; this is not proof all processed products are absent or a photometric nondetection.

QLP data inspection finds17851 finite quality-zero SAP and DET values. Their1st/50th/99th percentiles are approximately0.096/0.968/10.113 for SAP and0.165/0.998/2.096 for DET. Large excursions therefore predate our additional flattening. DET_FLUX_ERR has no finite quality-zero values; the discovery explicitly enabled the empirical-error fallback. This does not identify the physical or pipeline cause of the excursions. The initial interactive percentile check failed on the empty error column; the retained audit handles that absence explicitly. The selected47% box depth must not be interpreted as a physical transit depth or a radius.

Disposition: retain as a poor-quality unresolved diagnostic, weakened as an isolated planet signal. Original older-sector timing predictions remain inconclusive; no likely new planet or unique host is established. [All maps](../../tesscut-302382075-s97-20261011/events-1.png) · [Stack](../../tesscut-302382075-s97-20261011/difference.png) · [QLP audit](../../tesscut-302382075-s97-20261011/qlp-audit.json). Raw ZIP/FITS, frozen inputs, coverage gate, image hashes and processed404 provenance passed verification. Initial source checks are complete; physical vetting is not.
