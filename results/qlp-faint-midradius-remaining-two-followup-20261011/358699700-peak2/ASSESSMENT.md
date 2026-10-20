# TIC 358699700: unresolved diagnostic

Training sectors [80, 81]. Native refinement: period 16.417681741 days, duration 0.073600 days, depth 9025 ± 831 ppm (formal selected-fit error), 3 supported events. Original flags: alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Noisy broad central depression with markedly changing scatter; another period is retained by the coverage follow-up, not a second planet. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 40: timing_prediction_inconclusive, timing spread 1.0523 days. Sector 53: timing_prediction_inconclusive, timing spread 0.7161 days.

Training off-phase scan's selected maximum has formal SNR 7.23; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Source, coverage and catalog checks below favor contamination; exact variable identification remains open. No secure host, novelty, or credible planet claim; retain for further review.

## Source and catalog checks

Sector81 stacked and both individual raw difference images were visually inspected. Both event images show a compact positive feature displaced from the target toward TIC358699657 (T14.7661), with faint TIC358699670 and TIC1814674531 nearby. The stack moment is 3.078pixels from the target and 0.197pixels from TIC358699657; these are diagnostic distances, not calibrated PRF confidence or unique variable identification. Additional background structure remains. Classification: likely neighboring-source contamination; no credible planet claim for the target.

Sector80 has only one predicted image event (32 quality-zero inside exposures,127baseline), so its source analysis fails the unchanged minimum-two-event gate. Sector81 has two image events with32quality-zero inside exposures each and127/128baseline exposures. Exact checked processed target-pixel products returnedHTTP404 for both sectors; unavailable products are not nondetections or proof that all alternative products are absent. Raw and QLP data use the same observing epochs.

The Gaia query selected the target plus all listed sources within one pixel of the sector81 moment: four TIC IDs, none missing Gaia IDs. Four DR2/DR3 mappings returned four DR3 sources, no classifier rows and no eclipsing-binary rows. One faint-source mapping has angular_distance9.4747505 and proper_motion_propagation=false; this uncertain mapping is retained. Catalog nonmatches do not exclude variability or prove novelty. Exact variable and true period remain unresolved. The competing12.291004-day fit was subsequently checked separately: both sector81 events also point to the same off-target group; see its assessment.

Image provenance, coverage, failures and plotted arrays are verified by `verify_pixels.py`/`source_review.json`; Gaia provenance is recorded in `results/gaia-358699700-neighbors-20261011/verification.json`. No gates relaxed or external submission.
