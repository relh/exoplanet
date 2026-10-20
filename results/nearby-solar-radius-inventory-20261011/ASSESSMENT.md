# Expanded nearby-star inventory

A complete TIC query returns27,033 stars with catalog radii0.81–1.10solar,
T magnitudes6–12 and distances0–120pc. This extends beyond the earlier
small/midradius pool. Stellar catalog estimates are selection metadata,
not newly inferred physical parameters.

Cross-matching the existing TESS-SPOC sector inventory yields16,581 opportunities
with at least one ordinary sector<=55 and another in56–107. Initial filtering
removes one previously used identifier,98 duplicate/disposition-flagged entries,
2,221 entries with no cached coverage and8,132 without the required epoch split.
All counts reconcile to the full catalog. No light curve was opened here.

Each opportunity records the earliest discovery sector and latest reserved sector
in those ranges. These are provisional metadata choices: product availability,
actual observing dates and useful duration must be checked before a pilot search.
Sector numbers alone are not independent-epoch validation. Known-object catalog
screening and contamination cuts are still outstanding; the list includes stars
that may already host reported planets or variables. Brightness sorting is not
a claim that these are globally underexplored targets.

Local reuse screening considers target-result filenames and QLP/SPOC light-curve
cache filenames. It is not an exhaustive audit of every historical artifact.
The complete excluded-ID set is retained for reproducibility. The cached sector
inventory is not a refreshed query of all current TESS products.

`request.json` and `source.json` preserve the MAST query and downloaded-data hash.
`selection.json` records filtering counts, cache exclusions and input hashes;
`opportunities.json` retains all provisional opportunities. `verify.py` checks
query completeness, unique IDs, the count partition, exact catalog rows and both
sector assignments for all16,581 entries. No search algorithm changed.

Next: apply known-object and contamination screening to a manageable pilot,
verify its product identities and freeze discovery/reserved choices before
photometric screening. The larger stellar radii reduce Earth-size transit depths;
recovery controls must characterize sensitivity rather than assume it.
