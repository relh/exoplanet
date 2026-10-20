# TIC196681132: ZTF binary diagnostics remain inconclusive

Alternating ZTF dips have unequal fitted depths, keeping an eclipsing-binary interpretation open. The difference is not decisive once the substantial residual scatter is acknowledged. There is no convincing eclipse at the single tested halfway phase. These results neither classify a binary nor validate a planet.

The original TESS clock is unchanged. A simultaneous model fits even-cycle dips, odd-cycle dips and a dip halfway between them, with an independent baseline per ZTF object. All three windows use the frozen0.032-day duration. There is no phase search, retiming or outlier removal. This is a post-inspection analysis of the already opened ZTF observations.

For all658 points, even and odd depths are1.247% and2.869%, with13 points in each primary window. The difference is−1.622percentage points:−3.85 formal sigma, but−1.69 after multiplying uncertainties by the square root of reduced chi-square. Separate object-by-year-bin baselines give1.095% versus2.614%, with a residual-scaled difference of−1.59sigma. This rescaling is descriptive and does not calibrate correlated noise or establish a binary probability.

Both chronological subsets have deeper odd dips: early1.325% versus2.605%, later1.068% versus3.231%. Their residual-scaled differences are only−1.01 and−1.50sigma. They are not newly reserved tests. The prior TESS parity diagnostic also showed deeper odd dips weakly; shared nominal cycle labeling does not remove uncertainty in the long-baseline ephemeris.

The half-phase window contains34 observations and gives depth0.245% with0.194% formal error (formal SNR1.27; residual-scaled0.55). With seasonal baselines it becomes−0.054%, consistent with no dip. This tests only one phase and duration. An eccentric binary, unequal eclipse duration, equal-depth binary at twice the quoted period, or a blended companion is not excluded by this result.

All three plot panels were inspected. The odd-primary panel contains more negative points; the halfway panel has no clear isolated depression. Sparse sampling, uncertain propagated timing, intrinsic variability and residual calibration errors limit interpretation. The earlier independent-photometry agreement remains a reason for follow-up, but is not by itself planet evidence.

A deterministic synthetic scene with unequal2%/4% primary depths, a1% halfway dip and unequal object baselines is recovered numerically. verify.py independently reconstructs seven fits and their three-component covariance matrices after projecting out group baselines. Input hashes match. All49 repository tests passed in22.13seconds. No global scientific module changed.

TIC196681132 remains a higher-priority unresolved transit-like signal. The next decisive evidence should address the physical binary explanation or supply genuinely new observations; do not promote it to a securely attributed new planet candidate from these diagnostics.
