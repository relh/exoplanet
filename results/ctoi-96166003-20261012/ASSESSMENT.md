# TIC96166003: no match in the dated public CTOI snapshot

The5,138-row public ExoFOP CTOI snapshot retrieved2026-10-11T23:45:14UTC contains no exact TIC96166003 entry and no entry within120arcsec of its catalog position. The previously downloaded snapshot was reused without a new network request. This is a dated catalog nonmatch, not proof that the signal is undiscovered, planetary, or absent from other catalogs or unpublished work.

`results.json` preserves source URL, retrieval date, input/script hashes and matching rows. `check.py` parses every coordinate and independently checks Astropy separations against spherical haversine arithmetic. Target position comes from the hashed discovery record. Existing TOI/confirmed-table and SIMBAD checks remain in the discovery review; this report does not repeat or expand them into an exhaustive literature claim.
