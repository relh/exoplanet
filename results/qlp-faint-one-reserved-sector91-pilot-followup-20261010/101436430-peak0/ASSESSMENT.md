# TIC 101436430: likely neighboring-source contamination

No securely attributed target planet. The raw Sector 91 difference image is
compact and displaced from the target toward TIC 185284269 (T=13.673).
Its local moment is 3.6481 pixels from the target and 0.1594 pixels from that
neighbor. Fainter TIC 1180089556 (T=19.309) is 0.6523 pixels from the moment;
the exact variable source or physical system is not proven.

Frozen native QLP fit: P=2.978241909875 d, duration 0.1056 d,
epoch BTJD 3777.542202465. Local depth 7938 ± 681 ppm, four supported events.
Discovery plot inspected: noisy localized dip with positive shoulders and gaps.
Excluding the visibly noisy BTJD 3787–3789 interval does not alter the local
measurement or four supported events.

The reserved Sector 51 check is timing-inconclusive: −1798 ± 2745 ppm with
2.2420 d timing spread. It is neither confirmation nor a valid rejection.
Same-sector 10-minute-binned QLP measurement is 7807 ± 700 ppm. TESS-SPOC
light curve and target-pixel requests both returned HTTP 404; missing products
are not nondetections or independent corroboration.

Raw TESScut has six usable pixel event windows (distinct from the four supported
light-curve events). Difference and background plots were visually inspected.
A spatial plane fit using 46 background pixels retains the compact off-target
feature. The larger exclusion mask leaves only ten pixels and has no fit.
Formal peak pixel SNR ~349 is not calibrated positional or planetary confidence.
These are the same photons as QLP, not independent observations.

Neighbor TIC 185284269 has no listed QLP products for Sectors 91 or 51;
both missing-product errors are retained. Gaia DR2-to-DR3 lookup of the target,
TIC 185284269 and faint TIC 1180089556 returned three source records but no
variability-classifier or eclipsing-binary entries. Nonmatches neither exclude
an eclipsing neighbor nor establish novelty. The evidence favors contamination,
while the precise variable and fundamental period remain unresolved.

Evidence: [reduction](../../qlp-faint-101436430-reduction-20261010/results.json),
[raw pixels](../../tesscut-101436430-s91-20261010/analysis.json),
[background sensitivity](../../tesscut-101436430-s91-20261010/background.json),
[neighbor aperture availability](../../neighbor-185284269-20261010/results.json),
[Gaia](../../gaia-101436430-neighbors-20261010/results.json).
