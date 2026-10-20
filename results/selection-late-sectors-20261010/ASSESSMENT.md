# Late-sector search expansion, 2026-10-10

Search **1,322 additional small nearby stars** that were excluded by the original
earliest-adjacent-sector selection and had no photometry opened in earlier
campaigns. The complete scope is `eligible.json` plus `campaign-plan.json`;
`selected.json` is an initial256-star preliminary subset, not the final scope.

Each target has two adjacent training sectors from56–85 and at least one reserved
sector separated by at least eight sector numbers. The reserved epoch can precede
or follow training. This coarse selection is followed by actual time-based
prediction tests. The original radius, brightness, distance, temperature and
crowding cuts are retained. Ranking uses a brightness/radius proxy rather than
measured quietness. This is an opportunity-based search, not evidence that no
other researchers examined these stars.

Training searches use10-minute inverse-variance bins of the native200-second
files, preserving native files and checksum provenance for subsequent refinement.
Two deterministic injected finite-exposure signals (periods0.83/5.21d) recover
periods to0.2% and depths within20% through binning, flattening and the joint
search. All39 tests pass. This small test is not a survey completeness estimate.
Search period range0.5–20d and all prior screen thresholds remain unchanged.

## Historical checkpoint (superseded by final audit)

At the recorded checkpoint, **951/1,322 targets** have usable discovery searches:
362 below threshold,586 flagged,3 unflagged screening passes, zero errors.
The322-star batch is terminal (process exit0); the1,000-star batch is running.
`checkpoint.json` stores exact completed-record hashes; counts here are a snapshot.

All three current unflagged passes have been followed up:

- **TIC395477762, ~6.371d:** deep secondary eclipse at phase0.472; strong binary
  evidence, not a planet lead. The fixed half-phase automated check missed it.
- **TIC420359321, ~11.9d:** broad structure, inconclusive reserved timing,
  not reproduced by QLP training reductions; not promoted.
- **TIC68286478, ~14.3d:** weak irregular feature, inconclusive reserved timing,
  no strong QLP support; not promoted.

Ten exactly-one-flag peaks available at an earlier checkpoint were also tested
under a saved exploratory plan. TIC382552502 fails both reserved sectors despite
expected sensitivity; all other checks are timing-inconclusive. Original flags
are retained. See `../followup-late-marginal-20261010/plan.json` and per-star tests.
An automated follow-up worker applies the same frozen-prediction, native-plot and
QLP tests to every subsequent unflagged pass; outputs require human/agent review.

Refreshed Kostov2025 and live Villanova EB catalogs give no positional match
within126arcsec of these1,322 targets. A catalog non-match does not establish
novelty or exclude faint contaminating binaries. No new candidate promoted yet.

Final campaign:all1322 complete with no errors; see
[final audit](../audit-late-sectors-20261010/ASSESSMENT.md).
