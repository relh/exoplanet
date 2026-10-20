# TIC 129577784: raw-pixel source check is inconclusive

The requested Sector 83 SPOC target-pixel product returned HTTP 404. Its wrapper preserves the command, stderr and child exit code 1. This is missing data at that URL, not a nondetection.

A raw 11-by-11 TESScut at the catalog target position downloaded successfully. Its source URL, hash, extraction manifest and FITS integrity checks are retained. The existing frozen 1.962286-day fit was used without retuning the period, epoch or image-event requirements. Thirteen raw quality-accepted image windows contribute. This uses the same TESS photons as QLP, with different processing; it is not independent observing evidence.

The difference plot was inspected. Residuals are weak, patchy and mixed in sign, without a compact source. The largest positive pixel is about 2.11 times its formal error, an uncalibrated selected statistic. The algorithm reports a moment 2.75 pixels from the target, but the weak map does not support interpreting it as host localization. Nearby bright TIC 129577788 appears in the median image; that alone does not implicate it as the variable source.

The previously observed multiple dips per selected cycle still favor a period alias, and reserved-sector timing remains inconclusive. Raw pixels neither establish an on-target transit nor identify contamination. Retain the signal as an unresolved diagnostic, not a credible new planet candidate.
