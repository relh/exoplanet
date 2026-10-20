# External method review: Pavel Rabtsevich / TIC4206066

The supplied thread identifies TIC4206066. Direct X access returned403; the thread mirror supplied links to the author's Zenodo records. Primary metadata and selected protocol documents were retrieved successfully and hashed in sources.json/documents.json. Downloaded code was not executed.

Primary sources: [manuscript record](https://doi.org/10.5281/zenodo.22967456), [supporting materials](https://doi.org/10.5281/zenodo.22999133), [future-observation protocol](https://doi.org/10.5281/zenodo.23175179). The official [TESS DDT table](https://tess.mit.edu/science/ddt/) lists program100 under Rabtsevich for TIC4206066 at two-minute cadence. Observation approval is not planet validation.

The author's records distinguish a stronger3.18-day signal from a tentative11.13-day signal, explicitly retain an unresolved companion as an alternative host, and claim no statistical validation. The manuscript abstract lists23 transits whereas the supplied thread says22; we do not silently reconcile versions or independently endorse either count. These are external claims, not our discovery or a completed replication.

The full future-observation protocol was inspected. It acknowledges that archival data were already inspected, fixes processing and predicted timing/depth checks for new data, and separates recovery, inconsistency, sensitivity-qualified exclusion and insufficient data. It also prescribes pixel localization and calibrates decision statistics with archival controls, while acknowledging limitations of overlapping resamples. Its thresholds and outcomes are specific to that experiment and should not be copied as universal detection significance.

## Sensible changes to our work

- Add retrospective leave-observing-season-out tests where at least three seasons exist. Refit using only the retained groups; score excluded data at the frozen fold prediction. Report every fold, timing uncertainty, coverage and sensitivity. Retrospective signal selection remains a limitation.
- Keep future-data protocols separate from retrospective validation. Freeze input scope, preprocessing, timing alternatives, nominal decisions and source checks before accessing genuinely new data.
- Preserve explicit insufficient-data outcomes. A missed uncertain prediction or low-sensitivity observation is not a planet exclusion.
- Prefer independent reconstruction of measurements and alternative-explanation tests over counts of scripts, analyses or agreeing agents.
- Preserve host uncertainty. Neither recurrence nor a follow-up allocation rules out a bound companion or eclipsing contaminant.
- Separate known-signal external replication from our novel-candidate ranking. This review does not add TIC4206066 to our discovery table.

The first incremental application is a retrospective three-season test of TIC469309982. Its six sectors have already been opened; it cannot be described as a fresh blind confirmation. We retain existing source ambiguity and the full original timing results regardless of the fold outcomes.
