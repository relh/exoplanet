# TIC 278410520: later reserved Sector 93

The existing discovery ephemeris was applied unchanged to previously uncached
Sector 93. The plan and source hashes were saved before download; the sector
was selected after the earlier Sector 11/12 tests were timing-inconclusive.

The fixed prediction gives **1,554 ± 548 ppm**, formal SNR **2.84**, with two
supported events. This is substantially weaker than the training measurement
of 5,559 ± 246 ppm. Expected formal SNR using the fitted depth is 9.33, but
that assumes the event times and depth are correct.

The timing spread remains **0.1004 days**, exceeding half the fitted 0.092736-day
duration. Consequently this test is still timing-inconclusive: the weak signal
is neither a qualifying recovery nor a clean exclusion of the period family.
No phase or period was adjusted using this sector. This does not establish a
planet or identify the host. The next useful checks are a separate reduction
of the discovery epochs and a carefully labeled timing-family test, preserving
unused epochs for prediction. Original failed predictions must remain visible.

See [plan](plan.json), [full measurements and provenance](results.json), and
[reproducible script](run.py).
