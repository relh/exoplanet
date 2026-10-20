# TIC 207468583: selected secondary remains unverified

Applied the original target training scan's selected secondary phase 0.5323383,
period 4.613529479 days and duration 0.092 days unchanged to the neighbor.
These light curves had already been inspected for their primary dip, so this
is a post-hoc diagnostic, not a blind validation or new period search.

| Sector | Depth ± formal error (ppm) | Formal SNR | Supported events |
|---|---:|---:|---:|
| 76, discovery epoch | 1,688 ± 808 | 2.09 | 1 |
| 79, discovery epoch | 1,939 ± 449 | 4.32 | 2 |
| 83, later epoch | 1,584 ± 428 | 3.70 | 2 |
| 86, later epoch | −792 ± 667 | −1.19 | 0 |

Sector 83 has a positive dip at the selected secondary prediction, adding
some support to the binary hypothesis. Sector 86 does not recover it, and
no secondary-specific timing posterior or correlated-noise false-alarm
calibration exists. Neither the selected training SNR nor these diagnostics
establish a binary; they also do not justify a planet interpretation.
Retain the mixed evidence and the stronger primary recurrence separately.

[Plan](plan.json), [per-event measurements and provenance](results.json), [script](run.py).
