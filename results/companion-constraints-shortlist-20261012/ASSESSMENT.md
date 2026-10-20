# Shortlist companion metadata: no Gaia orbit, one important astrometric concern

The six exact target stars have no returned Gaia DR3 non-single-star solutions in the four queried NSS tables. None passes Gaia's suggested combined radial-velocity variability selection; TIC241928959 lacks the required statistics and TIC402358350 has only five RV transits. These are limited catalog constraints, **not binary exclusions or evidence of planetary mass**.

The useful interpretation is that TIC241928959 retains a specific multiplicity/blend concern: RUWE3.356 and14% double-peak image windows. TIC402358350 carries a catalog duplication/processing flag. Neither finding identifies the source of the TESS dips or establishes a companion. Current candidate dispositions need no upgrade.

## Exact identities and scope

Existing TIC catalog records supply the DR2 identifiers. All six return one DR2-neighborhood relationship each, with unchanged DR3 numeric IDs. Exact joins, not rounded coordinates, determine the source rows. All mappings and their distances are retained in [mapping.json](mapping.json); [summary.json](summary.json) links each original TIC record and hash.

| TIC | Exact Gaia DR3 source_id |
|---|---|
|80387959|5362389543781401216|
|402358350|4318715445843296256|
|241928959|6865254022910168320|
|469309982|5259582389096040960|
|96166003|161856980718462208|
|5546257|5426593115802740992|

This audit concerns the named target stars, not their contaminating neighbors. In particular, TIC5546257's quiet target metadata do not negate the separate known-eclipsing-neighbor evidence.

## Per-target measurements

All six have `non_single_star=0`; all four exact-source queries—`nss_two_body_orbit`, `nss_acceleration_astro`, `nss_non_linear_spectro`, `nss_vim_fl`—returned successful, schema-valid empty tables. No orbital period, mass or companion solution is available from this bounded query.

| TIC | RUWE | IPD multiple-peak windows | Duplicated source | RV transits / deblended | Constancy p / renormalised GOF | Robust RV range(km/s) | Practical change |
|---|---|---|---|---|---|---|---|
|80387959|0.828|0%|false|26 /10|0.1788 /0.444|5.955|No RV flag under the combined rule; host ambiguity remains.|
|402358350|1.000|0%|true|5 /3|0.1523 /0.796|3.620|Processing/association caution; too few RV transits for recommended selection.|
|241928959|3.356|14%|false|21 /9|unavailable /unavailable|unavailable|Astrometric/multiple-image concern reinforces uncertain single-star interpretation; no RV constancy assessment.|
|469309982|0.978|0%|false|13 /3|0.02609 /1.220|2.028|No combined RV flag; does not resolve timing/source uncertainties.|
|96166003|0.983|0%|false|24 /3|0.01347 /1.732|5.186|No combined RV flag; robust range alone is not an orbital amplitude.|
|5546257|0.913|0%|false|26 /11|0.1137 /0.744|2.653|No target RV flag; known-neighbor contamination remains the primary concern.|

The RV summaries span576–998days across the sample but supply no phase-resolved comparison with the TESS clocks. No epoch RV or photometry was downloaded.

TIC241928959 uses RV method2, has GRVS12.0188, and lacks the bright-star variability indices. Its median RV uncertainty5.236km/s is not evidence of velocity variation. Its astrometric excess noise is0.430mas with catalog significance124.36; RUWE and excess noise are related fit diagnostics, not independent companion detections. The known separate TIC241928961 lies10.5567arcsec away (roughly0.5TESS pixel). The present data do not show that this particular neighbor causes the Gaia double peaks or elevated residuals, nor identify an additional bound source. Avoid counting Gaia flags, known neighbor presence and poor single-star assumptions as three independent binary confirmations.

## What is newly established

This is primarily a **new interpretation and explicit audit of existing Gaia metadata**, not new Gaia observations. All22 selected source fields for80387959,402358350,241928959 and5546257 exactly match the earlier source snapshots; those prior hashes and matching fields are recorded. The earlier [241 source assessment](../prf-241928959-s92-20261011/ASSESSMENT.md) already mentioned elevated RUWE. This audit makes its14% IPD multiple-peak fraction and unavailable RV variability statistics explicit and checks the actual NSS tables. It adds an exact mapping and consistent metadata assessment for469309982/96166003 within this scope.

The new NSS nonmatches do not provide a completeness model. No calibrated binary probability, mass constraint or planet likelihood follows. For241, single-star stellar parameters used in the conditional transit fit remain questionable. For402, the duplicate-source flag deserves association/model caution, not a binary label. No other target obtains a stronger physical classification from these data.

## Official interpretation used

Gaia recommends the combined RV selection p<0.01, renormalised GOF>4 and at least10 transits. Missing indices cannot be treated as passing a constancy test. The robust RV range is an outlier-filtered maximum-minus-minimum, not a fitted orbital semiamplitude. IPD multiple peaks may indicate visual doubles; they do not establish a bound binary. `duplicated_source` reflects identifier consolidation and possible processing, matching or multiplicity issues. NSS flags describe available model categories. See the [official Gaia DR3 source documentation](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html); the raw page and its hash are preserved in [documentation.json](documentation.json).

## Failures, reproducibility and limits

The first official `TAP_SCHEMA.tables` query failed with HTTP500 and an internal SQL missing-FROM-clause error. Its raw response and [error record](nss-schema.json) are retained. A separately recorded [recovery plan](recovery-plan.json) used `TAP_SCHEMA.columns` once; that route succeeded and established the four table/source schemas before the bounded exact-ID requests. No failed response was interpreted as an empty scientific result. A guessed documentation-directory URL also failed in the web viewer; the directly linked main-source documentation succeeded and supplies the interpretation used here.

All raw responses are under isolated ignored `data/companion-constraints-shortlist-20261012/`, with URLs, retrieval timestamps, hashes, request schemas and errors in this directory. [verify.py](verify.py) reconciles ten raw records, six TIC/DR2/DR3 joins, all four empty NSS schemas, prior-snapshot equality and an independent Decimal calculation of the RV selection/deblended fractions and integer NSS bits. It verifies arithmetic and identity, not astrophysical accuracy or catalog completeness.

Run `uv run python results/companion-constraints-shortlist-20261012/verify.py`; [verification.json](verification.json) reports passed. No shared source, docs, caches, observations or external submissions were modified by this audit.
