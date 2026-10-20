# TIC 287530678: screening lead, not promoted

A 13.4766-day QLP peak passed the automatic signal-quality checks in Sectors
63–66, with unmeasured aperture crowding still flagged. Formal SNR is8.20 and
correlated-noise-adjusted SNR7.23. Native training refinement gives period
13.47591days, duration0.1056day and depth0.00356. Its training timing profile is
broad: approximately13.46494–13.48101days, under the stated heuristic profile.

The first two reserved sectors,10and11, were opened only after freezing the
training ephemeris. Their formal fixed-phase SNRs are0.72 and1.95, but extrapolated
timing spreads are1.26 and1.24days, much larger than the0.106day event. Both tests
are timing-inconclusive, not valid exclusions or confirmation. No period/phase
was retuned on these data. Other reserved sectors remain unopened by this check.

The available same-epoch TESS-SPOC Sector63 data give depth0.000553 +/-0.000987
(SNR0.56) at the frozen timing, compared with QLP's0.00499 +/-0.00078 in that
sector under the discovery binning. The SPOC data do not reproduce the QLP dip;
this is negative reduction-consistency evidence, not an independent observation
or conclusive rejection. TESS-SPOC64/65/66 downloads returned404; missing products
are not negative detections. All errors and per-sector measurements are retained
in ../../qlp-faint-287530678-reduction-20261010/.

Native training plots show structured variations around gaps, and one supported
event lies only0.0029day from a clean-segment edge. An exploratory off-phase scan
also finds a selected SNR7.07 dip, with only two supported events; this statistic
is uncalibrated and is not a demonstrated binary secondary. These features warrant
caution despite passing the automatic screen.

This is not a likely planet candidate or a novelty claim. The catalog star has
radius0.3023solar, distance50.38pc and Tmag13.12, but source attribution is unknown.
No radius is interpreted as a measured planet radius. Further timing, independent
reduction and contamination evidence would be required before promotion.

A subsequent [matched-exposure check](../../qlp-faint-287530678-matched-20261010/ASSESSMENT.md)
retains the disagreement at common native timestamps: QLP SNR4.49, SPOC PDCSAP0.56,
raw SAP0.40. Different timestamp coverage alone does not explain the QLP dip.
