# Sector 104 pilot: no eligible follow-up signal

All 100 frozen targets completed: 72 below the diagnostic threshold, 28 flagged,
and no data errors. Neither the original follow-up policy nor the separate
coverage-diagnostic policy found an eligible peak. Discovery and both watchers
exited successfully, with all three selected peaks per star retained in the audit.

The metadata-only selection contains 1,955 stars after excluding the previous
1,945-star four-sector selection, all 1,535 Sector 98 stars, and cached target
photometry. Each selected target has Sector 104 and at least two reserved
sectors. Input metadata hashes, uniqueness checks, exclusions, and original
radius/noise ordering are preserved in the selection directory. These are new
to this investigation, not necessarily unstudied or uncataloged elsewhere.

The unchanged pipeline searches 0.5 days through the smaller of 20 days and
clean baseline/2.5. It uses ten-minute QLP bins and retains the existing gates.
The first three stars have usable baselines of 23.31, 10.66, and 23.54 days,
giving maximum search periods of 9.32, 4.26, and 9.42 days respectively.
Sector 98's longer usable baselines must not be assumed here.

Three control runs preserve the original raw noise and inject before binning
and detrending, with exact baseline-loader agreement at both windows:

| Controls | In search range | Period and checked-phase recoveries | Pass non-crowding gates |
|---|---:|---:|---:|
| 1.37/4.73 days, 1/2 Earth radii | 10/12 | 9/12 | 6/12 |
| 9.73/15.37 days, 2/3 Earth radii | 0/12 | 0/12 | 0/12 |
| Additional 0.83/2.37 days, 1/2 Earth radii | 12/12 | 11/12 | 8/12 |

The out-of-range cases do not measure search sensitivity. Their aliases and
failed recoveries remain in the original results. The additional explicitly
in-range run was chosen after learning the usable baseline limits, so it must
not replace or be presented as the original control design. The small sample,
one phase and duration per grid, and box-shaped signals do not establish
completeness or calibrated false-positive probabilities. Existing variability,
weak signals and odd/even failures remain visible in the individual audits.

See the [short-period](../qlp-faint-sector104-injections-20261010/audit.json),
[long-period](../qlp-faint-sector104-long-injections-20261010/audit.json), and
[additional in-range](../qlp-faint-sector104-ingrid-injections-20261010/audit.json)
audits. The first two also have grid-audit.json recording individual limits.
No reserved photometry was opened by these controls or the empty pilot watchers.
The remaining 1,855 targets are being searched separately; results are pending.
