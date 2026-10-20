# Sector 49 exploratory search: no qualifying signal

All 339 selected targets were attempted. Original QLP results: 310 below screening
threshold, 20 flagged, nine data failures. Neither the original follow-up policy
nor the two-supported-event diagnostic policy admitted a peak.

All nine failures have zero usable positive quality-zero QLP flux and no valid
published uncertainties. Raw file integrity, counts, URLs and hashes are retained
in the recovery plans. Same-epoch SPOC recovered TIC 393819644; it was below
threshold (top formal SNR 4.58, no screened peaks). The other eight SPOC requests
returned HTTP 404. Thus 331 distinct targets have usable searches and eight remain
unsearched because of data availability. Reserved sectors for all nine were kept
unopened. A missing product is not a nondetection.

| Failed QLP TIC | Reserved sector | Same-sector SPOC |
|---|---:|---|
| 312832581 | 22 | HTTP 404 |
| 202376290 | 22 | HTTP 404 |
| 332250577 | 76 | HTTP 404 |
| 393819644 | 22 | Usable, below threshold |
| 383397703 | 22 | HTTP 404 |
| 137004801 | 22 | HTTP 404 |
| 3800967 | 22 | HTTP 404 |
| 284569410 | 76 | HTTP 404 |
| 376504254 | 76 | HTTP 404 |

The reconciliation verifies target/source hashes, all nine error audits, recovered
SPOC raw hash, unconsumed reserved epochs, and empty terminal follow-up inventories.
See [recovery records](../qlp-faint-one-reserved-sector49-recovery-20261010/).

Controls on the first three frozen targets (3814454, 156941650, 458446492)
used 12 short-period and 12 longer-period injections; all 24 are within the actual
search grids, with exact baseline-array agreement for both detrending windows.
Short controls: eight period/phase recoveries, five screening passes.
Long controls: twelve period/phase recoveries, four screening passes.
All nine passes have phase recovery; none is an Earth-radius trial.
The successful longer-period trials are at 5.73 d; none at 8.37 d passes.
This selected, small control sample is not a completeness estimate. The lack of
a qualifying signal cannot rule out planets.

Metadata-only inventory excluding the complete frozen Sector 49 selection leaves
2729 unused stars in the scoped pool. Its generated policy prose inherited the
previous sector list, but the actual prior-selection list and hashes include the
whole Sector 49 selection. The next frozen selection is Sector 54 with 308
untouched targets; no corresponding photometry was opened.
