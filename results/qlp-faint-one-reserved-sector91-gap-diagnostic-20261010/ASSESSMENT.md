# Sector 91 shared-event diagnostic

Nine diagnostic peaks on eight stars have only two supported discovery events.
Every one combines an event in the visibly noisy BTJD 3787–3789 interval after
the long data gap with an event between BTJD 3796.29664 and 3796.37773.
The latter centers span 1.9461 hours despite sky separations reaching 21.8373 degrees.
The two peaks on TIC 196682021 use essentially the same last event.

All discovery plots were visually inspected. Excluding BTJD 3787–3789 at the
unchanged native-cadence ephemerides leaves only one supported event per diagnostic
peak. Several surviving dips retain substantial formal SNR; the cut does not make
them disappear. It removes the evidence for repetition outside the noisy interval.
The main lead TIC 101436430 is unchanged, retaining four supported events.

This favors shared instrumental/processing structure for the diagnostic group.
It is a post-selection comparison, not a calibrated false-alarm test: common
observing windows and selection can correlate fitted times. No pipeline threshold
or frozen ephemeris was changed. Each reserved Sector 46 check remains timing-
inconclusive, so its depth is neither confirmation nor a valid rejection.
Pixel localization and individual catalog vetting were not performed for this
low-priority diagnostic group; a physical source is not established.

See run.py / plan.json / results.json for native-cadence fixed measurements,
and coincidence.py / coincidence.json for pairwise sky separations and times.

| TIC | Peak | Frozen period (d) | Retained review |
|---|---:|---:|---|
| 130726927 | 0 | 8.43809202 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/130726927-peak0/ASSESSMENT.md) |
| 147696488 | 0 | 8.72513243 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/147696488-peak0/ASSESSMENT.md) |
| 196682021 | 1 | 7.90910603 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/196682021-peak1/ASSESSMENT.md) |
| 196682021 | 2 | 8.71869053 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/196682021-peak2/ASSESSMENT.md) |
| 377171858 | 0 | 8.80194579 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/377171858-peak0/ASSESSMENT.md) |
| 377230444 | 0 | 8.82061117 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/377230444-peak0/ASSESSMENT.md) |
| 377248103 | 1 | 7.86944074 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/377248103-peak1/ASSESSMENT.md) |
| 380194703 | 0 | 8.84538237 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/380194703-peak0/ASSESSMENT.md) |
| 56754465 | 0 | 8.75789889 | [Assessment](../qlp-faint-one-reserved-sector91-pilot-coverage-followup-20261010/56754465-peak0/ASSESSMENT.md) |
