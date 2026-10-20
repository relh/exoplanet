# TIC396160833: no convincing recovery in the nearer sector25

Sector25 was selected after the inconclusive sector79 check because it is the
nearest available unused epoch. The choice and analysis were recorded before
its download. The existing discovery-only clock was unchanged; this is an
additional follow-up check, not the original reserved test.

The nominal fixed prediction gives **0.22ppm depth ±28.30ppm formal error**, or
SNR0.008, with16 in-window observations. The discovery-refined depth is159ppm.
A sensitivity scan over the311 period/epoch pairs already saved in the frozen
profile reaches only **62.91ppm, formal SNR2.23**. That maximum was selected by
looking at the new sector and is not an independent confirmation statistic.

The conditional timing spread is0.3196days, compared with duration0.1584days.
It still fails the existing half-duration timing gate. The profile scan also
omits additional epoch-floor offsets, alternative durations, red-noise and model
uncertainty. Therefore the low nominal result and weak profile maximum cannot
be presented as excluding every plausible ephemeris or all planets in the system.

This adds negative follow-up evidence and weakens the discovery lead. Neither
sector25 nor79 provides convincing independent recovery so far. The signal
remains unresolved, with instrumental explanations still possible. Both sectors
are now inspected and cannot be relabeled as untouched validation data.

`verify.py` checks the raw/source hashes and pre-download plan, reconstructs the
nominal measurement and all311 profile-pair measurements, and verifies the maximum
accounting. The observed light-curve and folded plot were inspected. No new
source localization or physical companion characterization was performed.

The test suite passed49 tests in27.62s.
