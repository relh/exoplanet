# Strong flagged Sector 30 dips: shared interval, no supported period

Native discovery plots for TIC 326149596 and 326092581 were visually inspected.
The former has one dominant irregular dip and surrounding structure; the latter
has a cluster of irregular deep deficits. Neither supplies a secure repeating
transit ephemeris. Original repetition, consistency and detrending flags remain.

A post-selection comparison includes all six stars with a discovery top-three
formal SNR >=100: 326092581, 326092880, 326104218, 326149596, 326184839,
326186462. All are on Camera 1 / CCD 1, in the small sky region recorded in the
results. Every native normalized-flux sample below 0.9 falls in BTJD 2121–2126:
respectively 84, 16, 48, 10, 60 and 28 samples; none outside. Minimum times span
BTJD 2122.7171–2124.6129, so they are not exactly simultaneous.
The largest deficit reaches normalized flux 0.0376.

This concentration across several nearby stars favors a shared observing or
processing disturbance over independent periodic planetary transits. It does
not identify the physical cause or exclude every isolated astrophysical event.
The interval and SNR threshold were chosen after examining results; this is not
a calibrated false-alarm test or preregistered rejection gate. No reserved
photometry was opened and no fitted period is promoted.

The initial interval.py comparison misread the plot axis as BTJD 2112–2116 and
contained zero samples. Its plan/results are retained as a failed diagnostic,
not supporting evidence. interval_v2.py uses the actual recorded timestamps and
explicitly records this correction; both scripts and outputs are preserved.
Only the two named discovery plots were visually inspected; other four stars
enter through the quantitative interval comparison.
