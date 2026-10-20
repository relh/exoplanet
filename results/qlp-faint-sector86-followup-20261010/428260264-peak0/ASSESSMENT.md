# TIC 428260264: likely contamination by a close known eclipsing binary

Native QLP86 refinement gives period 1.142977951 days, duration 0.1056 days and
epoch BTJD 3641.192510182. Seven supported events give 2,501 ± 294 ppm. The
visually inspected plot shows a shallow folded dip amid noise and large gaps.
The half-period peak fails odd/even, duty-cycle, SNR and detrending checks.
The exploratory secondary scan reaches only SNR 1.67.

Frozen Sectors 18/19 give 742 ± 240 and 1,526 ± 264 ppm at nominal timing,
but spreads of 3.853/3.801 days render both timing-inconclusive. Those nominal
positive depths are not secure recurrence confirmation. Binned QLP86 gives
2,544 ± 293 ppm. SPOC86 returns HTTP 404: unavailable data, not a null signal.
Sector 59 remains unopened as target photometry and is available for a separately
planned frozen follow-up; no search or timing retuning in it has been performed.

The visually inspected TESScut86 map has fifteen generic windows and a nearly
uniform positive background. Raw peak SNR 137.89 and automatic offset 3.829 pixels
are invalid for localization. A post-selection weighted plane excluding T<17
catalog sources by two pixels uses only 15 background pixels and leaves a
compact target-region enhancement (maximum pixel offset 0.588, residual 1.234
flux units). Three-pixel exclusions leave no background pixels; no fit is made.
The corrected map was inspected. Fainter close blends remain unresolved.

A separate cadence-level extraction applies the existing plane method with the
same two-pixel exclusion at each cadence, without timing retuning or flattening.
Target-centered radii 1.5/2 pixels yield 1,849 ± 191 / 2,330 ± 229 ppm at frozen
timing, formal SNR 9.68/10.19 and 12/11 supported windows. It uses more usable raw
pixel cadences than QLP; event counts are not equivalent across masks. The plot
shows the first four generic windows and was inspected; all qualifying windows
enter the measurements. This supports a target-region dip in the same photons,
not independent validation or unique host attribution. Published pixel errors
omit correlated noise and background-model systematics, and the spatial method
was chosen post-selection. The small background sample is a material limitation.

A subsequent catalog check maps the target and five neighbors to six DR3 sources.
TIC 643593883 (T=18.6975), only about 0.694 pixels from the target, maps to Gaia
DR3 249841717943942784 and is a known eclipsing binary with period 1.143688153
days. The TESS period differs by −0.06210 percent. This close blend lies toward
the residual maximum; a target-centered aperture includes its photons. Its
catalog brightness contrast permits a maximum undiluted-to-total contribution
of roughly 0.326 percent relative to target flux, comparable to the measured
0.25 percent dip if its eclipse is deep (bandpass/aperture uncertainties apply).
This is a plausibility check, not a calibrated dilution fit or unique attribution.

Disposition: likely contamination from close known eclipsing binary TIC 643593883.
The exact blend contribution remains unmodeled, but the matching period and
subpixel separation explain why the corrected signal remained near the target.
No new planet candidate is promoted. Sector 59 is still unopened; a further
check there would not by itself separate this blend. Catalog evidence is in
`results/gaia-428260264-neighbors-20261010`.

Evidence: `results/tesscut-428260264-s86-20261010` (raw, background and cadence
aperture artifacts), `results/qlp-faint-428260264-reduction-20261010`,
`results/neighbors-428260264-20261010`. Source URLs and hashes are retained.
