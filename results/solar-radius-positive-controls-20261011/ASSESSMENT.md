# Known shallow-planet controls in the solar-radius search pool

The unchanged discovery pipeline fully passes two of five preselected planet controls: Kepler-93 b and TOI-5159 b. Four of five have a top-three period within 1% of the selected catalog period, but two of those matches fail the original gates. No known period is supplied to the search itself. These are recoveries of known planets, not discoveries.

| Preselected planet | Sectors | Best corresponding period (days) | Corresponding formal SNR | Outcome |
|---|---|---:|---:|---|
|Kepler-93 b|40/41|4.726742|8.47|Pass; box depth 204 ppm|
|TOI-1435 b|14/15|0.686163|5.96|Below screening threshold|
|TOI-5788 b|40/41|6.341603|7.69|Low formal SNR and different strongest period under alternate detrending|
|TOI-5159 b|45/46|5.836942|9.59|Pass; box depth 233 ppm|
|HD 63433 d|44/45/46|Not recovered|—|Strong variability dominates the peaks|

TOI-5788's stronger known planet c is recovered at 16.213542 days and passes the gates. That is a separate success; it does not turn the preselected b outcome into a pass. The original results therefore contain three passing host datasets but only two passing preselected planets. HD 63433's highest peak is a broad 6.40-day variation, not a recovery of its selected 4.209-day planet d.

Selection was frozen before these photometry downloads: use the same solar-radius opportunity pool and adjacent-sector/contamination rules, join a current NASA Exoplanet Archive pscomppars query for confirmed transiting planets of 0.5–3 Earth radii and 0.5–20-day periods, require previously uncached training/reserved data, then select five distinct hosts with estimated area-ratio depths closest to 200 ppm. The proxy combines catalog planet radii with TIC stellar radii; it is not a precise predicted transit depth. All five hosts are excluded from the frozen unknown-object search pool.

This nonrandom, tiny control set tests relevant examples and exposes misses; 2/5 is not a completeness estimate or a population detection rate. Existing injection tests remain complementary. Period agreement alone is not a fresh astrophysical validation of these systems. All failures remain in the results, and no thresholds were relaxed.

A separate, explicitly exploratory residual search applied the existing at-most-two-round, at-most-20%-mask routine to all three nonpassing controls. TOI-1435 was skipped because its dominant peak is below SNR 8. Masking TOI-5788 c makes b the strongest residual feature, but SNR 7.81 still fails the existing formal-SNR gate. HD 63433 d remains unrecovered after both rounds. This does not change the original 2/5 outcome. See ../solar-radius-positive-controls-residual-20261011/verification.json for every stop reason and result.

The audit checks the selection chronology, all 11 raw products and FITS identities, source snapshots, NASA CSV/JSON equivalence, exact outcome arithmetic and unopened reserved caches. All control-fold plots were inspected. Residual mask fractions and unchanged retained flux/errors reproduce for both detrending windows in all three executed residual rounds. The scientific pipeline is unchanged; no additional model claim follows from the accounting checks.
