# SIMBAD identity and bibliography audit

Successful60-arcsec cone searches each return one source, identified by the exact
previously verified Gaia DR3 identifier. No new planet candidate is established.

| TIC | SIMBAD identity | Type | Linked reference |
|---|---|---|---|
| 241928959 | Gaia DR3 6865254022910168320 | `*` | SPYGLASS I (2021) |
| 422626648 | Gaia DR3 6254811248843788416 | `PM*` | Gaia Catalogue of Nearby Stars (2021) |

Each source has one bibliography record, and the identifiers table supplies only
its Gaia DR3 name. These sparse entries do not establish novelty or exclude
binaries, blends, stellar activity or unindexed literature.

For TIC241928959 the reference is
[SPYGLASS I](https://doi.org/10.3847/1538-4357/ac0251), a study selecting candidate
young stars. **The bibliography link is not a verified youth, membership or age
measurement for this target.** Its actual catalog row and selection flags should
be retrieved before adopting a young-star interpretation or revising the radius.
This is the next substantive literature lead.

For TIC422626648 the reference is the
[Gaia Catalogue of Nearby Stars](https://doi.org/10.1051/0004-6361/202039498).
That association does not resolve the existing RV variability/binary concern.

`results.json` and `references.json` preserve exact ADQL requests, URLs, raw-data
paths, hashes and parsed responses. All four raw hashes and CSV parses were
verified; Gaia identities and bibliography row counts match. No cone reached its
100-row cap. `verification.json` records those checks. No transit-search algorithm
changed, and no new photometry was opened in this audit.
