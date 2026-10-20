# No matching ESO raw pointings within the bounded cones

The anonymous ESO raw-observation table returns **zero records within 120 arcsec** of each target's retained Gaia DR3 position. Both requests completed with HTTP 200, `QUERY_STATUS=OK`, the expected 26-column schema, and no overflow. No new spectrum, image or flux was opened; both signals remain unresolved.

| Target | Gaia DR3 identity | Cone center (degrees) | Raw records |
|---|---|---|---:|
| TIC 80387959 | 5362389543781401216 | 165.31057513947022, −48.613881428659525 | 0 |
| TIC 402358350 | 4318715445843296256 | 295.15092862046833, +15.640411694115707 | 0 |

This checks `dbo.raw`, independently of the earlier [processed-spectrum search](../web-spectroscopy-20261012/ASSESSMENT.md). All instruments, observation categories and dates were eligible; the query imposed no science-only, spectral-only or release-date cut. It supplies no newly identified data for source attribution, binary constraints or ephemeris recovery.

The [official ESO documentation](https://archive.eso.org/cms/eso-data/programmatic-access.html) distinguishes raw and processed metadata. The retained live `TAP_SCHEMA.columns` response specifically states that raw `s_region` contains a position and that observation footprints are unavailable. Consequently this is **not** a census of wide-field images covering either star. Distant pointings might include a star on an image or multiobject field; this query cannot establish that coverage. Likewise, a positional hit would not by itself establish entry into a spectroscopic slit or fiber. Nonpublic metadata are outside the anonymous search. The Gaia J2016 coordinates were not epoch-propagated; the 120-arcsec radius is deliberately broad. ESO describes its raw coordinates as FK5 J2000; the small reference-frame difference is negligible at this search radius but this is not a precision crossmatch.

A separately frozen, post-result positive control used the SN 1987A coordinates in the [official TAP examples](https://archive.eso.org/tap_obs/examples). The identical raw-table cone predicate and selected columns returned three records (`TOP 3` deliberately bounds the control). This demonstrates that the service and predicate can return observations; it does not demonstrate completeness or improve the candidates' planetary likelihoods.

## Reproducibility and limits

[plan.json](plan.json) freezes scope and exact identity input before metadata access. [target-plan.json](target-plan.json) freezes exact ADQL and selected columns after schema discovery and before target queries. [requests.json](requests.json), [targets.json](targets.json) and [control.json](control.json) retain response URLs, UTC timestamps, status, schemas and SHA-256 hashes. Raw responses are isolated in ignored `data/eso-raw-metadata-20261013/`. The control amendment is [control-plan.json](control-plan.json).

Run `uv run python results/eso-raw-metadata-20261013/verify.py` for independent offline XML, query reconstruction, identity and provenance checks. [verification.json](verification.json) reports 52 checks passed. These verify the bounded metadata result, not the archive's completeness or an astrophysical classification. No shared scientific source, candidate clocks, thresholds or classification changed.
