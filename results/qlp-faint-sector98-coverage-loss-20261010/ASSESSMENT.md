# Where the longer-period controls lose event coverage

This audit traces the two-Earth-radius injections in the three frozen pilot
stars through raw timestamps, valid quality/flux/error cuts, ten-minute bins,
and both original detrending windows. It neither reruns the search nor changes
its gates. Counts use the injected ephemeris, not a refitted period or phase.

For the 9.73-day injection, cycles 0 and 3 retain 13 in-event bins each in all
three stars. Cycles 1 and 4 have raw timestamps but no valid input samples.
Cycle 2 retains 8, 13, and 10 bins respectively before detrending, but none
after either window. Thus missing event support includes both input rejection
and losses during preprocessing; it is not simply a lack of timestamp coverage.
These counts do not separate detrending edge rejection from other flattening
cuts and do not justify restoring rejected data without further validation.

For the 15.37-day injection, three primary events remain under the 1.5-day
window in each star. At half-period phase, every event has zero clean in-event
bins. Most already have no valid input samples; some surviving input samples
are subsequently lost during detrending. The secondary test is therefore
unmeasurable at this injected phase, consistent with the original gate result.
The 2.5-day window removes additional primary samples in two stars, but these
counts alone do not explain every difference between the periodograms.

See [results.json](results.json) for all primary and half-period centers,
in-event and local-baseline counts, stage totals, source hashes, and injection
provenance. The broad roughly 49-day clean span is not continuous coverage.
This is a diagnostic of six synthetic cases, not a survey sensitivity estimate
or a reason to promote a real peak with the same flags.
