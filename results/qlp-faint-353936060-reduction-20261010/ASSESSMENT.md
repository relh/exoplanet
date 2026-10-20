# TIC 353936060: limited separate-reduction support

The frozen native QLP ephemeris was applied unchanged to training Sectors 83–86.
No new reserved epochs were opened or phase fitted.

| Sector | QLP depth ± formal error (ppm) | TESS-SPOC depth ± formal error (ppm) |
|---|---:|---:|
| 83 | 2140 ± 281 (SNR 7.62) | 1496 ± 381 (SNR 3.93) |
| 84 | 1897 ± 329 (SNR 5.77) | No usable fixed-event measurement |
| 85 | No usable fixed-event measurement | No usable fixed-event measurement |
| 86 | No usable fixed-event measurement | HTTP 404; product unavailable |

QLP here uses ten-minute bins, SPOC native samples. Combined available QLP
measures 2082 ± 213 ppm (SNR 9.79); SPOC has only the Sector 83 measurement.
Positive SPOC support is limited and does not establish independent recurrence:
both reductions use the same underlying TESS images. Missing event measurements
are not zero depths or exclusions.

A [post-hoc matched-exposure comparison](../qlp-faint-353936060-matched-s83-20261010/ASSESSMENT.md)
finds compatible but noisy depths in QLP, SPOC corrected flux, and raw SAP.
Original detrending and timing failures remain. No host attribution or new
planet candidate is established.

[Plan](plan.json), [measurements and errors](results.json), [script](run.py).
