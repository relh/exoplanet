# Complete remaining-pool metadata audit and frozen5,619-star selection

All111 bounded MAST queries for the remaining27,549 targets completed without
errors (process exit0). The original untouched pool had29,549 stars; its first
2,000 were already queried in the earlier phase. Of these remaining targets,
26,621 have QLP products and5,619 satisfy the adjacent-training-pair plus
separate-reserved-epoch rule. The other21,930 do not satisfy that rule; they are
not photometric non-detections and could support other search designs.

`select.py` verifies every expected query offset, raw response hash and returned
row count. `selected.json` freezes all viable targets, not another ranked subset,
before opening their photometry. Exact TIC IDs are disjoint from the original
11,851, late-sector1,322 and earlier QLP288 selections. Earliest qualifying
adjacent sectors are training; sectors at least eight sector numbers away are
reserved. Timing independence and predictability must be checked with actual
timestamps during follow-up.

The full5,619-target campaign is in `../campaign-qlp-full-pool-20261010`, with
source/dependency snapshots and8 workers. Published uncertainties are retained
where usable. Based on the separately completed recovery campaign, sectors with
no usable uncertainty pairs may use the existing robust adjacent-difference
estimate; each such sector is explicitly labeled. Entirely missing flux remains
an error. These estimates are not calibrated red-noise errors or significance.

Current free disk space and a conservative estimate using the largest cached QLP
file were recorded before launch:~174GB available versus~16.4GB for two files
per selected target at that observed maximum size. This is an estimate, not a
storage guarantee. No archival agent/session data were altered.

This is coverage of a specific small, nearby, cool, low-crowding TIC sample with
dated known-catalog exclusions. It is not all TESS targets, a completeness survey,
or evidence that other researchers have not investigated these stars. Preserve
weak, failed and inconclusive results; review priorities are not planet candidates.
