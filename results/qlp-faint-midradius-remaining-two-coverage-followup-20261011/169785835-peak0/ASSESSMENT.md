# TIC 169785835: unresolved diagnostic

Training sectors [99, 100]. Native refinement: period 16.812329277 days, duration 0.133056 days, depth 3271 ± 285 ppm (formal selected-fit error), 2 supported events. Original flags: fewer_than_3_supported_events, alternative_detrending_prefers_other_period, crowding_or_missing_crowding.

Visually inspected discovery plot: Broad central depression with uneven flanking structure and large time-series gaps. The plot uses the discovery seed; the native refinement above differs slightly.

Sector 11: timing_prediction_inconclusive, timing spread 5.8988 days. Sector 37: timing_prediction_inconclusive, timing spread 4.2258 days.

Training off-phase scan's selected maximum has formal SNR 5.36; selection over phase and duration means this is not a calibrated false-alarm probability or binary confirmation. Inconclusive timing neither confirms nor reliably rejects recurrence. Initial pixel-source, quality and catalog checks are now recorded below. No secure host, novelty, or credible planet claim; retain for further review.

## Pixel and catalog follow-up

The sector100 stack and both individual raw difference images were visually inspected. They show a recurring compact positive feature approximately 2.06 pixels from the target, close to TIC169785532 (T=15.3794; moment separation 0.092 pixel). Fainter TIC994190948/994190947 are also within half a pixel of the moment. This favors off-target contamination; it does not uniquely identify the variable. Formal peak significance (61.5) and moments are not calibrated source probabilities. These are the same observing epochs as QLP, not independent recurrence evidence.

Sector100 has 57/58 unflagged inside-window exposures and 230 baseline exposures per event. Sector99 has no exposures within any predicted window: event0 at BTJD4061.570033 lies between BTJD4055.736332 and 4063.012317. The original aggregate analysis failed its two-event requirement and is retained. This coverage gap is not a nondetection. Both exact requested processed pixel products returned HTTP404, also not nondetections or evidence that every alternative product is absent.

Gaia DR2-to-DR3 queries returned four mappings, all marked proper-motion propagated, four source rows, one classifier row and one eclipsing-binary row. TIC169785532 maps to Gaia DR3 6085606747311830272, cataloged as an eclipsing binary with frequency 0.14879420499809948/day, period 6.720691844 days. The selected TESS spacing is 2.501577 times this period, about 0.010600 day longer than 2.5 periods. This is a possible alias lead, not an established ephemeris match; eclipse-time/phase verification remains undone. The other catalog nonmatches do not exclude variability. All mappings and responses are preserved.

**Disposition:** deprioritize the target-host planet interpretation because of repeatable off-target structure near a cataloged eclipsing binary. Exact variable/alias attribution remains unresolved, with nearby faint blends. No credible new planet or unique host claim.

### Fixed catalog-period diagnostic

[Comparison](../../alias-169785835-20261011/folds.png) uses the unchanged QLP preprocessing at native cadence for sectors11/37/99/100. The catalog period (6.720691844 days) and half-period are fixed; epoch is anchored to the first imaged S100 dip, BTJD4078.382362. Duration remains 0.133056 day. Neither phase nor period was optimized. Gaia's catalog epoch was not tested. All eight panels were visually inspected.

The half-period comparison has 0/1/0/2 formally supported events in sectors11/37/99/100. In S100 events0/5 are the already selected dips (formal SNR10.09/6.97); intervening sampled events1/4 have SNR approximately0/−0.60. Thus the assumed half-period clock does not yield consistent measured dips across sampled windows. Full-period S100 includes the anchor dip but a flat event2. Earlier sectors11/37 show displaced depressions in the displayed folds. These posthoc plots do not establish a matching binary ephemeris; catalog-frequency uncertainty over years, alternate eclipse phases, blending and systematics prevent using this simple comparison to exclude the nearby binary. The raw off-target evidence remains the reason to deprioritize the target-host interpretation. Original frozen/held-out results remain unchanged.
