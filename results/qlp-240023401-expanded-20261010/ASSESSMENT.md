# TIC 240023401: eclipsing-neighbor contamination

Rejected as a planet around TIC240023401. A real 2.07537814-day repeating dimming
passes independent-sector tests but originates off-target.

Already-opened sectors43/44/20/60 refined the period/phase. The prediction was
frozen before downloading71/72 (both cache flags false). These measure2403 ±182ppm
and2034 ±182ppm, formal SNR13.18/11.18, and pass preset recovery gates. Preserve
the original timing-inconclusive sector20/60 results; this was expanded follow-up,
not a second independent discovery. Sector73 remains unopened.

Sector43 difference imaging uses10 events, peak formal SNR27.3, offset1.38pixels
from the catalog target; sector44 uses11events, peak SNR24.9 and a consistent
northern off-target location. These are diagnostic moments, not calibrated PRF
astrometry. Sector60 TESS-SPOC pixel download returned404; error retained separately.

ZTF independently resolves the likely contaminant as TIC240023393, 28.3arcsec
from the target. At the frozen TESS ephemeris, with no period/phase optimization,
OID661212400022187 (r) shows0.1934 ±0.0036mag eclipses across17distinct events;
OID661112400007716 (g) shows0.2321 ±0.0059mag across10events. A separate r object
series supports the same eclipse. Catalog position matches are within0.05arcsec.
See [ground photometry](../ztf-240023401-contaminants-20261010/analysis.json) and
[phase plots](../ztf-240023401-contaminants-20261010/fixed-phase.png).

Neighbor Tmag16.1575, target Tmag11.8839: approximate full-throughput dilution
predicts3124ppm, sufficient to explain the~2000ppm TESS signal with partial
aperture throughput. Nearby much fainter sources and correlated errors remain;
the deep eclipsing neighbor plus off-target images provide strong contamination
evidence. No companion mass or definitive binary type is inferred from depth alone.

No exact TIC match among221neighbor IDs in the dated TOI/confirmed/CTOI/EB,
Villanova/Kostov2025/DTARPS catalogs checked. This is not a novelty claim and does
not rule out other catalog aliases. Catalog and raw-data URL/SHA provenance saved.
