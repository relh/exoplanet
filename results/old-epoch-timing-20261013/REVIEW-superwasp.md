# Independent review of the SuperWASP metadata screen

The saved responses support the archive assessment: the returned TIC 80387959 field records do not justify a decisive transit experiment, and the tested TIC 402358350 cone returns no indexed series. Neither finding is evidence against a planet.

This review reads the frozen queries, saved UI tables and network response, manifest hashes and derived summary. It issues no network requests and opens no epoch photometry. [review_superwasp.py](review_superwasp.py) independently checks all 21 returned field/control rows, distances and spans, the explicit empty-region response, summary arithmetic and raw-file hashes. **193 checks pass** in [superwasp-review.json](superwasp-review.json).

| Check | Independent result |
|---|---|
| Search radius | TAP uses 0.03333333333333333 degrees = 120 arcsec; UI fields explicitly label radius in arcsec. Successful 803/control result headings retain “120 sec”; 402 network request records `radius=120`. |
| TIC 80387959 | Twelve returned records; every record has 6–7 points spanning approximately 37.45–37.47 minutes in the same interval. The saved UI footer confirms 12 of 12, so this is not a first-page-only assessment. |
| Nearest 803 record | `1SWASP J110114.50-483649.2`, 0.8306 arcsec from the supplied J2016 coordinate; seven points across 37.4674 minutes, catalog scatter about the median 0.1692154 mag. This supports a close positional association, not uncontaminated target photometry or a resolved source identification. |
| TIC 402358350 | Exact requested coordinates appear in the HTTP 200 UI query and XML response: “No data found in this region.” This is a bounded archive-index nonmatch, not an astrophysical non-detection. |
| Positive control | The official documentation's `1SWASP J063954.26+353125.7` is recovered 0.0987 arcsec from its name-derived coordinate, with 4,965 points. Nine field records are displayed, and the footer confirms 9 of 9. |
| TAP failures | Both target cones and the positive control return HTTP 403. These blocked queries are retained as errors and are not counted as empty results. The later UI responses independently establish the bounded findings. |

The catalog scatter is not a measurement of a shallow transit or a calibrated detection threshold. Seven points over less than an hour cannot establish the reported 4.19-day recurrence, and no event coverage or individual measurement errors have been inspected. Multiple nearby catalog rows share the same observing interval and cannot be summed as independent target epochs. The large scatter further discourages opening these records merely to repeat a weak fixed-clock null test.

The [backward timing calculation](ASSESSMENT.md) supplies a separate limitation: every original timing gate fails at the tested representative early epochs. It does not calculate the exact phase of this archive interval or turn an absent dip into an exclusion. Any later attempt to open flux would require an independent scientific justification and a separately frozen plan, preserving HJD_UTC versus BJD_TDB conventions and the unresolved blending problem.

No physical classification, likelihood percentage, completeness claim for all SuperWASP holdings, or calibrated precision follows from this review.
