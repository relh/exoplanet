# Live reduced-window recovery stream

This stream preserves every original failure. For baseline-limit errors only, it chooses the longest latest suffix of three then two original training sectors whose cleaned time span fits the unchanged 120-day guard. The selection is recorded before a new period search. Reserved epochs are not used in choosing the window. Other error types are explicitly deferred for individual review.

The first audited 12 completed recoveries are usable: ten below threshold and two disqualified. No follow-up is eligible in that snapshot. Selection timestamps, original/result identity, raw hashes and reserved cache absence are verified. This is an incremental snapshot, not a terminal campaign or completeness claim. The stream shares the existing search and follow-up algorithms; 13 campaign/follow-up tests passed when this orchestration was introduced. New follow-up plots, if generated, require individual review before classification.

A later deferred error on TIC 309703302 reports insufficient adjacent samples for empirical errors in original training sectors 66–69. It is not a nondetection and requires a separate per-sector usability check.

The later checkpoint 0043 has 42 usable automatic recoveries (39 below threshold, three flagged) plus the retained deferred record for TIC 309703302. Its individual per-sector review now resolves the data failure: Sector 66's selected flux is entirely nonfinite, while sectors 67–69 are usable and yield a below-threshold alternate search. See `../qlp-faint-recovery-309703302-20261011/ASSESSMENT.md`. The original deferred stream record remains unchanged as provenance; the separate recovery must be included once in joint inventories.
