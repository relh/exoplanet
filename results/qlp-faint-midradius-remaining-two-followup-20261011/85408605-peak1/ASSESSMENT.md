# TIC 85408605, peak 1: unresolved signal

Training sectors [78, 79]. Native refinement: period 7.888412413 days, duration 0.072000 days, depth 6401 ± 756 ppm (formal selected-fit error), 3 supported events. Original flags: alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Noisy central depression at the shorter of two approximately 2:1 periods. Alternative detrending prefers another period. Competing period interpretations, not two planets. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 25: timing_prediction_inconclusive, timing spread 2.2253 days. Sector 51: timing_prediction_inconclusive, timing spread 1.1610 days.

The training-only off-phase scan selects phase 0.580798, depth 2725 ± 736 ppm, formal SNR 3.70. This maximum over phase and duration is uncalibrated; it does not establish a secondary eclipse. Inconclusive timing neither confirms nor reliably rejects recurrence. Further source and quality checks remain incomplete. No secure host, novelty or credible planet claim.

Comparison of the saved native event measurements confirms that the three supported long-period events coincide with short-period events 0, 2 and 4, within 90 seconds (fitted duration 0.072 days). The one additional measured short-period event has SNR 0.76 and is unsupported; missing events are not nondetections. This establishes that the fits reuse the same three supported dips, not independent evidence for two planets. Reproducible comparison: `../85408605-peak0/compare_alias_events.py` and `alias-events.json`.


## Initial source check at the long-period ephemeris

The sector79 stacked difference image and both individual events (long-fit events1/2) were visually inspected. Both show a strong compact positive feature near neighboring TIC85408619 (T14.3361), with TIC1270584513 and TIC85408622 in the same group, plus background changes. The stacked moment is3.690pixels from the target and0.164pixels from85408619. This favors neighboring-source contamination; the exact variable remains unresolved. Formal pixel SNR and moments are not calibrated PRF confidence, and raw background was not corrected. The shared supported events make this relevant to both competing fits, without establishing a true period.

Sector78 fails the unchanged minimum-two-image-events requirement: it has only event0, with31quality-zero in-event and124baseline exposures. This is insufficient event count, not a failed detection. Both attempted processed target-pixel products returned HTTP404; this is not a nondetection or an assertion that all products are absent.

Gaia: six selected TIC entries (target plus sources within one pixel of the sector79 moment), one missing Gaia identifier (85408617), seven DR2/DR3 mappings to five DR3 sources. Two distant cross-links are retained as ambiguous, not accepted unique matches. The sole variability-classifier row is SOLAR_LIKE for the target, with score0.073876575, not a source probability. No eclipsing-binary rows were returned; nonmatches do not exclude uncataloged variability or prove novelty.

[Source verification](../85408605-peak0/source_review.json), [individual images](../../tesscut-85408605-s79-20261011/individual-events.png), [Gaia provenance](../../gaia-85408605-neighbors-20261011/verification.json). Classification: likely neighboring-source contamination, exact host and period unresolved; no new planet promotion. Reserved timing remains inconclusive.

## Separate shorter-period image check

At frozen P7.888412413 days, sector79 stack and all three individual raw difference maps were inspected. Events2/4 show strong compact off-target features near the same TIC85408619 group; added event3 is weak and mixed, without the comparable compact feature. The stacked target offset is3.678pixels. These images reinforce contamination for the shared strong dips; they do not establish an independent new signal or unique variable. Sector78 still has only event0 (31 inside/124 baseline, quality zero), retaining the unchanged two-event aggregate failure. Sector79 events2/3/4 each have31 quality-zero inside exposures, baseline124/62/83. Passing flags do not remove background concerns.

Raw exposure overlap: sector78 long/short inside counts31/31, all31 shared; sector79 counts62/93,61 shared. Overall92 shared of93 long-fit and124 short-fit inside exposures. This demonstrates extensive reuse, not independent confirmation or exact period equality. Existing processed-product404 and Gaia checks are retained without retries; no new catalog evidence or unique source probability is claimed. Original held-out timing remains inconclusive.
