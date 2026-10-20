# TIC422626648: stacked difference-image PRF favors the target

A mission pixel-response fit to the six sector91 events favors TIC422626648
over12 alternative catalog sources with unique Gaia DR2-to-DR3 matches.
The fixed-target chi-square is139.60 for117 degrees of freedom; the next-best
source, TIC1178220382, gives750.70. These are conditional diagonal-error
comparisons, not calibrated host probabilities or planet-validation statistics.

The free position is0.0227pixel from the registered target. The38-source reference
scene fit shifts by(−0.0403,−0.0249)pixel; its RMS residual is1.31% of the scene
peak. Neither registration nor free-position fit reaches its optimization bound.
All17 registration perturbations from−0.2 to+0.2pixel toward the runner-up retain
the target preference. This samples one direction, not full astrometric uncertainty.

The13 hypotheses include all sources from the prior local Gaia plan with unique
available counterparts. They are not a complete catalog of all possible blends.
TIC1178220387 lacks Gaia proper motion: zero was assumed and explicitly recorded.
The original missing-value failure and script are preserved in `initial-failure.json`.
Scene stars are T<=18 plus tested hosts, with linear proper motions and no parallax.
Unresolved companions and faint/unmodeled sources remain possible.

Deterministic matched-model controls recover the target100/100 times and the
runner-up100/100 times at their individually fitted amplitudes. Other weak-source
controls are less successful; TIC422626640 has a nonpositive fitted amplitude,
so its zero-amplitude controls are noise-only. These are neither equal-depth
completeness tests nor empirical noise tests. Every count remains in `fits.json`.

The inspected plot removes the fitted background plane for display; the actual
fits jointly include that plane. Residual structure remains. The previously
observed event6 background offset motivates event-by-event and leave-one-out
checks before stronger attribution. The current result is a stacked fit only.

Raw-pixel/model hashes and download URLs are retained in `models.json`.
`verify.py` reconstructs all six events and13 fixed-source fits, checks input
hashes and registration results. Verification passed; the test suite passed
49 tests in22.23s. No external reporting occurred.

**Status remains unresolved, with a binary concern.** Favoring the target region
does not resolve the Gaia RV variability, establish a planetary companion, or
supply an independent transit epoch. The sparse ZTF check remains inconclusive.
