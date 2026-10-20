# TIC 207468582: neighbor contamination favored, attribution not final

At the frozen 4.61273-day ephemeris, discovery-sector difference images have
moments 1.25 and 1.91 pixels from the catalog target in Sectors 76/79.
Each uses four events; peak formal pixel SNRs are 5.70 and 4.70. Both moments
are closest to TIC 207468583 (Tmag 12.8497), but at different separations,
13.05 and 4.57 arcseconds. These noisy moments are not calibrated PRF astrometry;
proper motions were not propagated. The host is not definitively identified.

The neighbor's own QLP light curves show deeper dips at the unchanged target
prediction: **5,189 ± 753 ppm** in Sector 76 and **4,823 ± 550 ppm** in Sector 79
(formal SNR 6.89/8.76). This supports neighbor contamination, but both apertures
share the same images and can blend each other. It is not independent confirmation.
The fixed half-phase checks are weak (SNR −0.38/1.45); they do not establish
an eclipsing binary. In particular, they do not test the selected phase 0.5323
secondary exactly, and neither primary nor secondary was retuned here.

The target's separate-reduction check gives a combined QLP depth 2,594 ± 256 ppm
versus SPOC 1,111 ± 262 ppm over Sectors 76–79. This is additional reduction
dependence, not a proof of host identity. The original reserved timing tests
remain inconclusive.

**Status: suspected off-target contamination; no likely planet established.**
The neighbor itself is an unresolved periodic-dimming source hypothesis, not a
new planet or confirmed binary. Independent epochs, catalogs and stronger
localization are still needed before any astrophysical promotion.

[Crossmatch](localization-crossmatch.json),
[Sector 76 pixels](../pixels-207468582-s76-20261010/difference.png),
[Sector 79 pixels](../pixels-207468582-s79-20261010/difference.png),
[neighbor photometry](../neighbor-207468583-20261010/results.json),
[target reductions](../qlp-faint-207468582-reduction-20261010/results.json).
Plans, source hashes, download provenance and scripts are retained alongside results.

A [later-epoch check](../neighbor-207468583-later-20261010/ASSESSMENT.md) finds a strong fixed-prediction dip in previously unopened Sector 83 (SNR 10.11, five events), with weaker Sector 86 evidence. Timing-gate and host/classification limitations remain; no planet promotion.

A [fixed selected-secondary check](../neighbor-207468583-secondary-20261010/ASSESSMENT.md) gives positive Sector 83 evidence (SNR 3.70) but no Sector 86 recovery (−1.19). The mixed, post-hoc evidence leaves binary/planet classification unresolved.

A [dated catalog crossmatch](../neighbor-207468583-catalogs-20261010/ASSESSMENT.md)
finds no exact TIC matches across nine saved tables for the 38-star neighborhood.
This is not proof of novelty or exclusion of an unlisted binary.

An [independent ZTF check](../ztf-207468583-neighborhood-20261010/ASSESSMENT.md)
has insufficient predicted-event coverage. It cannot validate or exclude the
signal, and leaves source attribution and classification unresolved.
