# TIC422626648: target preference survives event removal

All six sector91 event images favor TIC422626648 over the12 tested neighbors.
The event numbers are0,1,3,4,5,6; this analysis does not invent an event in the gap.
Each fit includes a source response plus a background plane at the registration
fixed by the previous stacked scene analysis.

The advantage over the best neighbor ranges from20.31 to155.16 in conditional
chi-square. Target amplitudes are positive for every event, ranging8.55–21.78
in the response-template normalization. These amplitudes are not fractional
transit depths. Per-event target chi-square ranges85.32–149.13 for117 degrees
of freedom; correlated noise and response-model error are not calibrated.

All six leave-one-event-out stacks retain the target preference. In particular,
omitting event6, which has the previously noted background offset, gives a
best-neighbor-minus-target chi-square of300.35. Both chronological halves,
[0,1,3] and[4,5,6], favor the target. This reduces dependence on one contaminated
event but does not supply an independent observing sector.

Matched-model deterministic Gaussian controls recover target injections120/120
and the stacked runner-up TIC1178220382 injections103/120. Weaker sources have
poor recovery at their own small fitted amplitudes; zero-amplitude controls are
noise-only. The full1560 trials and their outcomes are retained, not summarized
as universal success. No empirical-noise completeness or host probability is
inferred from these controls.

`verify.py` independently reconstructs182 weighted linear fits across individual
events, leave-one-out stacks and chronological halves, and checks provenance.
The plot was inspected. The test suite passed49 tests in22.81s. The raw input hashes and fixed templates link to the
preceding stacked-fit run. Missing proper motion for one faint neighbor and
unmodeled/unresolved companions remain limitations of that scene.

**Status: recurring dimming localized to the target region, still unresolved.**
Gaia RV variability continues to raise a binary concern, and the ZTF check is
inconclusive. Source localization cannot determine whether a companion is a
planet. A useful next diagnostic is the target's alternating and secondary-event
shape; independent photometry remains necessary for stronger claims.
