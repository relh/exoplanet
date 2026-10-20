# Limited pilot recovery controls

All12 injections completed without errors in TIC167814656, the pilot target
with the smallest measured median scatter floor. Four injections reached the
screened top-three peaks; **none passed all screening gates**. No creditable
full-screen recoveries occurred.

The grid tests periods1.37,4.73,13.13days, durations0.04/0.12days and fractional
depths250/750ppm, with one phase each. Exposure-integrated boxes are inserted
before detrending using the existing injection-grid routine. These are not
Earth-radius injections and not survey completeness estimates.

The source has strong existing flagged variability (baseline peaks near18.92,
9.44 and14.03days). A low scatter floor therefore did not select an astrophysically
quiet source. The original signal was intentionally retained, and matching
baseline periods are excluded from recovery credit. This failure must not be
interpreted as proof that all targets have equally poor sensitivity.

`verify.py` checks all12 saved trial outcomes against their individual search
records, recovery accounting and parent-run provenance. The reserved sector
was never used. Before expanding the pilot, recovery across different variability
levels is needed; this one-star result gives no reliable population completeness.
