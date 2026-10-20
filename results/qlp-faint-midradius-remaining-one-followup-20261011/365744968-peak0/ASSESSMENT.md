# TIC 365744968: unresolved screening signal

Native refinement: P=1.397133780 days, duration=0.105600 days, box depth=0.00398319 ± 0.00019521 (formal). Training sectors [98]; 17 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Broad irregular central depression with multiple local minima and positive shoulders in a gapped time series. Seventeen supported events do not establish an isolated physical transit. Source attribution and independent recurrence remain unresolved.

Reserved-sector timing tests: sector 6: timing_prediction_inconclusive, timing spread 1.607998 days; sector 32: timing_prediction_inconclusive, timing spread 1.167276 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 4.300763216965499. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Further source attribution and physical vetting remain pending. No likely new planet claimed.

## Initial source checks

The sector98 raw stack and all32 usable individual difference images were inspected. Many individual events show a compact positive residual near the target, unlike the clearly displaced sources found in several other follow-ups. However, events5,6,16 and26 have large negative field offsets, event20 has mixed stellar/field structure and only two usable inside exposures, and event30 has a positive field offset. The aggregate image is mostly negative: its maximum formal pixel SNR is only1.10 and its positive-weight moment is0.66pixels from the target. These are uncalibrated diagnostics; neither establishes a host or excludes a recurring local residual. The white circle in individual plots marks the target itself, not a second source.

The32 image windows are not the17 supported QLP events. Usable windows have2–46 quality-zero inside exposures and99–183 outside exposures. The unchanged coverage gate and frozen timing are recorded in [coverage](../../tesscut-365744968-s98-20261011/coverage.json). Raw and QLP products use the same photons and do not provide independent epoch confirmation. [Stack](../../tesscut-365744968-s98-20261011/difference.png) · [Events1](../../tesscut-365744968-s98-20261011/events-1.png) · [Events2](../../tesscut-365744968-s98-20261011/events-2.png) · [Events3](../../tesscut-365744968-s98-20261011/events-3.png).

The TIC neighborhood contains129 rows. The Gaia query retained all neighbors within three pixels of the raw stack moment, including missing identifiers, and all returned DR2-to-DR3 mappings. It returned11 Gaia sources, no variability-classifier rows and no eclipsing-binary rows. This is an incomplete variability check, not proof of novelty or exclusion of a blended binary. [Catalog query and provenance](../../gaia-365744968-scene-20261011/plan.json). The requested exact TESS-SPOC pixel product returned HTTP404; this does not establish absence of all processed products or a photometric nondetection.

Disposition: retain as an unresolved target-region signal for background-aware source checks and period/shape vetting. Broad irregular folded structure, inconclusive older-sector predictions and possible unresolved blends prevent calling it a likely new planet. No planet radius is inferred. Raw ZIP/FITS, catalog downloads, frozen inputs, coverage and image hashes passed the source verifier. Initial source checks are complete; physical vetting is not.

## Published stellar context

An exact 2MASS identity match identifies this target as THOR28, an M4 member of the young32 Orionis group in Bell et al.(2017). This adds stellar activity to the explanations that need explicit testing; it is not a measured rotation period or an exclusion of a planet. [Verified literature evidence](../../literature-365744968-20261011/ASSESSMENT.md).

## Morphology follow-up

The three already-opened sectors show broad aperture-flux modulation that is largely removed by QLP processing. The sector98 residual sits near the broad modulation minimum. Stellar activity is a stronger alternative; an embedded transit remains untested. The two downstream flattening choices cannot establish independence from the upstream processing. Older timing predictions remain inconclusive. [All panels and limitations](../../morphology-365744968-20261011/ASSESSMENT.md).
