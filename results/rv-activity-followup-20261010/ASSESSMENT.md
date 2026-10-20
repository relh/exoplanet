# New RV leads: follow-up outcome

**HD297396,4.268863days: unresolved RV signal, not a likely planet yet.**
The initial SERVAL training semi-amplitude is7.63m/s. The frozen three-component
model improves predictions on13 later same-instrument nights relative to an
offset/trend baseline. Removing the4.27day term worsens those predictions by about
10.8 in chi-square when other periods are fixed. Post-hoc three-block checks also
favor it in SERVAL. However, DRS gives negative improvements on the original late
sample(-16.0) and latest block(-113.8), despite a4.268day peak in its full series.
Shared spectra and differing reductions make this a processing/coherence question,
not independent confirmation. The last14 nights from an instrument configuration
unseen in training were excluded from the original prediction test.

Initial activity-indicator periodograms do not have their strongest peaks at4.27d.
That does not exclude stellar activity: windows, errors, evolving phases and
correlated noise are incompletely modeled. Limited exact-name web searches did not
establish a prior planet report; alias/literature and catalog checks remain
incomplete. No novelty or physical mass inference is made.

**HD95542,81.601days: not promoted.** The original full-model prediction looked
better than a baseline, but component attribution changes with how the remaining
periods are optimized. Fixed-period drop-component tests favor omitting81.6d on
the original late sample and two of three chronological blocks in both reductions.
This model dependence is retained as negative evidence. The star is in the
[Yu et al.2024 activity sample](https://arxiv.org/html/2401.05528v1).

Further non-new recoveries:
- HD157172's ~105d signal appears in Mayor et al.'s2011 HARPS manuscript, including
  Table22's104.84d orbit: [ESO-hosted primary manuscript](https://messenger.eso.org/public/archives/releases/sciencepapers/eso1134/eso1134b.pdf).
  Its absence from our current confirmed-only query does not imply novelty.
- HD41248's18/25d periods have a long planet/activity debate;
  [Santos et al.2014](https://www.aanda.org/articles/aa/pdf/2014/06/aa23808-14.pdf)
  explicitly discusses a stellar-activity explanation. No new discovery here.
- HD16008 is HIP11915, with a published long-period companion hypothesis:
  [Bedell et al.2015](https://arxiv.org/abs/1507.03998). Our near-daily peak is not
  a secure new short-period planet and needs a long-period/alias model.
- HD85512 is marked a [false-positive planet by NASA](https://exoplanetarchive.ipac.caltech.edu/overview/HD%2085512).

Scripts run.py and temporal.py retain activity scans and temporal comparisons.
These checks are post-hoc on already-opened data, not additional fresh holdouts.
