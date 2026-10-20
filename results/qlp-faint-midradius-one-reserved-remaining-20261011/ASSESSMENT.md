# Remaining one-reserved-sector faint midradius search

All2810 remaining metadata targets were frozen after the completed16-star pilot. Each has one discovery sector and one reserved sector at least8 sector numbers away. Every target's available QLP cache was absent at freeze; earlier catalog/selection exclusions and metadata order are preserved. The plan, source hashes, slice identity and reserved-sector design passed verification before relying on results.

The search is running. Immutable checkpoint0094 records94 completed targets:82 below threshold,12 flagged,0 errors, and no peaks eligible under either follow-up policy. It verifies completed result identities plus raw input hashes/sizes and reserved-cache absence where no follow-up is eligible. This checkpoint is not a terminal count or a statement about every later result.

The original and coverage-diagnostic follow-up watchers are running. They retain original flags, refine only eligible training signals, freeze timing predictions and inspect the single reserved epoch. Already-opened alternate-peak caches are recorded and cannot be called blind validation. Original diagnostic policies and event/noise thresholds remain unchanged; one reserved epoch is weaker replication than two.

The pilot sensitivity experiment is limited to three stars and24 injections: none of six Earth-radius trials passed screening, while11 of12 trials at3–4 Earth radii passed except the permitted crowding flag. These controls do not estimate survey completeness and do not guarantee recovery in this remaining sample. Larger planets remain within the goal's scope.

[Selection](selection.json) · [Frozen plan](plan.json) · [Selection verification](selection-verification.json) · [Checkpoint0094](checkpoint-0094.json) · [Pilot evidence](../qlp-faint-midradius-one-reserved-pilot-20261011/ASSESSMENT.md).

No new candidate claimed. Continue the live processes and review eligible outputs; do not restart them based on a stale checkpoint. Scientific algorithms were reused unchanged; no fresh full-suite test claim.

## Checkpoint0468 and first source review

Checkpoint0468 verifies468 completed targets:417 below threshold,49 flagged,2 data errors and one eligible fit. TIC26042880's sector51 timing is inconclusive; source images instead favor neighboring-source contamination. [Source assessment](../qlp-faint-midradius-one-reserved-remaining-followup-20261011/26042880-peak0/ASSESSMENT.md).

The two errors,TIC139401998sector48 and97505520sector49, contain no finite selected KSPSAP flux/errors. Their raw files retain3836/3725 rows and2455/1966 quality-zero rows respectively. These are unusable inputs, not nondetections; no reserved-sector replacement was made. [Data audit](initial-errors.json). The search and both watchers remain live; checkpoint counts are interim.

## Checkpoint0888

The next immutable checkpoint verifies888 completed targets:779 below threshold,105 flagged and4 unusable. The sole eligible fit remains the reviewed TIC26042880 contamination case. Reconciliation checks all immutable target identities/counts, all four data-error audits, source-review artifact hashes and the reserved-sector51 input used for its inconclusive timing test.

New failures188503785sector47 and67362704sector48 have1881/3836 raw rows and1190/2455 quality-zero rows, but zero finite selected KSPSAP flux and uncertainty values. No reserved substitution or inference of planet absence was made. [New error audit](checkpoint-0888-new-errors.json) · [Checkpoint verification](checkpoint-0888-verification.json). The live search and both follow-up workers continue beyond this snapshot; this is not a terminal tally.


## Checkpoint2188

Verified immutable inventory:2188 completed of2810,1946 below threshold,233 flagged,9 errors. All nine errors were inspected against raw FITS; selected flux and error columns have zero finite values. They are unusable inputs, not nondetections. Four eligible follow-up fits have initial plot reviews and inconclusive reserved-sector tests. Source inspections:26042880 favors neighbor contamination;94923263 has background problems;439689688 favors a crowded neighboring source;77453582 pending. Both original/alternative and coverage policies retained unchanged. This is an interim scoped search, not all-sector completeness.


## Terminal reconciliation

All 2,810 discovery targets finished: 2,458 below threshold, 338 flagged, 14 errors (2,796 usable). Direct process polls returned exit0 for search67933 and follow-up35975/60408. Both terminal follow-up records reconcile to all11 eligible fits, all with initial plot reviews and inconclusive reserved timing tests. All14 errors have zero finite selected flux and errors in raw files; not planet nondetections.

Four initial source inspections complete:26042880 and439689688 favor contamination;94923263 and77453582 have background/mixed-sign image problems. Seven source inspections remain pending and are listed at README top. Prioritize224180405 and435878345 among the stronger recurring signals while preserving all eligibility and negative evidence. No all-TESS completeness, novelty or planet validation claim. verify_terminal.py checks frozen identities, source hashes, raw hashes, final four-field result-summary equality, error audits, all current reviews and terminal watcher coverage.


### TIC224180405 source update

All22 raw maps show a consistent off-target compact feature near224180336. Strong contamination evidence; unique faint-blend source and physical cause remain unresolved. Gaia134 selected TIC entries/149 mappings/133 unique returned sources and no variability rows, not a binary exclusion. Initial source checks now5 complete and6 pending. Prioritize435878345 next.


### TIC435878345 source update

Nine raw and nine processed event maps consistently locate dimming near435878339 about3.7pixels off target. Strong contamination evidence; faint nearby611541749 prevents unique-host inference from moments alone. Gaia five-source query has no variability rows, not an eclipse exclusion. Processed FITS identity/clock and arrays reconstructed and verified. Initial source inspections now6 complete,5 pending.


### TIC319010061 source update

All41 usable raw maps reviewed: boundary-adjacent positive feature, changing background and mixed target-region residuals; no secure host. Archived raw pixel audit confirms a sharp finite-valued column boundary, not missing-value padding. Processed exact URL404. Initial inspections now7 complete and4 pending.


### TIC23687157 source update

All11 maps reviewed; ten have recurring compact off-target feature near23687134, one has extreme negative field offset and remains retained. Gaia uniquely matches23687134 to ECL6234066831682693632, but catalog96.399515d does not match1.855187d TESS. Contamination favored, cause unresolved. Eight source inspections complete, three pending.


### TIC423597656 source update

Three raw maps reviewed: reversing bright-neighbor423597665 edge lobes and background changes; no secure target transit. Exact processed pixel URL404. Nine initial source inspections complete and two pending.


### TIC291110031 source update

Both raw maps show broad positive offsets and inconsistent target residuals; no secure host. Event0 fully quality2048 remains excluded. Exact processed pixel URL404. Ten initial source inspections complete;149005183 remains pending.


### Final initial-source reconciliation

TIC149005183: all three raw maps reviewed; background shifts and changing bright-blend residuals, no clean target transit. All11 initial source inspections now complete. None is a credible new planet candidate. This does not physically classify every signal or prove planet absence; all11 timing tests remain inconclusive.
