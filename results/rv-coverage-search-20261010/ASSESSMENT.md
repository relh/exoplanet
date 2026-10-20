# Coverage-selected HARPS search

The bulk HARPS-RVBank v2 release contains252,615 rows across5,239 archive target
names. Selection by actual quality-filtered observing coverage produced32 nearby
FGK targets with >=80 nights, >=500day span and median RV error<=3m/s, after a
confirmed-planet positional exclusion. This is not a complete published-candidate
or false-positive exclusion. Full source/hash and coverage inventory are in
../rv-coverage-20261010/.

Earliest75% of nights were searched; the last25% were reserved by a recorded
night boundary before period fitting. Training-only searches used instrument
offsets, linear trend, fixed2m/s nightly jitter, up to three circular sinusoids,
and periods0.8–min(1000,training span/3)days. Saved models were applied without
period, phase or amplitude refitting to eligible reserved nights.28targets had
at least10 reserved nights with already-trained instrument offsets; four did not.
Those four are explicitly inconclusive, not non-detections.

Most full models worsen held-out predictions. Follow-up of apparent improvements
finds previously reported/disputed signals (HD157172,HD41248), a known long-period
system with a near-daily alias (HD16008/HIP11915), a known activity false positive
(HD85512), and a model-dependent result (HD95542). None is a new planet discovery.

**HD297396's4.2689day signal remains an unresolved lead**, with favorable SERVAL
checks but failed late-data DRS checks. It is recorded at the top of README with
that limitation. See [detailed follow-up](../rv-activity-followup-20261010/ASSESSMENT.md).

This screen is not a completeness or occurrence-rate experiment; circular fits,
limited components, long-period truncation, sampling aliases and stellar activity
can hide real planets or generate compelling peaks. Chi-square improvements are
not calibrated false-alarm probabilities. Published candidates can be missing
from a confirmed-only catalog. Activity modeling, broader aliases and additional
independent observations remain necessary for promotion.
