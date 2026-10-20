# TIC 453330136: likely off-target contamination

Native refinement gives P=1.628318789 days, epoch BTJD 2939.930246203 and
duration 0.03968 days. Fixed native QLP gives 6,501 ± 715 ppm (formal SNR
9.10), with seven supported events. The discovery plot was inspected and
shows a shallow folded dip in noisy, gapped data. The exploratory off-phase
maximum is weak (formal SNR 2.35), not a calibrated binary classification.

At frozen timing, Sectors 20/73 give −773 ± 810 and 2,006 ± 793 ppm.
Timing spreads of 1.320/0.433 days exceed the duration, so these checks are
inconclusive rather than exclusions. The [same-epoch comparison](../../qlp-faint-453330136-reduction-20261010/results.json)
gives 6,355 ± 724 ppm in binned QLP and 1,775 ± 600 ppm in SPOC. These
share input images; the much shallower SPOC measurement weakens the on-target
interpretation but does not independently establish the source.

The [pixel map](../../tesscut-453330136-s60-20261010/analysis.json) was
inspected: a compact positive residual over 12 windows has formal peak SNR
19.63 and lies 1.998 pixels off target. Its moment is 0.050 pixels from
faint TIC 453330129 and 0.401 pixels from brighter TIC 453330128. These
nearby sources are not uniquely separable with an uncalibrated moment.
Background residuals and neighboring sources remain in the map.

[Gaia](../../gaia-453330136-neighbors-20261010/results.json) maps all three
queried nearby entries. TIC 453330128 maps to DR3 990883937697428480,
which has classifier label `RS` and score 0.47321752; no eclipsing-binary
row is returned. That catalog score is not used as a probability of the TESS
source class or identification. TIC 453330129 is a different DR3 source.
The QLP lookup for TIC 453330128 has no Sector 60 or 20 product; both explicit
missing-product errors are [retained](../../neighbor-453330128-20261010/results.json).

Likely off-target contamination. Exact host component, physical class and
period remain unconfirmed. Neither the classifier nor catalog nonmatches
establish novelty, and no new planet is promoted.
