# TIC 172715762: retained Sector 52 data failure

The original QLP product has 3,354 rows, 1,032 quality-zero
rows, zero usable positive flux measurements and zero valid errors. Its URL,
SHA-256 and integrity results are retained in plan.json. The unchanged loader
failed for insufficient adjacent samples. A separate same-epoch SPOC attempt
returned HTTP 404; it is not a nondetection.

The latest unreserved epoch, Sector 51, was selected before opening
its photometry. The separate unchanged search completed below threshold.
See [alternate plan](alternate/plan.json) and [result](alternate/result.json).
This supplies one usable search for the target, without repairing or concealing
the original Sector 52 failure. Reserved epochs remain unopened.
