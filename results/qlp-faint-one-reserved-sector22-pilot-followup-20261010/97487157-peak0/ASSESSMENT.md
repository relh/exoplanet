# TIC 97487157: likely neighboring-source contamination

The Sector 22 signal passed the initial screen apart from unknown crowding.
Native refinement gives P=0.713786570776 days, epoch BTJD 1902.374437671963,
and duration 0.05952 days. Fixed local depth is 5,970 +/- 508 ppm, with 16
supported events. The discovery plot was visually inspected. This is a
transit-like training signal, not a securely attributed planet candidate.

The reserved Sector 45 QLP check failed. Its file has 3,450 rows (3,067
quality zero), but zero usable positive-flux samples and zero valid positive
errors. Integrity checks and raw hash are retained in the separate heldout
recovery directory. A same-sector SPOC attempt at the unchanged ephemeris
returned HTTP 404. Neither is a nondetection or a replication. No independent
observing-sector recovery is available.

At the same Sector 22 ephemeris, QLP gives 5,970 +/- 508 ppm while SPOC gives
1,341 +/- 752 ppm. These reductions use the same photons. More decisively,
both processed and raw difference images show a compact off-target deficit:
processed, 31 event windows, offset 2.736 pixels from the catalog target and
0.052 pixels from TIC 97487160; raw, 32 windows, offset 2.705 pixels from the
target and 0.057 pixels from that neighbor. The reported formal peak SNRs
(16.7 and 32.9) are not calibrated localization confidence. Both plots were
visually inspected: the positive compact feature is away from the stamp edge
and displaced from the target.

Raw images include a broad positive background. Plane fits excluding catalog
sources within two and three pixels use 60 and 36 background pixels,
respectively; both retain the compact off-target positive residual. That
plot was also visually inspected. These diagnostics favor contamination by
a neighboring variable, rather than an on-target planet. They do not prove
the precise variable or its physical nature.

TIC 97487160 is the closest catalog source to the deficit and is fainter
(Tmag 15.612 versus target 13.4927). The neighbor query returned zero QLP
products, so no direct neighbor-aperture depth or recurrence can be measured
from that collection. Gaia DR2-to-DR3 mapping returned two sources, with
zero classifier or eclipsing-binary entries. Catalog nonmatches neither
exclude variability nor establish novelty. All errors and nonmatches are
retained. Classification: likely neighboring-source contamination; exact
source and fundamental period unresolved, not a credible new planet claim.
