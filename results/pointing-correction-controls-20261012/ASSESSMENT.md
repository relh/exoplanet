# Pointing correction improves known controls, but does not pass every frozen gate

A non-event-trained pointing correction recovered the correct Kepler-93 source ranking in sector 41 and preserved the fitted known-source amplitude within 6.6% in every control. All four sectors have better predictive non-event RMS. The predeclared requirement that source separation improve in **every** sector fails for the resolved contaminant in sector 33: its already large separation decreases slightly. **No candidate correction is applied.** This conservative gate failure is not evidence that the method is generally unusable; it limits what this bounded experiment authorizes.

## Real-control measurements

The separation column is best alternative χ² minus expected-template χ²; positive favors the expected template. Expected Kepler-93 identity is TIC 137151335. For TIC 106583384 the control establishes an offset contaminant region; template 780959515 was the archived preferred representative. This does not independently establish the exact contaminating star's identity.

| Control | Sector | Test RMS / constant | Source separation before → after | Expected amplitude change | Frozen gate |
|---|---:|---:|---:|---:|---|
| Kepler-93 | 40 | 0.2074 | 25.73 → 34.64 | 1.10% | pass |
| Kepler-93 | 41 | 0.1283 | −40.83 → 6.12 | 6.56% | pass |
| Offset contaminant | 33 | 0.2272 | 3643.99 → 3553.71 | 0.27% | fail: separation decreased |
| Offset contaminant | 34 | 0.1566 | 127.87 → 183.44 | 0.17% | pass |

Sector 41 switches from neighbor 137151319 to the known Kepler-93 host. Its best χ² improves from 389.9 to 126.6 for 117 degrees of freedom. Sector 40 improves from 321.6 to 159.0. The contaminant remains the preferred region in both sectors, with χ² improving from 1784.1 to 1436.2 and from 724.8 to 657.0. Large remaining contaminant residuals still show model mismatch. These likelihood contrasts use unchanged formal pixel noise and are not host probabilities.

## Frozen method and preserved failure

[plan.json](plan.json) precedes all results and hashes the original runner and raw/template/clock/model inputs. All observations were already opened; the experiment is retrospective. Each pixel is fit with an intercept and two standardized POS_CORR components outside a mask of ±max(0.5 day, three transit durations). Alternating two-day blocks train and test predictive RMS. The final correction trains on all eligible non-event samples and subtracts only pointing terms. Event clocks, local baseline windows, formal errors, templates, registrations and host hypotheses are unchanged. Every original image event is retained: six per Kepler-93 sector and ten per contaminant sector.

The first runner stopped before image measurements because it unnecessarily demanded pointing at quality-flagged cadences too. Missing pointing occurs at 10, 10, 10 and 9 finite timestamps, respectively, but **zero quality-zero timestamps** in every control. [initial-failure.json](initial-failure.json) preserves the failure. The separately frozen [plan-v2.json](plan-v2.json) and [run-v2.py](run-v2.py) correct only the assertion to use existing quality eligibility; no eligible observation is removed and no scientific gate is changed. Original script and plan remain intact.

## Preservation limits and decision

The 20% gate concerns **fitted template amplitude**, not independently calibrated integrated transit depth. Background and pointing residuals can change the stamp-integrated difference: Kepler-93 sector 41 changes from −1.37 to +7.03 flux units while template amplitude changes only 6.56%. Sector 40 changes 10.21 to 9.34; contaminant totals are 93.69 to 93.61 and 96.69 to 96.78. These descriptive stamp sums have no dilution or aperture calibration and should not be interpreted as corrected physical depths.

Coefficient uncertainty and time-correlated residuals are not propagated into image errors. The method learns the combined scene's pointing response, not individual empirical PRFs. Known-source rankings still rely on the archived mission-template model. A favorable real control is stronger than recovery of an injection built from the fitted template, but four retrospective sectors cannot calibrate close-blend host probabilities or prove general signal preservation.

Because the all-controls gate fails, no off-event injections, alternative-background sweep, or candidate application is undertaken. Those optional checks have not been completed. This package offers a measured method-development result, not a new exoplanet candidate or a calibrated probability.

## Verification

[verify.py](verify.py) independently reconstructs nearest-cycle masks, train/test splits, pointing regressions using QR, unchanged event membership, inverse-variance image combinations and 176 fixed-template/plane fits. It checks all raw and supporting input hashes and reproduces the frozen decisions. [verification.json](verification.json) records the passing arithmetic/provenance audit. [controls.png](controls.png) was visually inspected: the correction removes substantial structured Kepler-93 residuals while retaining the conspicuous contaminant location. Panel color scales are independent.

No downloads, candidate-data correction, shared scientific source edits, shared documentation edits or external submissions occurred.
