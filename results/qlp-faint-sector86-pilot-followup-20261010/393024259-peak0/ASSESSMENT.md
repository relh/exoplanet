# TIC 393024259: unresolved, with an off-target source hypothesis

Native QLP86 refinement gives period 1.575686225 days, duration 0.072 days and
epoch BTJD 3640.665929288. Five supported events give 5,911 ± 550 ppm. The
visually inspected discovery plot shows a weak folded feature and large gaps;
the seed period 1.571051634 differs appreciably from the native refinement.
The doubled-period peak has several variability/noise/coverage flags.

Frozen checks in Sectors 19 and 59 give −252 ± 407 and −571 ± 273 ppm. Timing
spreads 5.127 and 2.070 days make both inconclusive, not transit exclusions.
The selected secondary dip has SNR 3.07 and a comparable selected brightening;
it does not establish a binary. Binned QLP86 at the frozen timing gives
5,750 ± 551 ppm, consistent with native sampling. SPOC86 returned HTTP 404;
this is missing comparison data, not a null measurement.

The visually inspected TESScut86 map contains a localized positive patch near
TIC 393024226 on an otherwise negative, spatially structured background. Twelve
generic pixel windows yield raw peak SNR 10.30 and a moment 1.887 pixels off
target, 0.200 pixels from TIC 393024226 (T=14.97), with fainter blended neighbors.
The map is not uniformly negative, but neither background subtraction nor the
source position has a calibrated PRF uncertainty. The target itself is negative.
This supports a neighboring-source hypothesis without establishing a secure
component attribution or planetary source. Pixel-window and QLP-supported-event
counts differ because sampling/quality masks differ.

All three queried neighboring TIC Gaia identifiers map to DR3 sources; no
classifier or eclipsing-binary rows were returned. This is not novelty evidence
or an exclusion of variability. TIC 393024226 has no archived QLP product in
Sectors 86 or 19; explicit missing-product errors are retained.

Disposition: unresolved weak physical hypothesis, with pixels favoring an
off-target contribution. No securely attributed new planet candidate. All
available target sectors have already been opened; no unused adjacent target
epoch is available in this selection. Further progress requires stronger source
modeling or independent evidence, not relaxed discovery gates.

Evidence: `results/qlp-faint-393024259-reduction-20261010`,
`results/tesscut-393024259-s86-20261010`,
`results/neighbors-393024259-20261010`,
`results/gaia-393024259-neighbors-20261010`,
`results/neighbor-393024226-20261010`. Raw URLs/hashes and failures retained.
