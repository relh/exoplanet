# Additional archive coverage for the six candidates

**Current metadata identifies additional products or footprints for four candidates.** The previous search scopes remain complete as defined, but their opened-sector lists did not exhaust these later archive avenues. Product presence and a detector footprint do not establish usable precision, recurrence or host identity.

| TIC | Additional QLP sectors beyond documented opened list | Other additional TESScut footprints |
|---|---|---|
| 80387959 | None | 64, 99 |
| 402358350 | None | None |
| 241928959 | None | None |
| 469309982 | 90 | None |
| 96166003 | 86 | 71 |
| 5546257 | 89, 99 | 8, 63 |

“Additional” is relative to the current documentation, not proof of unseen data. Separate target investigations must inspect history and caches and freeze predictions before opening flux. Completed follow-through: [80387959 geometry rejection](../new-epochs-80387959-20261012/ASSESSMENT.md), [469309982/96166003 QLP tests](../new-epochs-469309982-96166003-20261012/ASSESSMENT.md), and [5546257 QLP tests](../new-epochs-5546257-20261012/ASSESSMENT.md). The remaining non-QLP footprints for 96166003/71 and 5546257/8/63 were not tested. No flux was accessed by this metadata audit. For 402358350 and 241928959 the returned metadata supplies no extra TESS epoch; it does not exhaust other missions or future releases.

The [plan](plan.json) preserves exact Gaia DR3 coordinates and their input hash. Six position-based TESScut responses and one exact-TIC QLP query are recorded in [manifest.json](manifest.json), with raw responses under ignored `data/coverage-six-extension-20261012/`. [Results](results.json) retain the full returned sector lists and differences. Gaia coordinates were not propagated to each observing epoch. A footprint can include an edge with little or no useful target flux.

[verify.py](verify.py) independently checks all raw hashes, query positions, target identities, QLP pagination and sector-set arithmetic. [Verification](verification.json) passes 15 checks. It does not establish aperture quality or access history.

Archive interfaces: [MAST QLP](https://archive.stsci.edu/hlsp/qlp), [TESScut API](https://mast.stsci.edu/tesscut/docs/getting_started.html). QLP reports a change to TGLC photometry beginning in sector 94; extraction changes must be considered when comparing sector 99/100 with older products. This context is not evidence of intrinsic depth variation.
