# TIC 280625681: likely contamination from a known neighboring binary

The native QLP86 refinement gives period 2.872446723 days, duration 0.092736 days
and epoch BTJD 3642.756804239, with three supported events and depth 18,974 ±
1,312 ppm. The visually inspected discovery plot shows a noisy deep folded dip
and large data gaps; the alternate-detrending and crowding flags remain.
Frozen Sectors 18/19 give −406 ± 788 and −527 ± 796 ppm with timing spreads
3.088/3.046 days, so both are inconclusive. The exploratory secondary scan
has selected SNR 2.98, insufficient for binary assignment alone.

Binned QLP86 gives 18,581 ± 1,315 ppm. SPOC86 is unavailable (HTTP 404), not a
null measurement. The visually inspected pixel map has seven generic windows
and a compact off-target enhancement on a positive background: raw peak SNR
391.82, moment offset 3.183 pixels, 0.043 pixels from TIC 280625668 (T=14.10).
Fainter blended sources are also close. The formal SNR and centroid are not
calibrated PRF confidence estimates. Background-plane sensitivity tests cannot
fit: two/three-pixel exclusions leave only eight/zero background pixels. No fit
was forced, and the failed-mask outputs remain explicit.

TIC 280625668 maps to Gaia DR3 492706764026937088, a known eclipsing binary
with period 2.876014482 days, differing from the TESS period by −0.12405 percent.
Three nearby stars map to DR3; one classifier and one eclipsing-binary row are
returned. The spatial association and close period strongly favor neighboring
binary contamination, although exact blend contributions remain unmodeled.
No neighbor QLP products exist for Sectors 86/18 in the archive query; these
missing-product errors are retained rather than treated as nondetections.

Disposition: likely known neighboring binary contamination, not a new planet.
No further reserved target epochs were opened for this source review.
Evidence: `results/qlp-faint-280625681-reduction-20261010`,
`results/tesscut-280625681-s86-20261010`,
`results/gaia-280625681-neighbors-20261010`,
`results/neighbor-280625668-20261010`. Raw URLs, hashes and limitations retained.
