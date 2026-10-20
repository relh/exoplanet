# TIC 320351354, peak 2: diagnostic only

Native refinement gives period 5.63842997 days, duration 0.216000 days and depth 39296 ± 1707 ppm (formal selected-fit error). There are 2 supported events after refinement. The original fewer-than-three-events and alternate-detrending flags remain; this follow-up is diagnostic only, not a waived primary screen.

The native discovery plot was inspected at the original selected seed period, as labeled in the plot. The plot shows very large, complex flux excursions and long gaps, with an irregular folded depression. This does not resemble an isolated, stable transit; variability or processing effects remain plausible.

Sector 15: timing_prediction_inconclusive; timing spread 11.4062 days. Sector 16: timing_prediction_inconclusive; timing spread 11.2135 days. Inconclusive timing neither confirms nor reliably excludes the proposed signal. Previously unopened epochs were opened only after freezing the discovery prediction; uncertainty prevents a useful recurrence test.

The off-phase selected dip has formal SNR 11.49, an uncalibrated search maximum, not a false-alarm probability or binary classification. Host attribution and novelty remain unestablished. No pixel source review has been performed for this diagnostic. No credible new planet candidate or external submission.

## Initial source check: irregular residuals and a column discontinuity

The sector76 raw stack and all four usable individual maps (0,1,2,4) were inspected. Event0 has a large negative field offset across columns0–6, with columns7–10 near zero; event4 shows a positive offset on the same side. Event1 has a weak compact target-region positive feature, but event2 has a strong negative lobe at the target and a positive lobe above it. These do not establish repeatable isolated dimming. The aggregate is predominantly negative, with its reported maximum formal SNR2.48 and moment4.98pixels from the target falling in the near-zero edge region. This is not reliable source localization.

A raw-column audit found all quality-zero flux samples finite and none exactly zero. Across6665 quality-zero rows, column medians are about98–149 for columns0–6 and−0.024 to0.040 for columns7–10. Thus the visual step is in the underlying flux, not NaN display or exact-zero padding. Its physical detector/processing cause was not established. No Gaia query centered on the unreliable stack moment was run. The TIC neighborhood contains30 rows; host and novelty remain unresolved.

Usable raw windows have59–94 quality-zero inside exposures and186–373 outside exposures. Event0 excludes two quality2048 exposures; event3 has94 inside exposures, all quality18432, and no usable baseline. Gates and original timing were unchanged. Four image windows are not the two supported QLP events. The exact requested TESS-SPOC pixel product returned HTTP404, not proof of absence of all processed products or a photometric nondetection. Raw and QLP share photons.

Disposition: the isolated-transit interpretation is weakened. Original older-sector timing predictions remain inconclusive. No reliable host or likely new planet is established. [All event maps](../../tesscut-320351354-s76-20261011/events-1.png) · [Stack](../../tesscut-320351354-s76-20261011/difference.png) · [Column audit](../../tesscut-320351354-s76-20261011/column-audit.json). Raw ZIP/FITS, frozen inputs, coverage gate, image hashes and processed404 provenance passed verification. Initial source checks are complete; physical vetting is not.
