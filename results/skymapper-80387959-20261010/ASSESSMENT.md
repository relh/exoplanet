# TIC80387959: SkyMapper photometry leaves host unresolved

No independent transit confirmation or contaminant exclusion from these data.
The public25arcsec DR4 cone returned137detections belonging to5objects on61images;
all queries report OK without overflow, image/object IDs match exactly, and filters
agree across the detection/image tables. Source hashes and schema metadata retained.

SkyMapper411683748 matches TIC80387959 within1.00arcsec;411683753 matches neighbor
80387965 within0.16arcsec. Fixed catalog coordinates were not proper-motion
propagated. The closest faint alternatives80387961 and937808821 were not returned
as separate master sources; absence does not exclude their eclipse contamination.

Image metadata gives MJD at exposure start. We add half exposure and convert UTC
to geocentric BJD TDB (neglected topocentric correction<=0.022s). Prediction uses
only the existing TESS frozen4.19216872d ephemeris, period/epoch profile and stated
heuristic epoch floor. No ground-based phase or period optimization. The profile
is conditional, not a calibrated timing-confidence region.

Strict selection requires flags0/nimaflags0/image-quality<=2; a recorded relaxed
check uses flags<4/nimaflags<5/image-quality<=2. Both require finite positive PSF
uncertainty. Target has22strict/37relaxed measurements, neighbor16strict/52relaxed.
Target observations near one2015predicted event lie at its edge and are not inside
all allowed profile windows. Neighbor80387965 has four relaxed in-event measurements
(u,v,i,z; onlyu/vstrict), all during a different2021event. No repeated eclipse test.

Relaxed per-filter differences from other-night baselines (formal errors only):

| Source | u | v | g | r | i | z |
|---|---|---|---|---|---|---|
| Target | +0.014±0.013 | +0.031±0.004 | +0.011±0.005 | +0.014±0.005 | +0.001±0.004 | −0.020±0.006 |
| Neighbor80387965 | +0.063±0.034 | +0.053±0.029 | no in-event point | no in-event point | +0.009±0.012 | −0.001±0.020 |

Values are magnitudes, one in-event exposure per populated cell. The apparently
large target v offset is a single non-repeated, timing-edge observation with no
simultaneous reference-star calibration; it is not evidence for the shallow TESS
planet hypothesis. Do not combine colors into a formal detection. PSF errors omit
calibration/blending systematics, and baselines span other nights. The neighbor's
~percent-level expected diluted-eclipse explanation remains compatible with these
uncertainties. Close unresolved alternatives remain untested.

analysis.json retains every detection, flags, barycentric time and coverage window;
comparisons.json retains strict/relaxed per-filter comparisons and profile-window
checks. Original TESS positives and source-attribution failures remain unchanged.
Documentation: https://skymapper.anu.edu.au/how-to-access/ and
https://skymapper.anu.edu.au/data-release/dr4/; table descriptions are archived in
schema.json and images/master-schema.json.46existing pipeline tests pass; new
input/derived-row integrity checks in checks.json do not validate astrophysics.
