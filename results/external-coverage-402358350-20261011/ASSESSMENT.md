# TIC402358350: no secure target light curve in the checked ZTF/Gaia routes

The public metadata checked here do not provide a securely associated independent target light curve for a fixed-ephemeris transit test. **No external flux was downloaded or measured.** This is a coverage/association limitation, not a transit non-detection and not evidence against the TESS signal.

| Survey route | Result | Consequence |
|---|---|---|
| ZTF DR24 object catalog,15arcsec cone |49 records; no record within3arcsec of the proper-motion-propagated target over2018–2027|Nearby records cannot be treated as target photometry.|
| Gaia DR3 target source |`has_epoch_photometry=false`, `phot_variable_flag=NOT_AVAILABLE`|No public DR3 target epoch-photometry series is identified by this flag.|
| Gaia selected comparison sources |Only the known48arcsec pulsating neighbor has epoch photometry|Its observations would not independently confirm the target transit.|

## ZTF association audit

The metadata query succeeded, returned49 rows below the1000-row limit, and preserves every source/filter record, including those with zero good observations. A15arcsec cone was used to inspect close blends rather than silently choose the nearest source.

The nearest object to the original unpropagated TIC position is6.342arcsec away, with a single listed observation and median magnitude18.439. Gaia gives the target G=9.828. Those different bands should not be directly equated, but neither the offset nor the much fainter catalog entry supports assigning it to the bright target.

The exact target Gaia DR3 source4318715445843296256 has reference epoch2016.0, pmRA63.134mas/year and pmDec25.562mas/year. Propagating its position on a0.01-year grid across2018–2027 leaves every ZTF catalog record outside3arcsec. The closest possible approach on that grid is5.118arcsec for object1587112400163948 at the2027 endpoint; that record lists zero observations. The interval deliberately brackets possible current survey epochs; it is not a claim that any measurement occurred in2027. Linear motion omits parallax and does not establish absolute crossmatch accuracy. No light-curve timestamps were opened.

The49 records include neighboring faint sources and potentially problematic detections around a bright star. Nearest matches to the limited previously selected Gaia scene are retained as context, not accepted identities. We did not assert that every ZTF record is a real separate star, that any particular image competitor is excluded, or that forced photometry and other releases lack exposures.

## Gaia and prior access lessons

The existing exact-identity Gaia source query was retrieved on2026-10-11 at23:40:33UTC, shortly before this investigation. Its raw CSV, source hash, selected records and target availability flag were rechecked here. Reusing that recent evidence avoids a redundant identical query. False/NOT_AVAILABLE means public catalog information is unavailable, not that the target is photometrically constant. The earlier [Gaia scene review](../gaia-402358350-scene-20261011/ASSESSMENT.md) retains the complete identity and close-blend qualifications.

Previous investigations repeatedly timed out at the direct IRSA light-curve service, while the documented cloud route succeeded. We therefore queried object metadata first rather than repeating known failing flux requests. If a secure target association becomes available, [IRSA's HATS workflow](https://caltech-ipac.github.io/irsa-tutorials/ztf-lightcurves/) supports indexed object-ID retrieval; the [light-curve API documentation](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_lightcurve_api.html) describes the alternative endpoint. No cloud light curves were requested because this query supplied no secure target-associated ID.

The earlier ASAS-SN work checked a variable-star compilation, not complete epoch coverage. Its nonmatches must not be reused as evidence that this target lacks observations. This run did not query or establish ASAS-SN epoch availability.

## Frozen measurement policy and verification

`plan.json` was saved before external metadata retrieval and before any external flux access. It copies the unchanged expanded primary clock (period11.769544332days, duration0.144day) and all saved timing-profile information. Had usable flux been found, only that fixed prediction would have been measured, retaining propagated timing uncertainty and both conditional HMJD-scale interpretations used by earlier work. No period, phase or profile-maximum search was authorized or performed. Because no target flux was obtained, there is no timing-recovery verdict or observational upper limit to report.

`ztf-metadata.json` preserves the exact query, raw CSV URL/time/hash, all49 records and truncation check. `results.json` retains each positional association diagnostic and the Gaia source inputs. `verify.py` reparses the CSV, checks source hashes and the frozen clock, independently recomputes all49 proper-motion separation tracks using spherical trigonometry, and reconstructs the Gaia source table/availability flags. All checks passed. Raw downloads use the exclusive ignored prefix `data/catalogs/external-coverage-402358350-20261011/`. No TESS data, shared scientific code or catalog state was changed.
