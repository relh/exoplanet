# Sector 98 faint-star extension: completed, no new likely candidate

All 1,435 expansion targets finished: 1,288 below the diagnostic threshold,
147 flagged, and no data errors. The separate 100-star pilot finished with
73 below threshold and 27 flagged. Together these are 1,535 usable searches,
disjoint from the earlier 1,945-star four-sector selection.

One peak passed all screening flags except unmeasured aperture crowding:
[TIC 46432934](../qlp-faint-sector98-followup-20261010/46432934-peak0/ASSESSMENT.md).
Its strong 1.4404-day signal localizes on the nearby known planet host
TIC 46432937, matches the published period, and falls within 1.40 minutes of
the published predicted epoch. It is contamination from a known neighbor,
not a new candidate. Its original timing-inconclusive reserved tests and
unavailable TESS-SPOC product remain in the evidence record.

The original-policy watcher completed this one follow-up. The separate
coverage-diagnostic watcher completed with zero eligible peaks across the
pilot and expansion. Discovery and both watchers exited successfully.
[Reconciliation](reconciliation.json) checks all target identities, result
summaries, raw-file hashes, both policy inventories, and the completed
follow-up's plots, measurements, and written assessment. Every selected top
three peak is retained in [audit.json](audit.json).

This was a frozen metadata-ranked search of faint nearby small stars with
Sector 98 QLP products and at least two reserved sectors. It searched periods
from 0.5 days to the smaller of 20 days and clean baseline/2.5, using ten-minute
bins and the existing detrending and quality gates. It did not search every
period, all TESS targets, or all available sectors. Catalog exclusions used
dated snapshots and do not establish novelty.

[Short-period injections](../qlp-faint-sector98-injections-20261010/ASSESSMENT.md)
recovered 12/12 periods and checked phases, with 8/12 passing non-crowding gates.
[Longer-period injections](../qlp-faint-sector98-long-injections-20261010/ASSESSMENT.md)
recovered 12/12 periods and checked phases but none passed the full gates.
The [cadence audit](../qlp-faint-sector98-coverage-loss-20261010/ASSESSMENT.md)
shows losses at both input selection and detrending. These limited synthetic
controls are not survey completeness or calibrated false-positive estimates.
No planet exclusion follows from a negative search.
