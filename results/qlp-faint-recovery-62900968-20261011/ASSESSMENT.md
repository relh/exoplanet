# TIC 62900968: missing-flux failure and separate usable-window search

The original Sector 44–46 search failed during empirical-noise estimation. Sector 45 has no finite KSPSAP_FLUX values in any of its 1,796 rows. Sectors 44 and 46 independently load 2,391 and 2,516 clean points. All usable assigned sectors were frozen before a separate period search; the decision did not use measured quietness or a favorable period.

The separate two-sector search retained the existing screening gates and 120-day baseline limit. Its strongest selected peak has formal SNR 6.72, below the screen threshold. Sectors 71 and 72 remain unopened. This is not an exclusion of planets and does not turn the failed three-sector attempt into a full-coverage nondetection. The recovery adds usable coverage for the same star, not another target. Verification checks raw hashes, identity, selection timing and reserved-cache absence; missing internal FITS checksums are recorded.
