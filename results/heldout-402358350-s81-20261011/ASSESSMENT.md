# TIC402358350: strong frozen-clock sector81 dimming, timing gate still inconclusive

Sector81 was opened after coordinator review of the committed plan, prior observations and cache history. All four period/epoch/duration predictions were fixed before retrieval; no phase, period, duration or profile-maximum optimization was performed. The strong positive measurements support recurring dimming, but the predeclared timing gate is not met. Source attribution and planet interpretation remain unresolved.

| Frozen timing family | Detrending(d) | Depth ± formal error(ppm) | Formal SNR | Supported events | Timing spread(d) | Outcome |
|---|---|---|---|---|---|---|
|40/41/54 expanded **primary**|1.5|634.6±72.2|8.79|2|0.09142|Timing-inconclusive|
|40/41 original|1.5|273.6±64.4|4.25|1|1.18683|Timing-inconclusive|
|40/41/54 expanded sensitivity|2.5|656.1±72.0|9.11|2|0.17910|Timing-inconclusive|
|40/41 original|2.5|488.4±64.2|7.60|2|1.16456|Timing-inconclusive|

The expanded duration is0.144day, giving a required timing spread below0.072day. The primary spread0.09142day exceeds that threshold, so its formal SNR8.79 does not convert this into a strict prediction recovery. Its expected formal SNR at the training depth was7.65. Positive evidence is retained without relaxing the rule. Neither timing-inconclusive nor a failed precision gate establishes absence of a planet.

The inspected four-panel plot shows a compact dip near the expanded predictions in both reductions. The original40/41 predictions are shifted relative to the feature and have much larger uncertainties. These comparisons were specified beforehand; no stronger comparison replaces the primary. All four use the same81 photons, and the two reductions are not independent observations. Sector54 had already been evaluated and explicitly added to training; the new81 observations were not used to improve these clocks.

`PREPARATION.md` and unchanged `plan.json` retain the prepared state. `execution.json` records the input and implementation hashes before the first fetch. `verification.json` reconstructs the raw FITS identity/hash and both detrended arrays, independently recalculates all four fixed-clock total/event depths, timing spreads and decision rules, and checks frozen-input integrity and freeze-before-download chronology. It uses independently written precision-sum and timing arithmetic archived in the expansion verifier; preprocessing is shared. All checks passed.

Sector81 is now deliberately opened and must never be described as a fresh holdout in later work. A posthoc timing refit or source analysis may be useful but must retain these original predictions. This run does not localize the81 dimming, settle the ambiguous discovery-sector host fits, exclude unresolved binaries, establish novelty or produce a calibrated planet probability. Formal timing/error estimates remain conditional on the selected box model and do not fully account for red noise or model mismatch.
