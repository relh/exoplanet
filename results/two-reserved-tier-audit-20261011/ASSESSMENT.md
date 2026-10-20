# Earlier tier coverage audit

All 28,049 frozen selected targets have exactly one matching initial result:
23,789 below threshold, 4,206 flagged and 54 data failures. Target identity and
training/reserved sector lists agree with the corresponding plans and selections.
Selection, plan and result hashes are recorded. No missing or duplicate records
were found. This verifies coverage, not scientific correctness or completeness.

Recovery-plan verification resolves the sector differences. Twenty initially
failed stars have a usable screened result, leaving 34 without one and
28,015 distinct stars with usable searches. Sixteen records change discovery
sectors: twelve below threshold, two flagged and two still failing. Each matches
its own recorded plan, whose timestamp precedes processing; original reserved
lists are unchanged and have zero overlap with alternate training sectors.
Original-result and raw-data hashes match the archived plans and results.

The two flagged alternate searches do not meet follow-up gates: TIC 120523140
has a large-duty-cycle peak and variability failures; TIC 26587095 lacks event
support and measurable odd-even/consistency checks, with additional depth and
single-event failures on another peak. No candidate is promoted.

These are separate alternate-sector searches, not repaired original light
curves or additional distinct stars. Plan timestamps verify recorded provenance,
not an independent forensic guarantee that data were never accessed earlier.
Initial equality/subset audit assertions exposed the differences; the explicit
verification now covers their actual planned behavior.

TIC 423088347 has an explicit insufficient-training-coverage result rather
than a targets file. Its original four sectors yielded only two usable sectors,
below the recovery minimum of three. Its plan, sector checks, assessment and
terminal result are hashed. This is not a nondetection.

The final HD 32564 activity assessment was reviewed. Three shorter externally
reported RV components improve prediction in its wider omitted-year tests.
The approximately 49-day component fails some 2012 DRS alternatives. Reductions
share spectra; the checks do not exclude correlated stellar activity or
establish a new discovery.

Next: check earlier-tier follow-up evidence before asserting whole-campaign
completion. Existing unresolved signals remain unresolved.
