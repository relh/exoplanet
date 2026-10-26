# Raw observation cache retirement

The owner authorized reclaiming regenerable research inputs after preserving a
remote summary. This document scopes retirement to old, unused downloaded FITS
files in `data/qlp`, `data/pixels`, and `data/lightcurves`. Do not remove private
backups, research outputs, agent histories, checkpoints, or saves.

## Research summary already published

Publication commit `a89b5885d35565e7a818444ee567b416d9dc5dda` retains the README,
CHECKED-RESULTS index, manuscript, assessments, figures, and measurements.
The search produced six possible signals, not confirmed planets. TIC 80387959
and TIC 402358350 are the strongest leads; source attribution and nonplanet
explanations remain unresolved. The largest search attempted 7,004 targets and
reviewed 28 screening passes. Overlapping search counts must not be added.
Failed checks and negative findings remain in the evidence index. Neither lead
passed the reported TRICERATOPS validation thresholds. Cleanup does not alter
any scientific claim, create new blind holdouts, or resume research queues.

## Retirement criteria and reproduction

For each removed file, preserve its adjacent `.fits.json` provenance document
with source URL, retrieval timestamp, byte count and SHA-256. Only remove a
regular FITS file whose actual size and streaming SHA-256 match that document,
whose source is the public MAST archive, and which has no active reader and no
recent modification. Preserve files with absent or mismatched provenance.

A representative QLP manifest URL returned HTTP 200 and the expected 72,000-byte
length on 2026-10-26. This establishes current archive access, not a claim that
every URL was individually fetched again. No new bulk download was performed.

The existing `src/exoplanet/pipeline.py:fetch` routine recreates a missing cache
file from its public URL. To reproduce, use the preserved per-file URL and
compare the restored bytes with the preserved SHA-256 before scientific use.
Do not overwrite the original provenance metadata. An archive response differing
from the recorded hash is a reproduction gap, not equivalent evidence.

The retained manifests record previously inspected data even after local FITS
files are removed. Cache absence must never be interpreted as a fresh blind test;
continue following the data-access preflight in CODE-ORGANIZATION.md.

This is storage maintenance only. No scientific algorithms, predictions,
measurements, or publication claims were changed and no scientific tests rerun.
