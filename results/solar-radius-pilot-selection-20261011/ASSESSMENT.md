# Solar-radius pilot selection

Of16,581 metadata opportunities,408 match saved TOI/confirmed/CTOI/archived-EB
TIC identifiers,1,635 fail the contamination<=0.2 or available-value requirement,
and7,534 lack an adjacent pair of early sectors. The remaining7,004 are ranked
by the existing radius/brightness/training-sector-count noise proxy. The first16
form the pilot. All counts and input hashes were verified.

Discovery uses the earliest available contiguous group of two or three sectors
<=55. Each target's latest ordinary sector56–107 is reserved. All selected
reserved light-curve files were absent before discovery and at verification.
Sector metadata is provisional; the loader checks FITS identity, checksum and
actual usable baseline. No temperature cut is imposed on this expanded-radius pool.

The catalogs are cached snapshots, not refreshed or exhaustive novelty checks.
Exact TIC exclusions miss alternative identifiers and blends. The local cached
Villanova file inspected during preparation contained HTML, so it was not treated
as a valid current EB catalog. Signals require positional/VSX and source checks
before being considered new candidates.

The pilot runs the existing campaign search and its unchanged screening gates.
Strong peaks with flags are not candidates. Recovery controls remain necessary
before broader expansion; the ranked bright pilot is not representative survey
completeness. `plan.json`, catalog hashes, excluded IDs, complete eligibility and
frozen selection are retained. No photometry outcomes influenced this ranking.
