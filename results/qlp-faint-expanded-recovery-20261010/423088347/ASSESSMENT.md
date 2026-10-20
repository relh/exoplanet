# TIC 423088347: insufficient training coverage

The original four-sector search failed because Sector 46 lacks a sufficiently
long contiguous usable segment. The separate recovery examined every original
training sector. Sectors 44/45 yield 2402/2406 clean samples; Sector 46 again
fails its contiguous-segment requirement, and Sector 47 has insufficient adjacent
samples for the explicitly permitted empirical-error fallback.

Only two sectors are usable, below the frozen recovery minimum of three.
No recovery period search or reserved photometry was opened. This is an
unsearchable target under the current plan, not evidence against a planet.
The original error remains in the parent inventory; this is not an extra star.

[Plan](plan.json), [all sector checks and raw hashes](sector-checks.json),
[terminal recovery result](result.json).
