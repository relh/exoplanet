# Single-sector faint midradius pilot

The frozen first 16 metadata-ranked targets have completed discovery searches: 13 below threshold, three flagged, zero original-policy or alternate-detrending-only follow-up selections, and no download/data failures. No planet candidate is established. All top-three peaks and failure flags are retained. This is 16 searches, not a completed search of the 5,732-target tier.

The metadata coverage audit excludes all frozen four-, three- and two-sector tiers. Of 10,582 remaining pool targets, 5,732 have a latest available single discovery sector and at least two other sectors separated by eight or more sector numbers. The other 4,850 fail this coverage rule. These targets retain the dated parent selection: distance ≤120 pc, 12<Tmag≤13.5, 0.5<R≤0.8 solar radii, Teff≤5200 K and catalog contamination ratio≤0.2. Selection uses metadata order, not measured quietness. All photometry was absent from the configured cache when the tier was frozen. That establishes local non-use, not absence of prior astronomical study or novelty.

The 16-target pilot uses unchanged preprocessing, period search, top-three peak accounting and quality gates, with 10-minute binning. One-sector training shortens period coverage and reduces the available number of events. Actual period bounds were checked for each injection. All distant reserved-sector cache paths remain absent after discovery and controls; they were not downloaded to improve this result.

| Flagged target | Main reasons retained |
| --- | --- |
| TIC458778313 | Fewer than three supported events; strongest peak dominated by one event; alternate detrending favors a different period; other peaks retain further flags. |
| TIC49530431 | Low formal SNR, too few supported events, unmeasurable odd/even comparison, comparable inverted signal. |
| TIC439409759 | Low formal SNR, comparable inverted signal and large duty cycle. |

All also lack a measured aperture-crowding value. These are computational screening outcomes, not visual source reviews or physical rejection of every possible planet. No follow-up qualified under the primary or alternate-detrending-only rules. A later audit of the separate existing two-event coverage policy admitted TIC458778313 peak1 for diagnostic follow-up; the omitted policy is corrected below.

## Deterministic sensitivity checks

The first three frozen metadata targets were used, with no selection by measured quietness or replacement. Reconstructed raw-flux loaders exactly match both original detrending-window arrays before injection. Box signals are exposure-integrated, multiplied into the published flux/error before binning and detrending, retaining the real variability/noise. The two sets use one phase each and fixed durations; they are not population completeness estimates.

| Control set | Trials | Period among top three | Period plus timing check | Non-crowding screening pass |
| --- | ---: | ---: | ---: | ---: |
| 1/2 Earth radii; periods 0.83/2.37 d; duration 0.04 d | 12 | 2 | 1 | 0 |
| 3/4 Earth radii; periods 2.37/5.73 d; duration 0.09 d | 12 | 8 | 8 | 7 |

All 24 injected periods lie inside the actual search grids. Both first-set period matches are two-Earth-radius injections; one has inconsistent timing. The larger-signal set was chosen after seeing zero small-signal screening passes and is explicitly a sensitivity extension, not an independent test or a revision of the first set. The original failures remain. A short intermediate commentary said none of the small injections recovered; the completed audit corrected this to two period matches and zero screening passes, as recorded here.

The larger controls demonstrate some usable sensitivity for this narrow configuration, while the small controls provide no successful screen-level Earth/super-Earth recovery. No null result excludes such planets. Further expansion should preserve the reserved data and use native-cadence follow-up and contamination checks for any eligible signal; all 5,716 remaining frozen targets are still unsearched by this pilot.

The verifier checks the tier's disjointness and latest-sector rule, raw metadata/photometry hashes, all 16 terminal outputs, unchanged source hashes, held-out cache absence, loader-equivalence records and injection grid bounds. Existing science algorithms were reused; no new full-suite test run is claimed for this configuration-only search.


## Subsequent coverage-policy correction

The earlier primary-policy audit was complete, but its statement about no warranted follow-up omitted the separate two-event diagnostic policy. TIC458778313 peak1 qualifies under that policy despite retaining its original flags. Its now-completed [diagnostic review](../qlp-faint-midradius-one-pilot-coverage-followup-20261011/458778313-peak1/ASSESSMENT.md) finds only one supported native event and inconclusive timing in sectors18/58. Those two reserved epochs were opened after the frozen prediction, so the earlier cache-absence verification describes the discovery/control snapshot only. No planet promotion. Original evidence and verification records are preserved.
