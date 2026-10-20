# Independent ZTF time series retrieved; interpretation pending

All ten requested ZTF DR24 cloud records were retrieved successfully, after the separate light-curve API had repeatedly timed out. The compute process exited0. These are independent ground-based observations, but no transit recovery or physical classification is claimed yet.

| TESS target | ZTF records | Measurements | Quality-zero finite measurements | Catalog nobs sum |
| --- | ---: | ---: | ---: | ---: |
| TIC422626648 | 2 | 576 | 466 | 782 |
| TIC241928959 | 5 | 820 | 779 | 989 |
| TIC196681132 | 3 | 738 | 658 | 1041 |

The total is2134 exported measurements, of which1903 have catflags=0, finite HMJD/magnitude/error and positive error. These are record counts, not yet a cross-object unique-exposure count. Individual cloud nepochs agree exactly with their nested row counts. Object IDs and filter IDs match the prior catalog query; source-coordinate differences are below0.044arcsecond, consistent with the cloud's float32 coordinate storage. Association with the physical TESS host, including proper motion and blends, still needs assessment.

Several cloud counts differ substantially from the corresponding TAP catalog nobs, including one TIC241928959 field record with3 versus84 observations. The cause is unresolved. No completeness claim is made, and the discrepancy is retained per record in audit.json. It is not explained away as quality filtering: the unfiltered nested counts already differ.

Quality-zero HMJD ranges are58204.34844–60859.23858 for TIC422626648,58235.50210–60969.14845 for TIC241928959 and58198.36379–60857.23721 for TIC196681132. No repeated quality-zero timestamp appears within an individual object record. Cross-object duplicates remain unchecked. No photometric outlier rejection, period adjustment, phase search or transit selection has been performed.

The downloaded schema identifies HMJD as exposure-midpoint HJD minus2400000.5, truncated to five decimal places. Its underlying time scale is not explicit in that field description. Unlike prior API data, these records must not be treated as uncorrected MJD. Further timing verification/conversion is needed before using the frozen TESS windows. The prior TESS clock-propagation uncertainty remains applicable; a lack of points in a nominal narrow window would not reject a planet.

The retrieval follows [IRSA's DR24 cloud tutorial](https://caltech-ipac.github.io/irsa-tutorials/ztf-lightcurves/). plan.json records the collection URL, selected IDs, script and input hashes, and package versions. Dependencies were isolated with uv; the repository lock is unchanged. The three selected spatial partitions are recorded in selection.json. Raw selected records are serialized to JSON in ignored data/ztf and hashed in results.json; these are selected-record exports, not original Parquet byte streams. The schema's original Parquet metadata bytes are separately cached and hashed. audit.py checks identities, hashes, fields, counts and quality summaries; summary.json records the verified totals. No scientific detection code changed or new test-suite run is claimed.

Next: resolve timestamp conventions, audit source associations and cross-object duplicates, then compare useful time coverage with the frozen TESS timing uncertainty. Reconcile the cloud/catalog count differences before claiming complete ZTF coverage. The search goal remains active.
