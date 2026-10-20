# Two exact-source literature leads checked: no new validation

Following actual bibliographic matches resolves two potentially misleading leads. TIC 469309982 appears in an open-cluster study but its row has zero reported Platais 8 membership probability. TIC 96166003 appears in a TESS planet-yield paper because that paper simulated a planet around the catalog star. Neither entry supplies a cluster age or observed planet. Both internal signals remain unresolved.

## TIC 469309982: the cluster reference does not establish membership

SIMBAD's exact Gaia DR3 query identifies **HD 300413** and directly joins TIC 469309982, 2MASS J09552355-5641092, TYC 8606-1845-1, Gaia DR2/DR3 5259582389096040960 and Gaia DR1 **5259582384786570368**. The release distinction matters: the open-cluster table uses DR1, whose identifier differs.

The specific reference, Cantat-Gaudin et al. 2018, [Characterising open clusters in the solar neighbourhood with the Tycho-Gaia Astrometric Solution](https://www.aanda.org/articles/aa/abs/2018/07/aa31251-17/aa31251-17.html), leads to the [actual membership table documentation](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/A+A/615/A49?format=html&tex=true). An exact DR1 query returns one row, independently corroborated by its Tycho identifier:

| Field | Value |
|---|---|
| Cluster considered | Platais_8 |
| Pfinal | 0.00 |
| Astrometry used | TGAS (T) |
| DR1 parallax | 13.38 ± 0.49 mas |
| DR1 proper motion RA/Dec | −46.182 / +41.011 mas/yr |

This is a positive identification of a **tested field star**, not an accepted cluster member. Pfinal is the paper's cluster-membership quantity, not planet probability. The value does not reject all possible associations, but prevents importing a Platais 8 age as a stellar prior from this reference. The target's RAJ2015/DEJ2015 and Tycho fields were used; the table also contains derived `_RA_icrs`/`_DE_icrs` fields inconsistent with the listed target coordinates, which are retained and not used to override the exact identifiers.

The other SIMBAD references concern the Henry Draper extension, stellar diameter/flux catalogs and Gaia's nearby-star census. Their presence is not an independent orbital or high-resolution companion measurement. No new source-resolved secondary, orbit or rotation measurement emerged from exact-ID/alias web searches. Previously measured season-dependent half-phase structure and uncertain later timing remain the relevant signal limitations.

## TIC 96166003: simulated planet is not a known observed planet

The exact Gaia DR3 query identifies **HD 282445**, joining TIC 96166003, 2MASS J04502136+3342255, TYC 2391-1304-1, Gaia DR2/DR3 161856980718462208 and Gaia DR1 **161856976421129472**.

Its reference to Barclay, Pepper and Quintana 2018, [A Revised Exoplanet Yield from TESS](https://doi.org/10.3847/1538-4365/aae3e9), is followed to [table 2 documentation](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJS/239/2?format=html&tex=true) and the exact TIC row. That table explicitly describes simulated detections. The row has **Perp = 15.592607 days**, versus the approximately 0.955-day internal signal. It is not observational evidence for a planet, competing ephemeris or prior discovery. Its synthetic detection/SNR fields must not enter candidate likelihood calculations.

The second specific lead, the [low-extinction TGAS HR catalog](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FA%2BA%2F609%2FA116), returns the exact DR1 ID and exact 2MASS designation. It gives **E(B−V)max = 0.0103**, DR1 parallax 8.683493 ± 0.227108 mas, and catalog photometry. The upper-extinction field supports the scope of that catalog's low-reddening selection; it is not a measured age, rotation period, spectrum or binary exclusion. No host mass/radius was recomputed from these older catalog entries.

These table matches add concrete context rather than generic catalog nonmatches, but they do not settle the disagreement between the two pre-sector-59 clocks. The prior source ambiguity, weak recurrence and processing/clock comparison remain unchanged.

## Scope, retained limitations and reproducibility

This bounded extension followed the two target-specific literature leads most likely to change interpretation: cluster membership and an apparent planet-paper association. Exact Gaia, TIC, 2MASS and Tycho searches surfaced no additional securely matched spectroscopy, high-resolution imaging or rotation result. This is not an exhaustive absence claim. The remaining listed references were classified by their documented catalog purpose; no unsupported binary/age inference was drawn from their inclusion.

`query.py` preserves six SIMBAD identity/alias/bibliography responses; `follow.py` saves the two primary supplementary-table ReadMes and cluster table discovery response; `tables.py` saves the three exact-source table rows. Their manifests retain final request URLs and SHA-256 hashes for all **12 successful responses** in isolated ignored data storage. No network/query failures occurred in this bounded pass.

[verify.py](verify.py) independently checks all hashes and CSV records, validates the release-specific Gaia identities against exact SIMBAD aliases and existing TIC records, reconciles target positions, verifies the independent Tycho/2MASS links, and checks the cluster probability, simulated-period field and documentation scope. [verification.json](verification.json) passes. Verification establishes provenance and interpretation of the returned rows, not catalog completeness or astrophysical confirmation.

No new epoch flux, light curve, image or spectrum was opened. No new clock search or fit was made. No shared scientific source, cache, documentation or external submission was changed. No candidate probability or status upgrade is justified by this extension.
