# TIC 278410520: strong off-target evidence

Local-baseline difference images at the frozen 2.982-day ephemeris place the
dimming approximately two pixels away from the catalog target in both discovery
Sectors 65 and 67. Eight and six image events contribute, with peak formal pixel
SNRs 23.51 and 17.16. Neither difference peak is at the stamp edge.
The two difference sky positions agree within about half an arcsecond.

A complete MAST TIC cone query returned 108 objects within 0.05 degrees.
Both difference moments lie nearest **TIC 278410515** (Tmag 14.8314), at
2.35 and 1.88 arcseconds respectively. This makes that neighbor the leading
source hypothesis. The original target offsets are 1.99 and 2.07 TESS pixels.
This also offers a plausible explanation for reduction-dependent dip depths.

These are diagnostic image moments, not calibrated PRF astrometry. Proper
motions were not propagated, and fainter nearby sources remain possible.
The neighboring star's own light curve and binary status have not yet been
checked. The evidence strongly disfavors an on-target planet interpretation;
retain the signal as likely contamination pending direct neighbor verification.
No new planet candidate is established.

[Sector 65 image](../pixels-278410520-s65-20261010/difference.png) ·
[Sector 67 image](../pixels-278410520-s67-20261010/difference.png) ·
[Crossmatch](localization-crossmatch.json) · [Catalog provenance](source.json).
The pixel directories retain raw-download hashes, event numbers, moments and
image arrays. Original timing-inconclusive and reduction checks remain intact.

A [direct neighbor QLP query](../neighbor-278410515-20261010/ASSESSMENT.md) returned no available products. This is missing data, not a negative eclipse test.
