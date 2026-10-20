# TIC196681132: event-level source consistency

The fixed image-response comparison favors the target over TIC196683452 in21 of22 individual events. All22 leave-one-event-out stacks and both chronological halves favor the target. Thus no single event drives the previous stacked preference. This is same-sector repeatability under fixed templates, not an independent detection or a planet validation.

The existing frozen clock, scene registration and two source templates were retained from ../prf-196681132-s91-20261011. No event was removed based on its fitted preference. Event numbers are−1,0,1,2,14 through31. Per-event images and variances were reconstructed from the raw cutout with the existing quality and baseline gates. The combined image and formal uncertainty match the previous saved stack.

Event15 favors the neighbor: target chi-square2582.39 versus neighbor2508.67, each117 degrees of freedom. Both fits are poor. This is the same event previously identified as background-affected and window-sensitive; its disagreement is retained, not treated as evidence for a second host or silently discarded. All individual target amplitudes are positive, ranging15.85–32.01 in the PRF normalization. The minimum leave-one-out conditional target advantage is3200.36 in chi-square.

The first11 events have target/neighbor chi-square591.09/1929.50; the last11 have141.94/2298.52. The contrast in target residuals reinforces the need to model time-dependent image effects. Fixed global registration does not account for per-event pointing or PRF changes.

Twenty deterministic Gaussian trials per source per event recover the injected target440/440 and neighbor433/440 times. These identical-template controls measure formal separability at fitted amplitudes; they do not capture model mismatch or calibrate the real-data preference. Existing shifted-image controls are documented in the parent analysis. No statistical independence between events or host probability is claimed.

The event-consistency plot was inspected. Direct weighted-linear reconstruction verifies92 source fits across the22 events,22 omitted-event stacks and two halves. Input hashes and control totals pass verification. The full repository suite passed:49 tests in22.20seconds. An initial reconstruction guard caught single-precision input arithmetic differing from the previous double-precision analysis; the new script was corrected to use the established float conversion before computing results. The guard then passed. No scientific library module was changed.

The signal remains unresolved. These results weaken this particular separated-neighbor eclipse explanation, but do not exclude an unresolved stellar companion, uncataloged source or systematic error. There is still no independent observing epoch. Physical binary diagnostics or independent observations remain necessary before promotion to a credible new planet candidate.
