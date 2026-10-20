# TIC 31869709: frozen shorter-period prediction

This is a separate post-hoc model motivated by the three-dip training fold;
it does not replace or erase the original detrending failure. The existing
refinement routine uses only native QLP Sectors 27–30 and gives period
0.376837600530 days, epoch BTJD 2037.2428585652 and duration 0.03999744 days.
The selected BLS depth is 2,267 ± 168 ppm (formal SNR 13.50). These training
statistics are selected, not an independent detection significance.

Sectors 13 and 61 were chosen as the nearest reserved epochs before and after
the training interval, excluding already-opened Sectors 1 and 2. Both were
uncached when the model was frozen, before either download. The unchanged
predictions give:

| Sector | Depth (ppm) | Formal SNR | Timing spread (days) |
|---|---:|---:|---:|
| 13 | 763 ± 324 | 2.35 | 0.1081 |
| 61 | −1,070 ± 304 | −3.52 | 0.2071 |

Neither recovers a qualifying dip. Both timing spreads exceed half the duration
(0.0200 days), so neither is a decisive rejection of a drifting prediction.
Expected formal SNR at the training depth was 6.99 and 7.45 respectively;
this sensitivity does not repair uncertain timing. The records retain both
negative and positive measurements, raw provenance and frozen-model hashes.

This supports no promotion to a likely planet candidate. The shorter-period
training signal remains unresolved, with unknown host and no separate-reduction
confirmation. Original failed detrending checks and missing SPOC files remain
material limitations. No catalog non-match or novelty claim is made.
