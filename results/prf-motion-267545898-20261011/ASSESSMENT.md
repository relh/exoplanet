# TIC 267545898: local image tests weaken an on-target transit interpretation

Deprioritize this signal as a likely on-target planet lead. The fixed-clock discovery difference images provide little additional support for target-shaped dimming after allowing two small-displacement image terms and a background plane. This adds to the broad asymmetric light-curve morphology and the later-sector search failing the original correlated-noise gate. The physical cause remains unresolved, and the strong maximum among the broad later-sector timing alternatives is retained as positive evidence for variability.

| Discovery sector | Region radius (pixels) | Conditional target amplitude / formal error | Chi-square improvement over motion + plane |
|---|---:|---:|---:|
|27|2.5|0.50|0.25|
|27|3.5|1.18|1.39|
|28|2.5|1.29|1.67|
|28|3.5|2.82|7.96|

These are conditional linear-fit diagnostics, not transit detection significances or calibrated exclusion limits. The motion terms are spatial derivatives of the registered target PRF; adding them substantially improves the local image fits, but residual structure remains. Target-plus-motion fits have chi-square/dof about 27/13 and 113/31 in sector 27, and 108/13 and 422/32 in sector 28. In particular, the model is inadequate in sector 28. We cannot conclude that spacecraft motion alone caused the photometric signal.

The initial whole-stamp fits are retained. They have catastrophic residuals (chi-square above 12,000 for 115 degrees of freedom), dominated by strong variability elsewhere in the crowded stamp. Their preferred stars change between sectors/events and are not reliable source identifications. That failure motivated the two fixed local radii, selected after examining the whole-stamp residuals. Both radii, every tested catalog hypothesis and all signed amplitudes remain in local-regions.json. The best local alternatives can even have negative amplitudes, so no preferred neighbor is promoted to a dimming source.

All fits use the unchanged discovery-only refined clock, original difference images and diagonal formal errors. Scene registration uses catalog T<=18 positions, linear proper motion, fixed Tmag flux ratios and a common shift. This is a posthoc image-model sensitivity study. There is no retuning of event times, new observing sector, improved discovery classification, source probability or exclusion of all possible planets.

The verifier checks raw pixel and mission-model hashes and reconstructs 2,719 hypothesis measurements with an independent QR solver, including source-only, source-plus-motion and motion-only comparisons. Matched-template controls recover a planted target signal even alongside motion terms and when added to the observed residual image. They establish linear identifiability within this model, not real-world sensitivity: correlated residuals, catalog errors and PRF mismatch are not simulated. The plots were inspected. The scientific search code and the running campaign's gates remain unchanged.

Validation: the existing 49-test suite passed in 25.55 seconds after this analysis. The local matched-template checks and independent numerical reconstructions also passed.

Subsequent known-planet calibration: [Kepler-93 b](../prf-137151335-20261011/ASSESSMENT.md) also yields inconsistent source rankings with poor residuals. Consequently these image diagnostics alone cannot reject a shallow planet. This signal remains unresolved with its separate photometric concerns; no physical false-positive label or exclusion is established.
