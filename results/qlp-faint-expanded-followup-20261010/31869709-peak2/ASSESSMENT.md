# TIC 31869709: diagnostic signal family, not promoted

The third retained peak in QLP Sectors 27–30 fails alternative-detrending
consistency and has unresolved aperture crowding. It is a diagnostic-only lead.
Native refinement gives period 1.1302095480 days, epoch BTJD 2037.6345232052,
and duration 0.03968 days. The fixed training depth is 2,548 ± 308 ppm
(formal SNR 8.27), with 12 supported events. Individual events include negative
and weak measurements; this selected formal SNR is not discovery significance.

Reserved Sectors 1 and 2 were uncached when the ephemeris was frozen. Their
unchanged measurements are 77 ± 539 ppm and 181 ± 559 ppm, respectively.
Prediction spreads 0.2752 and 0.2652 days exceed half the duration, so both
checks are timing-inconclusive. They do not establish a planet nondetection.

Visual inspection shows additional dips roughly one-third of the selected
period apart. The stronger retained peaks are 0.753696845 and 1.507170070 days;
both carry secondary-eclipse or variability flags, and the latter also fails
alternative detrending. These periods are consistent with a harmonic family
near multiples of 0.3768 days. They must not be counted as separate planets.
This visual/period comparison does not determine the true period or source.
The exploratory off-phase scan finds a dip at phase 0.65639 with SNR 7.41
and duration 0.04 days, compared with strongest brightening SNR 3.85.
The scan maximum is selected and uncalibrated, not a binary classification.

[Same-epoch comparison](../../qlp-faint-31869709-reduction-20261010/results.json)
at the frozen ephemeris measures QLP depths 2,039 ± 581, 2,369 ± 641,
3,110 ± 649 and 2,793 ± 603 ppm in Sectors 27, 28, 29 and 30. All four
TESS-SPOC downloads return HTTP 404. Missing files are not negative evidence
and provide no independent-reduction validation.

No host attribution or novelty claim is supported. Retain as an unpromoted
diagnostic signal family; a shorter-period/harmonic check may clarify its origin.

A [training-only P/3 check](../../qlp-faint-31869709-harmonic-20261010/ASSESSMENT.md)
finds positive dips at all three phases and a pooled 2,133 ± 179 ppm signal
at 0.3767365160 days. This post-hoc interpretation warrants a separate frozen
short-period test; it does not overturn the original failed checks.

The [separate shorter-period prediction test](../../qlp-faint-31869709-short-followup-20261010/ASSESSMENT.md)
refined only training data before opening Sectors 13/61. Neither sector gives a
qualifying recovery, and both timing spreads remain too broad for decisive
rejection. The signal remains unpromoted.

A [dated catalog check](../../qlp-faint-31869709-catalogs-20261010/ASSESSMENT.md)
finds no exact TIC matches across the 67-source neighborhood in nine saved tables.
This is not novelty clearance. A faint neighbor lies 6.47 arcseconds away; source
attribution remains unresolved.

An [exact-name archive query](../../qlp-faint-31869709-neighbor-coverage-20261010/ASSESSMENT.md)
returned no QLP/SPOC light curves for the two selected neighbors. This does not
exclude eclipses. A [Sector 29 difference image](../../tesscut-31869709-s29-20261010/ASSESSMENT.md)
favors contamination: its moment lies 2.12 pixels from the target, near
TIC 31869705/31869706. A second-sector check is pending; neither neighbor
is yet uniquely identified as the source.

A [Sector 30 comparison](../../tesscut-31869709-s30-20261010/ASSESSMENT.md)
also places the signal off target (2.76 pixels), closest to TIC 31869705.
Together the sectors strongly favor contamination; the sky moments differ by
10.45 arcseconds, so a unique nearby host is not established.

A [direct archive availability check](../../qlp-faint-31869709-localized-neighbor-coverage-20261010/ASSESSMENT.md)
for TIC 31869705/31869706 returned no QLP/SPOC products under their TIC names.
No direct neighbor depth could be measured; the off-target classification remains
supported, while the precise source and physical classification remain unresolved.
