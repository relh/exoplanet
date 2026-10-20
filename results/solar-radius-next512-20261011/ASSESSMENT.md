# Expanded solar-radius search: next512 complete

All512 targets in frozen eligible ranks336–847 completed:255 below the screening threshold,254 flagged,3 passing discovery screening,0 errors. The terminal audit verified all1,238 raw training product hashes and identities, exact selection membership and source ranking, and absence of all reserved-sector files before follow-up.

The original process exited143 after410 completed targets. `interruption.json` preserves that state and the102 unfinished identifiers. `resume.py` verified unchanged source/selection hashes and processed only missing targets; completed records were retained. The final run and ranking cover all512.

Passing signals: TIC423928109 is an exact match to a known ROT variable; TIC120689141 matches a published stellar rotation period. Both are removed from new-planet priority. TIC362222987 remains unresolved with competing aliases, a dominant event near background variation and timing uncertainty. Its dip is present in aperture and corrected flux, which share photons and do not provide independent confirmation. See the linked review reports in the top-level README.

This brings the expanded0.81–1.10solar-radius campaign to848 completed targets including prior16,64 and256 batches. It is not an all-sky or exhaustive TESS search. Selection, sensitivity and catalog limitations remain those documented in the frozen selection. No securely attributed new planet is established.

The `reserved_cache_absent` result is a historical pre-follow-up audit. A subsequent intentional reserved-sector download will cause that assertion to fail if this audit is rerun; preserve this result and use the separately frozen follow-up provenance to verify temporal separation.
