# TIC402358350: public candidate checks find no listed match; novelty remains unproven

The current public ExoFOP responses contain no TOI, CTOI or planet-parameter entry for TIC402358350. This supports keeping the11.77-day signal as an unlisted lead within the checked sources, **not claiming it is undiscovered**. Its astrophysical and host uncertainties are unchanged.

| Check | Result | Scope |
|---|---|---|
| Fresh public CTOI CSV |5,138 rows; zero exact TIC matches; zero rows within120arcsec|All retrieved coordinates parsed successfully. No candidate period exists in these matching subsets to compare with11.77days.|
| ExoFOP target page |TOI0, CTOI0, planet parameters0; confirmed planets shown as N/A|Parsed the actual empty embedded table arrays, not a generic page-error or missing search snippet.|
| TESS EB catalog target page |Explicitly states the TIC is not in the catalog|A catalog nonmatch does not exclude an eclipsing binary.|
| SIMBAD exact-identity bibliography |Four linked references; none identifies a planet claim in the reviewed metadata|Indexed bibliography is incomplete and not a full-text/supplement search of all literature.|

The fresh CTOI CSV retrieved on2026-10-11 has the same SHA-256 as the saved2026-10-09 and earlier2026-10-11 snapshots. Retrieval time establishes when we received this public response; it does not establish the last scientific update, completeness or absence of unpublished/private submissions. The independently queried [ExoFOP target page](https://exofop.ipac.caltech.edu/tess/target.php?id=402358350) likewise shows no entries. Its [CTOI download endpoint](https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv) and raw response hashes are retained.

## Exact identity and literature context

The existing exact SIMBAD chain is TIC402358350 = HD353367 = Gaia DR3 4318715445843296256, with aliases TYC1602-2473-1 and2MASS J19403616+1538250. The [identity record](../review-402358350-20261011/identity.json) is the basis for the bibliography query, not a positional guess.

SIMBAD returns four linked bibcodes:1995A&AS..110..367N,2014ASPC..485..223B,2018A&A...609A.116R and2019MNRAS.490.3158C. Their metadata concern stellar positional/spectral catalogs, diameter catalogs and photometric calibration. The2018 [author paper](https://arxiv.org/abs/1710.05803) describes Gaia red-clump photometric calibration; the2019 [author paper](https://arxiv.org/abs/1910.00542) describes a compilation for infrared interferometry. Neither abstract is a transit discovery announcement. Bibliographic association with a population study does not by itself classify this particular star as a red giant or establish its binary status. This review does not replace target-level stellar characterization.

Exact-identifier web searches for the TIC, HD, Gaia, Tycho and2MASS names yielded no relevant indexed planet paper; irrelevant numerical/string matches were discarded. Restricted searches for the TIC/HD names on primary astronomy domains were also empty. These search failures are weak negative evidence because indexing and alias coverage are incomplete. No statement that all papers, supplementary tables or community reports have been searched is justified.

The [live TESS EB page](https://tessebs.villanova.edu/402358350) was successfully retrieved by direct HTTP and explicitly reports nonmembership. It was not inferred from an inaccessible page.

## Provenance, verification and access limits

`query.py` retains fresh ExoFOP and SIMBAD-schema requests; `references.py` records the exact-object bibliography; `eb_probe.py` and `literature_sources.py` preserve additional public responses. Raw files use the exclusive ignored prefix `data/catalogs/novelty-402358350-20261011/`. All responses have URLs, retrieval times and hashes in committed manifests. `queries.json` stores only matching CTOI rows and the full retrieved row count; the entire raw CSV is retained locally.

The web tool could not access the target ExoFOP page, EB page, DOI routes or the ADS2014 abstract. Direct HTTP succeeded for ExoFOP/EB, and author arXiv pages supplied the2018/2019 abstracts. These access failures are recorded in `web-search-notes.json`; they are not treated as evidence that a source is absent. The1995 and2014 full texts were not inspected. No login, submission, message or downloaded-code execution occurred.

`analyze.py` records exact matches, neighboring coordinates, target table sizes and old snapshot provenance. `verify.py` checks raw hashes, reparses all5,138 CTOI rows, recomputes the120arcsec neighborhood with independent spherical arithmetic, checks all three ExoFOP table counts and exact target identity, verifies four bibliography rows and the explicit EB nonmembership message. It validates the stated snapshot checks, not novelty or catalog completeness. No observations or scientific analysis algorithms changed.
