# Sector 100 pilot complete: no eligible follow-up signal

All 100 frozen targets completed: 85 below the diagnostic threshold, 15 flagged,
and no data errors. Neither the original nor the separate coverage-diagnostic
policy selected a follow-up. Discovery and both watchers exited successfully;
the audit retains all three selected periodogram peaks per star.

The metadata-only selection contains 1,599 stars with Sector 100 and at least
two reserved sectors at least eight sector numbers away. It excludes all
5,435 stars from the previous four-sector, Sector 98, and Sector 104 selections,
plus cached QLP/SPOC target photometry. Metadata hashes, product uniqueness
checks, exclusion counts, and the prior radius/noise ranking are preserved.
This does not establish novelty or absence of previous investigation elsewhere.

The unchanged pipeline uses ten-minute QLP bins, the existing detrending and
quality gates, and periods from 0.5 days to the smaller of 20 days and usable
baseline/2.5. The first three stars have usable baselines of 22.13, 8.80, and
22.22 days; search sensitivity is not inferred from a sector number alone.

Twelve deterministic raw-flux injections into those three stars use periods
0.83 and 2.37 days, radii one and two Earth radii, duration 0.04 days, and one
phase fraction. All periods lie inside their actual search ranges. All twelve
recover the injected period among the top three peaks and remain within half
the injected duration at the three checked times. Nine pass gates apart from
unmeasured crowding. The three one-Earth-radius cases at 2.37 days are too weak
to pass; their failures remain in the audit.

Baseline loader arrays match exactly at both windows. These limited box-signal
controls are not completeness, calibrated false-alarm rates, or planet exclusions.
See the [injection audit](../qlp-faint-sector100-injections-20261010/audit.json)
and [period-bound audit](../qlp-faint-sector100-injections-20261010/grid-audit.json).
No reserved photometry was opened by the pilot or controls. The remaining
1,499 targets are being searched separately, with results pending.
