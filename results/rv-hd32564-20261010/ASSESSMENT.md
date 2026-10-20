# HD 32564: replication of an externally reported lead

The main radial-velocity signal family reported by Mehran Jalali is reproducible
in HARPS-RVBank v2. This is an external lead, not a new discovery by this project.
Stellar activity and the full range of aliases remain incompletely tested.

205 public measurements form191 observing nights. With separate pre/post-May2015
instrument offsets, a linear trend, circular sinusoids and fixed2m/s nightly
jitter, the three-signal fit yields:

| Period(days) | Semi-amplitude(m/s) |
|---:|---:|
| 2.556593 | 4.259 |
| 11.061030 | 3.529 |
| 23.597024 | 2.913 |

The unrestricted sequential search initially selects the1.635-day daily alias
of the shortest signal. Joint comparison favors the2.5566-day family under the
assumed model. This is why sequential peak picking alone is insufficient.

The first143 nights train the externally suggested period family.41 later
pre-upgrade nights are tested with unchanged coefficients. Three signals give
2.21m/s predictive RMS versus5.41m/s for the offset/trend baseline. Four signals,
adding approximately49.1days, give1.95m/s. Seven later post-upgrade nights are
excluded from this prediction because their instrumental offset is unknown to
the earlier training set. Full-data fits do include them with a separate offset.

The four-signal full-data fit has periods2.556630,11.063272,23.611849,49.102191days,
and amplitudes4.165,3.437,2.947,1.644m/s. White-jitter1/2/3m/s sensitivities and
alternative alias fits are archived. These fits do not yield a formal false-alarm
probability, a marginal likelihood, or planet validation. The public suggested
periods came from the full historical dataset, so this chronological test is a
retrospective predictive check, not an independent blind discovery.

Activity indicators are archived and initially compared at the signal periods;
correlated-noise models, activity phase evolution, additional aliases, and further
independent reductions still need scrutiny. No true planet masses are inferred:
RV amplitudes constrain minimum masses only under a stellar/orbital model.

A fresh NASA pscomppars rectangular query around the target returned no confirmed
planet rows. This is neither an all-literature check nor proof of novelty.
Yu et al.2024 already includes the star in an activity sample.

Reproducibility: raw RV source/hash is ../user-posts-20261010/hd32564-source.json;
configuration.json stores filtering, split, source/module hashes. run.py produces
the original screen and frozen temporal model; compare_modes.py and plot.py are
follow-up diagnostics.34 project tests pass, including a deterministic irregularly
sampled two-signal RV injection with instrumental offset and linear trend.
