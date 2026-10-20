# TIC 189526569: likely neighboring eclipsing-source contamination

Frozen native QLP period 2.926354484163 d, duration 0.048 d,
epoch BTJD 3613.888368701. Local depth 11479 ± 782 ppm, six supported
events; crowding/missing-crowding is the remaining screening flag.
Discovery plot was inspected: noisy localized trough with positive shoulders
and a long gap. Passing screening is not a planet discovery.

Reserved Sector 17 measures 1871 ± 1187 ppm, but the propagated timing
spread is 0.514635 d. The result is timing-inconclusive, neither confirmation
nor exclusion. Same-sector binned QLP measures 11203 ± 795 ppm; SPOC
measures 4425 ± 711 ppm. Same photons, different processing: this is not
independent corroboration or secure source attribution.

TIC cone returned 71 entries. Processed pixels show seven event windows and
a compact difference source 3.52647 pixels from the catalog target, only
0.04254 pixels from TIC 189525884 / 620829057. The latter is explicitly marked
DUPLICATE with duplicate_id 189525884; these are not two independent stars.
The brightest-image moment belongs to another source and is not the target.

Raw 11-pixel images show eight event windows and a similar compact off-target
source (3.49887 pixels). A 2-pixel stellar mask leaves 36 background pixels
and its plane subtraction retains the dip; the 3-pixel mask leaves only six,
so that fit is unavailable. Because the source approaches the small stamp
edge, a 21-pixel cutout was checked: eight windows, 3.49744 pixels from target
and 0.07762 from the duplicate neighbor position. Both background-mask fits
(260 and 160 pixels) retain the compact off-target residual. All processed,
raw and background diagnostic plots were inspected. Formal pixel SNRs
155/224 and these moments are not calibrated localization confidence.

At the frozen target ephemeris, TIC 189525884's native Sector 85 aperture
shows primary depth 141042 ± 970 ppm and half-phase depth 40874 ± 1168 ppm.
These deep primary/secondary features favor an eclipsing stellar contaminant.
Its Sector 17 measurements (352 ± 1018 and 408 ± 1005 ppm) do not establish
recurrence or exclusion given the original timing uncertainty. Apertures and
processing products use the same images, not independent observations.

Gaia DR2-to-DR3 mapping for target plus both neighbor identifiers yields two
unique sources, zero classifier and zero eclipsing-binary rows. Correction (2026-10-11): the neighbor mapping separation is 7.16 mas
(0.00716 arcsec), not the previously stated 7.16 arcsec. The earlier
large-offset concern was a unit error. All mappings are retained; catalog
matching does not by itself establish the variable source. Catalog nonmatches do
not exclude variability. Positions were not proper-motion propagated.

Classification: likely neighboring eclipsing-source contamination, not a
credible planet candidate on TIC 189526569. The precise physical variable,
fundamental period and novelty remain unconfirmed. No planet-radius claim.

Evidence directories: `results/qlp-faint-189526569-reduction-20261010`,
`results/neighbors-189526569-20261010`,
`results/spoc-pixels-189526569-s85-20261010`,
`results/tesscut-189526569-s85-20261010`,
`results/tesscut-189526569-s85-wide-20261010`,
`results/neighbor-189525884-20261010`,
and `results/gaia-189526569-neighbors-20261010`.

Unit reference: [Gaia@AIP DR2-neighbourhood metadata](https://gaia.aip.de/metadata/gaiadr3/dr2_neighbourhood/).
