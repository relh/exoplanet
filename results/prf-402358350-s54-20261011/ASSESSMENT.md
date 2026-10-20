# TIC402358350: sector54 source remains ambiguous

Sector54 supplies two usable difference-image events, but does not resolve the transit host. Neighboring templates rank first under both tested clocks; the preferred neighbor changes with clock, motion terms, fitted region and individual event. This adds a source-attribution concern without establishing contamination or excluding a planet on the target.

Sector54 photometry had already been opened and included in the expanded fit before these pixels were downloaded. The primary image clock is therefore **posthoc with respect to54**, not an independent confirmation. Its period11.769544332days and duration0.144day are copied from the primary expanded model. A separate sensitivity analysis retains the original source-check clock (~11.772740days) without retuning. No sector81 product was accessed.

| Clock / model | Preferred template | Best chi-square / dof | Target chi-square / dof |
|---|---|---|---|
| Expanded / source + plane | 1918682563 |173.36 /117|185.96 /117|
| Expanded / source + scene gradients + plane |1918682448|151.15 /115|171.85 /115|
| Original / source + plane |1918682563|250.22 /117|274.62 /117|
| Original / source + scene gradients + plane |1918682563|161.18 /115|162.23 /115|

These are conditional image-template comparisons, not host probabilities. In particular the original-clock motion-model target and preferred-neighbor fits are almost indistinguishable. Positive target coefficients persist, but that does not uniquely assign the dip to the target. The two timing choices share the same observations, and their chi-squares should not be used to select a scientifically independent clock: they define different inside/outside pixel samples.

The expanded-clock individual motion fits prefer74037553 and1918682448; the original-clock event fits prefer74037553 and1918684054. With only two events, leave-one-out stacks repeat the other individual event and add no independent confirmation. Whole-stamp fits retain101 geometric source hypotheses; this exploratory multiplicity is another reason to avoid treating the best rank as a probability.

Local2.5/3.5-pixel regions likewise do not settle the host. Expanded-clock preferred templates are402358335 and1918682448; original-clock preferred templates are1918682538 and74037553. The target's local motion-model chi-squares are46.63/13 and80.56/33 (expanded),35.61/13 and59.75/33 (original). Structured positive and negative residuals remain visible in both inspected figures. Nominal registration is near[-0.029,+0.084]pixels, away from the bound, with scene residual RMS about0.50% of peak; this does not calibrate registration uncertainty. No registration grid or posterior marginalization was performed in this added analysis.

## Provenance and checks

`frozen.json` links and hashes the primary expanded record; `original-clock/frozen.json` preserves the earlier source-check record. `pixels/localization.json` retains the sector54 pixel download URL/hash and FITS checksums. Moment offsets are diagnostics only. `models.json` and `download_models.py` preserve the PRF model paths, URLs and hashes; the original-clock copy refers to the same primary download record.

The models retain the existing catalog-ratio scene, magnitude/geometry selection and approximate proper-motion propagation. Scene-gradient nuisance terms are two0.01-pixel finite differences of the full catalog-ratio scene, with unconstrained linear coefficients. Source-only comparisons use the same stamps and scene registration. The plane, PRF assumptions, diagonal errors and incomplete instrumental model remain limitations.

For each clock, verification reconstructs raw stacked and individual images at its saved timing, checks pixel/PRF/input hashes, and reproduces707 hypothesis comparisons using a separate QR solver, including whole-image, individual-event, omission and local-region fits. The two runs therefore check1414 comparisons in total. Matched-template injections test coefficient arithmetic, not empirical source accuracy. Both local-model figures were visually inspected. The source-only and scene-gradient outcomes, including all unfavorable alternatives, are preserved in `fits.json` and its original-clock counterpart.

The [photometric recurrence and expanded timing evidence](../expanded-402358350-20261011/ASSESSMENT.md) remains relevant, while the host remains unresolved (internal APC). Continue the separately frozen sector81 test only under the coordinator's holdout rules; successful timing there would still require physical and source vetting. This result does not justify a new planet claim or automatic false-positive classification.

Subsequent coordination note: while this report was being completed, the coordinator deliberately opened81 under its separate frozen protocol. The earlier successful verifier absence checks remain historical evidence. A later packaging-only cache-absence assertion consequently failed; `subsequent-state-check.json` retains that event. No81 data were read or analyzed by this sector54 investigation, and its source results are unchanged.
