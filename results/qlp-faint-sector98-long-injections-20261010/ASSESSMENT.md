# Longer-period Sector 98 controls expose screening limitations

All twelve injected signals were recovered among the top three periods and
within half the injected duration at the three checked times. **None passed
the full non-crowding screening gates.** These negative gate results are
retained; period recovery alone is not end-to-end candidate recovery.

This separate control run uses the same first three frozen pilot stars, periods
9.73 and 15.37 days, radii two and three Earth radii, duration 0.09 days, and
phase fraction 0.317. Signals enter raw flux before binning and detrending;
baseline arrays match the original loader at both windows. All runs completed
without errors. See [audit.json](audit.json) for individual results and hashes.

At 9.73 days, the original diagnostics report only two supported events,
despite the roughly 49-day clean time span. All six cases fail the three-event
gate; one additionally fails event-depth consistency and another detrending
consistency. At 15.37 days, all six have three supported events but fail the
secondary-measurement and alternative-detrending checks. A long first-to-last
time span therefore does not guarantee enough usable phase coverage. These
results do not establish that every gate failure is caused by missing coverage.

The original discovery search and original follow-up policy remain intact.
A separately frozen diagnostic policy now examines peaks with at least two
supported events whose flags include insufficient supported events or an
unmeasurable secondary, permitting only crowding and alternative detrending
as additional flags. It retains all original failures and does not admit the
inconsistent-event-depth injection or variability/noise failures. Any ensuing
checks remain diagnostic-only and use the existing frozen-ephemeris tests,
including their requirement for three supported training events before
declaring precise timing. No candidate promotion follows from this policy.

No reserved photometry was opened by these controls. One phase, one duration,
and three stars are insufficient for completeness or false-alarm calibration.

A subsequent [cadence audit](../qlp-faint-sector98-coverage-loss-20261010/ASSESSMENT.md)
locates losses at both the input cuts and detrending steps. Raw timestamp
coverage alone would overstate the usable event coverage.
