# TIC 115351953: noisy two-event diagnostic, not promoted

The native-cadence refinement gives P=8.257993204 days, epoch BTJD
2720.737985809 and duration 0.048 days. The fixed QLP measurement is
11,920 ± 1,314 ppm (formal SNR 9.07), with two supported events of seven
samples each. It fails the three-supported-event requirement and lacks
measured QLP aperture crowding. This is a coverage diagnostic only.

The discovery plot was inspected. Its title and fold use the original
8.271118306-day search seed, not the subsequent native-cadence refinement.
Strongly changing scatter and other negative excursions complicate interpretation.
The exploratory off-phase scan selects a 13,894 ± 2,023 ppm dip, predominantly
from one event. That selected statistic is not a calibrated secondary-eclipse
significance and does not establish a binary.

At the frozen refined timing, reserved Sectors 24 and 25 give respectively
−192 ± 746 and −1,622 ± 812 ppm. Propagated timing spreads of 1.840 and
1.762 days greatly exceed the duration, so these checks neither confirm nor
exclude recurrence. Sectors 78 and 79 remain reserved and unopened here.

The [same-epoch reduction comparison](../../qlp-faint-115351953-reduction-20261010/results.json)
measures 11,919 ± 1,313 ppm in QLP versus 1,744 ± 725 ppm in SPOC (SNR 2.41,
zero individually supported events). Sampling differs: QLP supports events 0
and 1, while SPOC measures events 1 and 2. Crucially, their overlapping event 1
is 12,435 ± 1,886 ppm in QLP versus 1,599 ± 914 ppm in SPOC. Thus the
large QLP dip is not reproduced even at the overlapping event. Shared input
images and different processing mean this comparison is not independent sky
confirmation or a definitive exclusion of a smaller signal.

No pixel source attribution was performed for this weak, processing-dependent
lead. Its physical cause, host and period remain unresolved. No planet-size,
novelty or discovery claim is made. Original evidence and failed checks are retained.
