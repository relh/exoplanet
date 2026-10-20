# TIC 438792601: likely off-target contamination

The primary four-sector discovery peak near 0.781427 days passes existing gates except unmeasured aperture crowding. Native-cadence refinement gives period 0.781550277 days, duration 0.05952 days, and depth 780 ± 76 ppm (formal error), with 19 supported training events. The discovery plot was inspected: the folded shallow dip is visible amid substantial scatter and gaps. Formal selected SNR is not a calibrated discovery probability.

The frozen fit was checked in reserved QLP sectors 11 and 38. Both conclusions are timing_prediction_inconclusive: projected timing spreads are approximately 0.6855 and 0.4881 days, respectively. Fixed-center depth estimates are negative, but the prediction uncertainty prevents treating those measurements as a reliable exclusion. They are not confirmations either. The off-phase exploratory scan has maximum selected dip SNR about 2.18, not a calibrated false-alarm probability or proof of no secondary.

Raw Sector 99 and 100 source checks favor contamination; a Gaia catalog check now favors neighboring TIC 288891067 as the contaminating eclipsing system. The pool's dated catalog exclusions do not establish novelty. Retain as a likely contaminated signal with a favored but not uniquely proven neighboring variable source, not a credible new planet candidate. No submission or external contact has been made.

## Raw-pixel follow-up

[Sector 99 source analysis](../../tesscut-438792601-s99-20261011/ASSESSMENT.md) shows a compact dimming source about 2.21 pixels from the target, near a blended group including TIC 288891067 and 438792607. Twenty-four image-event windows contribute. This favors off-target contamination without resolving the exact variable source; it does not support an on-target planet. The approximately 1.57-Earth-radius estimate is conditional on an on-target transit and should not be used as a planet measurement. The requested SPOC pixel product returned HTTP 404 and its failure is retained.

[Sector 100](../../tesscut-438792601-s100-20261011/ASSESSMENT.md) repeats a compact off-target dimming source using the unchanged ephemeris: 33 event windows, offset about 2.03 pixels, moment about 3.35 arcseconds from the Sector 99 moment. Both lie near the same faint group, strengthening the contamination interpretation without resolving its members. These are already-opened discovery epochs, with the same photons as QLP; this is not independent transit confirmation.

## Gaia catalog cross-check

[The 14-source Gaia query](../../gaia-438792601-neighbors-20261011/ASSESSMENT.md) finds TIC 288891067 mapped to Gaia DR3 6067173709758352000, an ECL-classified eclipsing-binary candidate. Its geometric-model period is 0.7816034974 days, about 4.60 seconds (0.00681%) longer than the native TESS fit. This star is also nearest both raw-image moments. The combination strongly favors a contamination explanation involving this known candidate eclipsing system. The periods are not identical, no joint period/phase uncertainty comparison was performed, and the blended pixels cannot prove unique attribution. It is not a new on-target planet candidate.
