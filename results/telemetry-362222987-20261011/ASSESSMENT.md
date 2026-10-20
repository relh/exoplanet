# TIC 362222987: discovery telemetry checks

Using the unchanged discovery period, epoch and duration from peak 0, inspect SAP_BKG, POS_CORR1/2 and MOM_CENTR1/2 around the four measured events in sectors 17–18. No reserved data are used. The code is adapted from the prior TIC396160833 diagnostic.

The strongest flux event (event 0, local flux SNR 7.08) coincides with a substantial curved background variation. Its background residual relative to the local outside-event linear fit is −2.68 times the outside residual scatter. This is a descriptive ratio, not a significance. The other background ratios are +1.30, +0.33 and −1.19. The figure shows different background behavior between events; this does not demonstrate a common instrumental mechanism.

Pointing-correction residual ratios have absolute values at most 1.28, and flux-weighted centroid ratios at most 1.15. There is no consistent centroid displacement across all four events. Lack of such a displacement does not establish the target as the source or rule out a blend. Nonlinear trends limit the local linear diagnostic.

This adds concern about the dominant event and leaves the transit-like signal unresolved. Later-epoch recovery remains required. The plan records hashes of both FITS inputs, the frozen discovery record and script. A deterministic linear trend plus injected 0.125 offset is recovered exactly; an independent polynomial-fit reconstruction verifies all 20 channel/event measurements and input hashes. The plot was visually inspected.

Validation: `uv run pytest -q` passed all49 tests (32.97 seconds).
