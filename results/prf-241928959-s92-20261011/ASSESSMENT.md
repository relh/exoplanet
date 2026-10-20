# TIC241928959: conditional target preference

Sector92 image-response fits favor TIC241928959 over nearby TIC241928961. This weakens the specific known-neighbor eclipse explanation. It does not exclude an unresolved companion or establish a new planet candidate.

The frozen clock and five raw event windows are unchanged. Official STScI PRF downloads, detector coordinates and the pixel-file hash are in models.json. Both hypotheses use Gaia DR3 proper-motion-propagated positions, with separation0.46194pixel at the observation epoch. The previous unpropagated catalog separation was about0.50pixel.

The initial T<=18 scene failed to converge in the nonnegative linear solver. That script and failure are preserved in analyze_t18.py and initial-failure.json. The alternative T<=16 scene contains21 stars and retains both competing hosts. This brightness cutoff is a model change after a numerical failure, not a solution proving the fuller scene is unnecessary. Fainter and outside sources remain omitted.

The successful scene registration is[-0.00822,−0.04856]pixels; its residual RMS is1.40% of the scene peak. At that registration the target/neighbor difference-image chi-square values are110.80/426.89, each117 degrees of freedom. Both amplitudes are positive. A free-position fit moves0.05061pixel from the registered target, reaching chi-square108.50. Neither shift fit is at its boundary.

All17 tested registration offsets along the pair direction, from−0.2 to+0.2pixel, prefer the target. The smallest conditional chi-square advantage is48.81. This finite one-dimensional check is not a registration confidence interval, host probability, or exhaustive model-mismatch test.

Identical-PRF Gaussian controls recover both hosts100/100 times. Injections into41 shifted real difference images recover each host41/41 times. These controls omit PRF mismatch; the shifted images overlap and are not independent. The three-panel fit image was inspected: the principal difference feature is reproduced near the target, with remaining spatial residuals.

Event-level analysis in ../prf-events-241928959-20261011 favors the target in all five events, all five leave-one-out stacks, and both chronological groups (three and two events). Event6 is substantially deeper than the others; that variation is retained. Its removal does not change the preferred host. None of these shared-sector checks provides independent observing confirmation.

Verification reconstructs the five-event stack and both source fits and checks input hashes, detector coordinates, control totals and registration outcomes. The event analysis independently reconstructs24 linear fits. No scientific fitting module changed; the same modules passed49 repository tests in the preceding investigation turn. These are configuration-specific evidence checks, not a newly run test-suite claim.

The target's elevated Gaia RUWE, incomplete binary diagnostics, close unresolved-source possibilities and absence of an additional returned TESS epoch still limit interpretation. Next useful work is physical binary vetting or independent photometry; the scene-model convergence limitation should also be resolved before stronger attribution claims.
