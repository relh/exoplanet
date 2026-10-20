# Running recovery of incomplete discovery data

This companion worker handles only completed per-target errors from the active
1,845-star search. It does not restart the survey or overwrite original failures.
Each assigned training sector is inspected separately. A target is searched only
if at least three assigned sectors remain usable, with unchanged signal-quality
gates and the existing120-day baseline limit. Reserved epochs remain unopened
unless a recovered peak separately qualifies for frozen-ephemeris follow-up.

The first processed target, TIC97361835, has usable Sectors44,45and47. Sector46
fails the missing-uncertainty fallback because there are insufficient usable
adjacent samples. The recovered three-sector search is below threshold. Its
original failed result remains in the main campaign. Raw hashes and download
provenance are retained even for failed sectors.

TIC389918717 was recovered previously and is explicitly excluded from duplicate
work here; see ../qlp-faint-recovery-389918717-20261010/. Neither recovery is a new
star for counting purposes. Narrower coverage does not imply original sensitivity,
and absent data are never treated as a negative transit detection.

This worker remains active until the parent campaign is terminal and all its
original errors have been handled once. Progress files are provisional; terminal
inventory and recovery-aware unique-star counts must be audited at completion.
