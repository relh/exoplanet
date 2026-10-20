# TIC 164293311: known eclipsing-binary contamination

The 0.991009-day Sector 100 screening signal is strongly attributable to
neighbor TIC 164299149, already classified as an eclipsing binary in Gaia DR3.
It is not a new planet candidate around TIC 164293311.

The frozen native-cadence measurement is 2573 ± 253 ppm with 12 supported
events. Reserved Sectors 10/11 give negative fixed-phase measurements, but
4.57/4.52-day propagated timing spreads make those checks inconclusive.
The same-epoch TESS-SPOC request returned HTTP 404, not a nondetection.

Sector 100 difference imaging gives a compact positive feature 2.951 pixels
from the target, only 0.072 pixels from TIC 164299149. Sector 99, opened
subsequently without changing the ephemeris, repeats this: 3.012 pixels from
the target and 0.059 pixels from the neighbor. Both images were inspected.
There are 26/20 contributing pixel windows and formal peak SNRs 217.5/199.1.
These are post-selection moments, not calibrated PRF confidence intervals;
catalog positions were not propagated for proper motion.

The archived Gaia DR2-to-DR3 neighborhood query maps the neighbor to DR3
6079630390520064896. The Gaia classifier labels it ECL, and the eclipsing-binary
table gives frequency 1.0095070388859295 per day, or period 0.990582494 days.
This differs from the TESS fit by 0.000426586 days. Its catalog model has primary
and secondary depths 0.803/0.096 mag. Spatial agreement in two sectors and the
matching catalog period strongly support known binary contamination. No
Gaia-to-TESS epoch/phase comparison was performed; the classifier score is not
a calibrated posterior probability for this source attribution.

The nine earlier dated catalog tables had no exact-TIC matches among the 515
cone sources; that limited non-match was superseded by the positive Gaia EB
identity. Exact-name QLP/SPOC neighbor availability returned no observations,
which does not negate the catalog classification.

Evidence: [Sector 100 pixels](../../tesscut-164293311-s100-20261010/analysis.json),
[Sector 99 pixels](../../tesscut-164293311-s99-20261010/analysis.json),
[Gaia period comparison](../../gaia-164293311-neighbor-20261010/period-comparison.json),
[reduction checks](../../qlp-faint-164293311-reduction-20261010/),
and this directory's frozen, held-out, secondary, and discovery artifacts.
Raw sources and SHA-256 hashes are retained in the corresponding manifests.
