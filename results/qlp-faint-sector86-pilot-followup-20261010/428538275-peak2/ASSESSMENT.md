# TIC 428538275: known neighboring binary contamination and period alias

The third screened peak refines to period 2.849934976 days, duration 0.072 days
and epoch BTJD 3641.858801001. Four native supported events give 5,611 ± 607 ppm.
The original alternate-detrending and crowding flags remain. The discovery plot
was visually inspected: additional dips appear near one-third and two-thirds
phase. Stronger peaks at 0.950198738 and 1.899360233 days already carry secondary
or variability flags. The selected secondary at phase 2/3 is 5,502 ± 784 ppm,
consistent with aliasing, not a unique planetary period.

Frozen checks in Sectors 19 and 59 give 482 ± 426 and −376 ± 340 ppm, with
2.550 and 1.046-day timing spreads. These are inconclusive, not exclusions.
Binned QLP86 at frozen timing gives 5,472 ± 601 ppm. SPOC86 is unavailable
(HTTP 404), retained as missing comparison data.

The visually inspected TESScut86 map shows a strong compact positive source,
six generic pixel windows, formal peak SNR 545.84, moment 5.339 pixels off target
and 0.169 pixels from TIC 428538335 (T=11.52). Formal errors/centroids are not
calibrated PRF confidence intervals; faint blends and catalog motion remain
limitations. This clearly favors an off-target source.

TIC 428538335 maps to Gaia DR3 251466285032523008, an eclipsing binary with
period 0.950081524 days. The diagnostic TESS period is 2.999674 times that
period (−0.01086 percent relative to the three-period harmonic). At the frozen
target timing, the neighbor's QLP86 depth is 12.366 ± 0.056 percent, with a
4.138 ± 0.066 percent half-phase dip. QLP19 is negative at that uncertain
long-baseline timing (−2.013 ± 0.061 percent primary), so it is not independent
recurrence confirmation. Shared neighboring apertures are not independent data.

Disposition: contamination from the known nearby eclipsing binary, with the
2.85-day feature representing a three-period alias. No new planet candidate.
Catalog mappings, raw hashes and inconsistent/failed checks are retained in:
`results/qlp-faint-428538275-reduction-20261010`,
`results/tesscut-428538275-s86-20261010`,
`results/neighbors-428538275-20261010`,
`results/gaia-428538275-neighbors-20261010`,
`results/neighbor-428538335-20261010`.
