# TIC 419253850: likely off-target contamination; physical period unresolved

The Sector 17 coverage diagnostic has refined period 5.283964852 days, duration
0.18144 days and epoch BTJD 1767.675383204. Only two supported native QLP events
are present, separated by three fitted cycles. Depth is 19,081 ± 888 ppm;
period aliases and the original alternate-detrending/crowding flags remain.
The discovery plot was visually inspected. These are large, V-shaped dips,
not sufficient evidence for a planet.

Frozen checks in reserved Sectors 58 and 78 give −1,613 ± 568 and 571 ± 837 ppm.
Timing spreads of 1.639 and 2.409 days make both checks inconclusive, rather
than clean exclusions. The exploratory secondary scan is mainly one two-sample
event and does not establish a binary. Same-epoch SPOC17 gives 21,099 ± 1,156
ppm, agreeing with the large QLP feature, but both reductions use the same photons.

The original Sector 17 difference image was visually inspected and is entirely
negative with strong background structure. Its automatically emitted centroid
is invalid for source attribution. An additional unreserved adjacent Sector 18
check kept the exact frozen timing and duration: QLP gives 8,234 ± 773 ppm and
SPOC 4,480 ± 896 ppm. This is a post-hoc recurrence diagnostic, not blind validation.

Sector 18 pixels show a compact positive source reaching the 11×11 cutout edge.
A separately preserved 21×21 cutout, also visually inspected, contains the source:
four windows, formal peak SNR 123.08, difference moment 5.102 pixels off target,
0.192 pixels from TIC 419246494 (T=11.79). TIC 419246493 (T=11.18) is 0.950 pixels
from that moment; other fainter sources are blended. The source position is not
a calibrated PRF confidence region. Raw background, catalog motion and blending
limit exact component identification.

At the unchanged target timing, neighboring TIC 419246494 QLP18 gives a
6.168 ± 0.423 percent primary and 3.260 ± 0.477 percent half-phase dip. QLP17
instead gives negative depths (−4.381 ± 0.580 percent primary), so the epochs do
not cleanly establish a common physical ephemeris. This disagreement is retained.

The Gaia DR2-to-DR3 lookup maps six nearby sources and returns one known eclipsing
binary: TIC 419246493 → Gaia DR3 430569204423511552, period 0.848517904 days.
That is not a match to the 5.283964852-day diagnostic period. Catalog presence
nearby does not uniquely identify the variable; nonmatches do not establish novelty.

The other bright neighbor, TIC 419246493, likewise gives positive QLP18 depths
(3.595 ± 0.258 percent primary; 1.942 ± 0.290 percent half-phase) but a negative
QLP17 primary (−3.002 ± 0.361 percent). Blended neighboring apertures are not
independent confirmations and do not distinguish the component. Artifacts:
`results/neighbor-419246493-20261010`.

Disposition: likely off-target contamination near the bright neighboring pair;
exact component, physical period and class remain unresolved. No new planet
candidate is promoted. All failed and inconsistent checks are retained. Source
URLs, raw hashes and frozen plans are in the linked artifact directories below.

- `results/qlp-faint-419253850-reduction-20261010`
- `results/qlp-faint-419253850-adjacent18-20261010`
- `results/tesscut-419253850-s17-20261010`
- `results/tesscut-419253850-s18-20261010`
- `results/tesscut-419253850-s18-wide-20261010`
- `results/gaia-419253850-neighbors-20261010`
- `results/neighbor-419246494-20261010`
