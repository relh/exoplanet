# TIC 167307093: diagnostic lead, not promoted

The four-sector QLP search (66–69) selected a 14.024475-day dimming,
formal SNR 8.54 and depth 0.00453. It **fails the original screening criteria**:
alternative detrending prefers a different period, and aperture crowding is
unmeasured. The watcher followed it only under its pre-existing diagnostic rule.

Native-cadence training refinement gives period 14.016171 days, duration
0.072 days and epoch BTJD 3109.488402. The fixed training measurement is
4,378 ± 529 ppm (formal SNR 8.28), with four supported events. The discovery
plot shows uneven phase coverage and structured residuals; the selected folded
dip alone is not reliable planet evidence. Supported training events lie
0.067–0.359 days from cleaned segment edges.

The ephemeris was saved in [frozen.json](frozen.json) before the first downloads
of reserved Sectors 1 and 2. Their fixed-ephemeris SNRs are −0.12 and 1.53.
However, the propagated timing spreads are 1.254 and 1.235 days, far longer
than the fitted duration. Both tests are **timing-inconclusive**, not decisive
non-detections and not confirmation. The timing profile is heuristic and ignores
correlated noise/model mismatch. Other reserved sectors have not been used by
this follow-up.

The exploratory training-only off-phase scan selects a secondary-like dip at
phase 0.898 with SNR 3.48, comparable to its largest brightening (3.44).
This selected statistic is uncalibrated and does not establish a binary.

No host attribution, new catalog clearance, or planet validation is established.
Keep the original detrending flag and this negative/inconclusive evidence.
Raw URLs, hashes, measurements and source versions are in [frozen.json](frozen.json),
[heldout.json](heldout.json), and [secondary.json](secondary.json).
