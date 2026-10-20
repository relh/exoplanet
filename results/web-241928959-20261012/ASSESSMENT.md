# TIC 241928959: no new discriminating literature evidence found

This bounded web and primary-catalog investigation finds no newly linked spectroscopy, high-resolution companion measurement, rotation period or secure young-association membership. It does not improve the planet interpretation or rule out multiplicity. The existing RUWE/IPD flags, tentative SPYGLASS I youth and grazing/density ambiguity remain unchanged; they are not presented as new discoveries.

## Identity and new catalog checks

The existing exact TIC record links Gaia DR2 6865254022910168320, 2MASS 19515688-2130112, AllWISE J195156.87-213011.2 and UCAC4 343-196048. The previous verified Gaia neighborhood mapping preserves the same numerical DR3 source identifier. SIMBAD at the previously established exact object identifier 30823552 now returns only the Gaia DR3 identifier and one bibliography entry: **2021ApJ...917...23K**, the already inspected SPYGLASS I paper. No new bibliography lead is present in this bounded SIMBAD lookup.

| New check | Actual result | Meaning and limitation |
|---|---|---|
| SPYGLASS IV young-association membership table 1, exact Gaia ID | Successful empty CSV | No membership corroboration from this table; not an age measurement or proof of being old. |
| SPYGLASS IV older-association table 4, exact Gaia ID | Successful empty CSV | No older-group membership corroboration; does not reject youth. |
| El-Badry et al. 2021 resolved-wide-binary catalog, either component exact Gaia ID | Successful empty CSV | No reported pair in this selected catalog; cannot exclude a close companion or poorly measured pair. |
| Washington Double Star catalog, 60-arcsec cone around exact TIC position | Successful empty CSV | No cataloged visual-double entry in this cone; no contrast curve or completeness guarantee. |

The [SPYGLASS IV documentation](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJ/954/134?format=html&tex=true) explicitly describes table 1 as candidate members of young associations and table 4 as candidate members of older associations. These are not a complete list of all isolated young stars. The previous SPYGLASS I model youth probability 0.40 and unassigned cluster fields remain the relevant positive catalog facts.

The [wide-binary study](https://arxiv.org/abs/2101.05282) concerns spatially resolved pairs. Its nonmatch has no direct power to veto an unresolved eclipsing companion at the TESS period. The [WDS description](https://www.astro.gsu.edu/wds/wds.html) establishes the scope as measured visual double and multiple stars. Absence here is not a multiplicity constraint with a known detection limit.

## Web search and stopping point

Exact-ID/alias searches used the Gaia ID, TIC number, full 2MASS designation, AllWISE designation, UCAC identifier and coordinate fragments. No relevant new exact-source primary paper was surfaced; abbreviated numeric searches returned unrelated pages, which were not treated as stellar evidence. Search-engine absence is not bibliographic completeness. The only specific followable scientific lead was the newer SPYGLASS catalog, checked through its actual supplementary tables above.

No high-resolution contrast curves, phase-resolved spectroscopy, lithium measurement or externally measured rotation period could be securely linked in this bounded pass. Consequently no new physical inference, mass constraint, planet probability or candidate upgrade is justified. This report does not claim all archives have been exhausted. A source-identified contrast curve or spectroscopic orbit would be qualitatively different evidence; additional generic nonmatches would not supply it.

## Provenance and verification

Four query scripts preserve all 12 raw metadata responses under isolated `data/web-241928959-20261012/`; the four `queries*.json` manifests record final URLs, HTTP status and SHA-256. The initial SIMBAD bibliography query used the wrong column and returned HTTP 400; the corrected reference-table join succeeds. The first WDS cone used absent coordinate names and returned HTTP 400; the retained schema query supplied RAJ2000/DEJ2000 for the successful recovery. Neither error was interpreted as a nonmatch. A local quoting syntax error in preparation of `query-final.py` occurred before network execution and was corrected; it changed no scientific response.

[verify.py](verify.py) independently hashes and parses all responses, checks errors, reconciles exact TIC aliases, verifies exact-ID predicates including both binary components, checks the WDS cone, and confirms the returned schemas and row counts. [verification.json](verification.json) passes. These are identity/arithmetic/provenance checks, not a claim of catalog completeness.

No new photometry, TESS observations, telescope images or spectra were opened. No shared source, docs or cache was changed and no external candidate submission occurred.
