# ASAS-SN catalog check of the two remaining single-sector signals

Successful60-arcsec queries around TIC241928959 and TIC422626648 return no rows
in **II/366/catv2021**. Both responses have valid CSV headers; hashes, response
parses and the absence of rows were independently verified by `verify.py`.
Exact queries, URLs and raw-data hashes are in `results.json`.

This is a nonmatch in the [VizieR ASAS-SN variable-star compilation](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=II%2F366).
Its metadata describes the2021 version with a2024 database retrieval. It is not
a complete current search of every ASAS-SN measurement or unpublished signal.
No light curves were downloaded, and no observational upper limit follows.
ASAS-SN and VSX also share source material, so their nonmatches should not be
counted as independent statistical evidence for a planet.

Neither signal's status changes. TIC241928959 still lacks convincing independent
confirmation; TIC422626648 also retains substantial RV variability concerns.
The earlier EPIC identity check already removed TIC196681132 from new-planet
priority. Further catalog nonmatches alone would not justify upgrading either
remaining signal. Additional photometry or stronger source/shape diagnostics
are needed.
