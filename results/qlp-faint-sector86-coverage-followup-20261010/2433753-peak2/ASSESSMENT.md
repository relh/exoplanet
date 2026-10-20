# TIC 2433753 peak 2: likely off-target contamination, physical period unresolved

Period 4.458114580 days, duration 0.092736 days, epoch BTJD 3643.488857740. Only two native supported events give 19,154 ± 1,738 ppm. Frozen Sectors 19/43 give 3,935 ± 1,341 and −1,136 ± 971 ppm, with timing spreads 1.947/1.260 days. The fewer-than-three-events and alternate-detrending flags remain.
Both older-sector checks are timing-inconclusive, not clean confirmations or
exclusions. Both discovery plots were visually inspected. Competing peaks near
1.671, 3.344 and 4.461 days remain; this is not evidence for multiple planets.
The two-event diagnostic has a selected off-phase dip at phase 0.6237 with
SNR 8.88, further weakening uniqueness of its period.

Binned QLP86 depths at the respective frozen timings are 16,512 ± 1,106 ppm
(peak0) and 18,496 ± 1,740 ppm (peak2). SPOC86 requests return HTTP 404 for both;
these are missing comparison data, not nondetections.

Both pixel maps were visually inspected. The peak0 map has eleven generic
windows and is entirely negative (maximum formal SNR −6.43), making its raw
automatic centroid invalid. Peak2 has three pixel windows and a compact positive
patch near TIC 2433754 / 2433756, raw peak SNR 18.55 and moment 2.331 pixels
off target, on a low positive background. A separate post-selection spatial-plane
sensitivity test excludes catalog sources brighter than T=17 by two pixels:
18 background pixels remain. Both corrected maps peak at pixel (3,6), 2.471
pixels off target, in that same neighboring region. Maximum residuals are 2.998
and 2.792 flux units. A three-pixel exclusion leaves zero background pixels,
so that comparison cannot be fitted. All corrected plots were inspected.

The repeated neighboring location supports contamination, especially for peak2,
but the small background sample, unmodeled spatial structure and blended stars
prevent calibrated source confidence or a unique component assignment. Raw
negative-map centroids are not rehabilitated merely by a post-hoc plane fit.
All pixel tests use the same photons and do not independently validate recurrence.

Three nearby TIC Gaia identifiers map to three DR3 sources; no classifier or
binary rows returned. These nonmatches do not establish novelty or exclude
variability. TIC 2433754 has no QLP products for Sectors 86/19; the errors are
retained. Exact source component and physical period remain unresolved. No
new planet candidate is promoted.

Evidence: `results/tesscut-2433753-s86-20261010`,
`results/tesscut-2433753-peak2-s86-20261010`, both reduction directories,
`results/gaia-2433753-neighbors-20261010`,
`results/neighbor-2433754-20261010`. Original outputs, raw URLs and hashes retained.
