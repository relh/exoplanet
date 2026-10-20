# TIC 301942350: unusable discovery and failed same-epoch recovery

Sector 17 QLP has 1130 rows and 640 quality-zero rows,
but zero usable positive flux measurements and zero valid errors. Raw URL,
hash and integrity results are preserved. The empirical-error loader fails
because no usable adjacent measurements exist.

All other available epochs are reserved. A separate same-epoch SPOC attempt
returns HTTP 404. Reserved products remain unopened. This target is not counted
as successfully searched; no nondetection or planet-exclusion claim.
