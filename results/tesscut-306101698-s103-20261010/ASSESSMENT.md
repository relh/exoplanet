# Sector 103 pixel diagnostic is unusable for source attribution

The fixed Sector 104 ephemeris was applied without retuning to an additional
Sector 103 cutout. The resulting difference image is negative across the entire
stamp: even its maximum formal difference/error value is −165.94. Visual
inspection shows broad spatial structure rather than a localized positive
transit deficit. Large background/systematic differences dominate this simple
local temporal subtraction.

**Do not interpret the emitted moment position, its 1.798-pixel target offset,
or its nearest-neighbor list as a transit localization.** The generic script
computes these descriptive quantities even without a positive dip; that
calculation does not make them astrophysically meaningful. This result cannot
corroborate the Sector 104 offset or identify a contaminant. It is retained as
a failed check, not a target or neighbor nondetection.

The raw cutout, SHA-256, source URL, nine event-window differences, aggregate
arrays, original numerical output and inspected plot are retained. No background
model was fitted and no phase was changed to force recovery. Sector 103 has
now been opened for this diagnostic and must not be called untouched data later.
