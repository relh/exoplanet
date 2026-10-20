# TIC 207468582: screening lead with possible secondary, not promoted

QLP Sectors 76–79 select a 4.61353-day dimming. Native refinement gives
P=4.612729814 days, epoch BTJD 3369.726706, duration 0.0736 days.
The fixed discovery measurement is 2,702 ± 253 ppm (formal SNR 10.67),
with ten supported events. The original screen retains only the missing
aperture-crowding flag. The discovery plot has large gaps and structured scatter.

The fit was saved before downloading reserved Sectors 16/19. They yield
362 ± 392 ppm and −212 ± 505 ppm at the fixed prediction. Timing spreads
0.484/0.462 days exceed the event duration: these are inconclusive tests,
not confirmation or a clean exclusion. No source attribution is established.

The exploratory training scan selects a possible secondary at phase 0.5323,
depth 1,328 ± 233 ppm, selected SNR 5.70. It is a binary warning requiring
verification, not a calibrated binary classification. The half-period search
peak has odd/even and inconsistent-depth flags.

A diagnostic-only third-ranked peak is near three times the period
(13.83897 days after refinement), and its selected off-phase dip is near phase
one-third. These may reuse the same events; they are not evidence for another
planet. That fit fails detrending consistency and reuses the already-opened
Sectors 16/19, so its follow-up is not independently blind. Its timing tests
are also inconclusive (SNR 1.06 in Sector 16; no usable Sector 19 depth).

**Status: unpromoted screening signal, possible eclipsing contaminant.**
Independent recurrence, secondary verification, and pixel/source attribution
remain needed. No novelty or planet claim is made.

[Discovery plot](discovery.png), [frozen ephemeris](frozen.json),
[reserved tests](heldout.json), [secondary scan](secondary.json),
[three-times-period diagnostic](../207468582-peak2/frozen.json).

Updated [pixel and neighbor checks](../../neighbors-207468582-20261010/ASSESSMENT.md) favor contamination from TIC 207468583, whose own QLP dips are deeper. Localization is noisy and binary status remains unverified; no planet promotion.

[ZTF ground photometry](../../ztf-207468583-neighborhood-20261010/ASSESSMENT.md)
around suspected source TIC 207468583 is too sparse at the frozen event times
for a qualifying measurement. This is not a negative detection.
