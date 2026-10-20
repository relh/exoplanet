# No matching public ESO spectrum product in the bounded search

The ESO public processed-product ObsCore query returns no spectrum within 120 arcsec of any of the three top targets: TIC 80387959, TIC 402358350 and TIC 241928959. All three requests succeed with valid schemas and QUERY_STATUS=OK. This identifies an unavailable follow-up route in this snapshot; it does **not** exclude a stellar companion or prove that no spectra exist in other archives, raw collections or private programs.

The centers use the exact Gaia DR3 target identities from the [companion audit](../companion-constraints-shortlist-20261012/ASSESSMENT.md). The cone deliberately includes nearby sources and reasonable proper-motion displacement, but is not a full epoch-propagated matching algorithm. Any returned observation would have required association checks before scientific use. None was returned, and no spectrum or velocity series was opened.

## Independent archive-index check

A previously downloaded HARPS RVBank index contains 5,105 parsable target entries. None lies within the same 120-arcsec cones. Nearest entries are 1,481, 7,968 and 7,988 arcsec away respectively, far outside the selection radius. All index coordinates parse successfully. This check uses the explicitly dated local snapshot, not a new live inventory; original retrieval provenance and SHA-256 are retained in [rvbank.json](rvbank.json). The web viewer rejected the live index because it exceeded its response-size limit. That access failure is not an astronomical nonmatch.

The index is a particular published RV collection, not every HARPS observation or every form of spectroscopy. In particular, the separately investigated RAVE record for TIC 80387959 is unaffected by these ESO/RVBank nonmatches.

## Sources and verification

The query follows the [official ESO TAP examples](https://archive.eso.org/tap_obs/examples), using `dataproduct_type='spectrum'` and a positional cone in `ivoa.ObsCore`. The documentation response and its hash are preserved. [queries.json](queries.json) records the full ADQL, response URLs, timestamps, raw hashes, columns, status and empty rows; raw responses are in ignored `data/web-spectroscopy-20261012/`. [plan.json](plan.json) predates requests and hashes the identity inputs.

The [HARPS RVBank index](https://exo-restart.com/wp-content/uploads/Stellar_parameters/HARPS_RVBank.html) was already cached with original provenance; no velocity samples from its downloadable series were accessed. `rvbank.py` records all nearest-distance checks and parse failures (none).

`verify.py` checks hashes and ESO XML status/schema/row counts, reparses the index, and independently computes sexagesimal coordinates and haversine distances for all 5,105 entries. Its scope is metadata and arithmetic, not archive completeness or physical validation. No candidate disposition changes follow from this report.
