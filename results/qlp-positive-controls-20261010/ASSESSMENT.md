# QLP known-planet controls and documented missed signals

Four known hosts were tested on their earliest/latest adjacent QLP pairs,
chosen before opening their photometry. There are **seven distinct sector-pair
datasets**:GJ1132's earliest and latest pair are identical, so its duplicated run
must not be counted as an independent control. Period recovery means a top-three
peak within1% of a catalogued period, not full validation or exhaustive recovery
of every planet in each multi-planet system.

| Host | Early pair | Late pair | Initial result |
|---|---|---|---|
|L98-59|8/9|89/90|c/d period matches early; no matches late|
|TOI270|3/4|97/98|c/d matches both; early c has an event-consistency flag|
|TOI700|4/5|96/97|No early recovery; late c recovered|
|GJ1132|9/10|same|b recovered; duplicate labels retained but counted once|

Thus5/7 distinct datasets recover at least one known period initially;4/7 have
a match passing all non-crowding checks. These few selected positives are not a
completeness estimate. The missed early TOI700 signal remains a negative control
outcome, not silently removed or counted as a pipeline success.

The L98-59 late dataset is dominated by one deep event. An explicitly separate,
at-most-two-round residual search masks the currently dominant phase window,
removing at most20% cumulatively, while preserving original flux values and all
original searches. It recovers L98-59 c at3.690286d and then b at2.253388d, both
passing non-crowding checks. TOI270 b also emerges after masking stronger signals.
No known period emerges for early TOI700. Across original plus residual runs,
6/7 distinct datasets have at least one known-period match.

Residual searches add trials and may mask real events. This demonstration does
not classify the removed event as instrumental or establish a survey-wide false
alarm rate. See `../qlp-positive-controls-residual-20261010` for every round,
mask fraction, failed check and stop reason. Original1%-period-match comparisons
also admit nearby aliases; do not count every approximate match as a recovered
physical planet.

New native-QLP follow-up and mask integration tests bring the suite to46 passes.
Synthetic tests distinguish recurring signals, absent signals and unusable data;
verify the freeze precedes reserved-sector reads; and preserve retained flux
under masking in both detrending windows.
