# Resolved-observation planning for the two priority signals

**TIC 80387959 supports a provisional approximately 5.6-hour observation window. TIC 402358350 needs ephemeris recovery before a short targeted observation.** This packet propagates existing frozen timing profiles and identifies neighbors whose eclipses could mimic each signal. It supplies no new observational evidence and does not change either APC classification or establish a planet probability.

## Scheduling feasibility, October 2026–April 2027

| Target | Nominal period | Duration | Preserved midpoint envelope, full width | Full observation span | Timing decision |
|---|---:|---:|---:|---:|---|
| TIC 80387959 | 4.192168718 d | 2.23 h | 1.35–1.42 h | 5.58–5.65 h | Passes original timing gate; provisional window |
| TIC 402358350 | 11.769544332 d | 3.46 h | 11.99–13.04 h | 17.45–18.50 h | Fails original timing gate; recover timing first |

The observation span includes the full midpoint envelope, transit duration and an assumed one-hour baseline on each side. The 80387959 envelope uses its original frozen profile; the 402358350 envelope includes both already-preserved expanded-training detrending profiles. The original gate requires the primary profile's largest timing deviation plus three heuristic epoch floors to be less than half a duration. The 402358350 primary deviation alone grows from 3.68 to 4.03 hours, exceeding its 1.73-hour half-duration. Its earlier discovery-only profiles span 68–75 hours when extrapolated to these dates; these historical alternatives remain in the packet but are not adopted as the updated window.

**These widths are not confidence intervals or guarantees of event coverage.** They propagate a selected local period-profile family and an existing heuristic floor. The saved profiles do not hit their local search boundary, but this does not exclude other aliases, non-periodic variability, correlated noise or model error. No clock was refined here, and successful recovery of 80387959 in already-opened sectors does not convert the local profile into a calibrated timing distribution. Treat a non-detection outside adequate timing coverage as inconclusive.

[events.csv](events.csv) contains all 47 nominal 80387959 events and 17 nominal 402358350 events from 13 October 2026 through 30 April 2027, with midpoint bounds, full-track endpoints and timing-gate decisions. It is an event list, **not an observability schedule**. Select dates only after computing site-specific target altitude, twilight, Moon separation, weather and instrument constraints. No observing site or instrument was selected.

BJD_TDB is the primary clock: `BJD_TDB = BTJD + 2457000`. UTC columns are approximate geocentric arrival times, derived with the bundled Astropy solar-system ephemeris, not a mere renaming of a TDB calendar date. Observatory timestamps must be converted consistently before fitting. Millisecond output formatting is computational precision, not claimed event accuracy; the much larger profile widths govern planning. No IERS or other network data were downloaded.

## Targets and principal competing sources

| Target | Gaia DR3 identity | Approximate ICRS direction at J2027.0 (degrees) | T magnitude |
|---|---|---|---:|
| TIC 80387959 | 5362389543781401216 | 165.3106853, −48.6140525 | 10.52 |
| TIC 402358350 | 4318715445843296256 | 295.1511289, +15.6404898 | 9.43 |

Target directions use saved Gaia J2016.0 coordinates and linear proper motion. The packet retains both original coordinates and proper motions; these are finder positions, not new astrometric measurements. Neighbor TIC positions and position flags remain separately labeled because their coordinate epochs and several DR2–DR3 identities are not uniformly established. Confirm identities on an actual finder image before defining extraction apertures.

| Target | Neighbor TIC | Separation | T magnitude | Nominal required eclipse | Optimistic lower requirement |
|---|---|---:|---:|---:|---:|
| 80387959 | 80387965 | 13.76″ | 13.62 | 1.10–1.39% | 0.56% |
| 80387959 | 80387968 | 35.34″ | 15.09 | 4.26–5.38% | 2.16% |
| 80387959 | 80387961 | 7.54″ | 16.70 | 18.86–23.85% | 9.59% |
| 80387959 | 937808821 | 7.39″ | 18.07 | 66.64–84.27% | 33.80% |
| 402358350 | 1918682563 | 10.12″ | 15.87 | 20.59–23.08% | 9.13% |
| 402358350 | 74037550 | 25.46″ | 15.03 | 9.50–10.65% | 4.28% |
| 402358350 | 402358383 | 17.35″ | 17.43 | 87.34–97.90% | 39.26% |
| 402358350 | 1918682446 | 5.24″ | 17.90 | 134.24–150.46% | 11.82% |
| 402358350 | 1918682448 | 8.41″ | 17.64 | 105.53–118.29% | 47.60% |
| 402358350 | 402358249 | 48.11″ | 13.33 | 2.00–2.24% | 0.89% |

Requirements are copied from the [conditional aperture-flux budget](../paper-host-vetting-20261012/ASSESSMENT.md), not measured eclipses. Values above 100% reject only that nominal flux model; optimistic variants reopen the listed faint sources. Uncertain aperture response, source identities, magnitudes and color-dependent dilution prevent categorical exclusion. The optimistic column combines declared stress assumptions and is not a confidence bound. This list prioritizes important competitors; it is not an exhaustive clearance of every modeled or unresolved companion.

The corrected TRICERATOPS catalog uses a different, Gaussian aperture-response model for one sector per candidate. It assigns TIC 80387968 a sector-36 aperture fraction of 0.007582 and an illustrative eclipse requirement of **9.07%**; TIC 74037550 has a sector-54 fraction of 0.004448 and requirement **13.09%**. These are nominal estimates, **not lower bounds**. Separate fields in the packet distinguish them from the four-sector flux-budget ranges above. The [new SkyMapper test](../resolved-followup-803-20261013/ASSESSMENT.md) of 80387968 and [resolved-neighbor investigation](../resolved-followup-402-20261013/ASSESSMENT.md) of 74037550 motivate retaining both in future observations. Neither archival check clears a source automatically.

## Measurement priorities and decision rules

1. **80387959: resolved time-series photometry of the target and TIC 80387965 in the same field.** Include the other listed nearby sources where measurable. A repeatable dip on a resolved neighbor at the predicted phase would strengthen a contaminating-host interpretation. To attribute the TESS dip quantitatively, also measure its passband-dependent depth and show that its captured TESS flux can explain the aperture decrement. A deep neighbor eclipse alone need not be the entire explanation.
2. **402358350: recover the event clock before allocating a short transit track.** The retained expanded-profile envelope requires approximately 18 hours including baseline, beyond a conventional single-night track. A coordinated longer campaign or new independent space-based epoch could test the unchanged prediction; the campaign must preserve the current clock and register timing and negative-result criteria before opening new flux. Any improved clock derived afterward must be labeled a fit to those observations, not their prior prediction.
3. **Measure empirical sensitivity before interpreting absence.** As planning targets, try 60–120-second cadence and an event-depth uncertainty of at most 100 ppm on the primary star. These are requested capabilities, not demonstrated telescope performance. The target signal is only several hundred ppm. For TIC 80387965, an illustrative event-depth precision below 0.11% would give a nominal ratio of five against the 0.56% stress-test eclipse. For TIC 1918682563, the analogous number is 1.83%. Neither ratio is a calibrated detection significance; assess correlated noise, comparison-star stability, saturation, seeing-dependent blending and baseline coverage.
4. **Preserve unresolved alternatives.** Detecting a dip on the primary narrows source identity but does not establish a planetary companion or exclude an unresolved stellar binary. Non-detection on one resolved neighbor only constrains that source, that depth, passband and covered interval. A flat target light curve during incomplete timing coverage does not disprove the candidate. Several repeated well-covered events and appropriately selected imaging or spectroscopy may still be needed.

Resolved photometry is especially attractive for TIC 80387965 because its conditional eclipse is much deeper than the blended target-aperture signal. Whether the target and companions can be separated must be demonstrated from the actual PSF and extraction; their angular separations alone do not certify an instrument's resolving performance. Filter-specific eclipse contrast must be considered when comparing new measurements to TESS.

## Artifacts and verification

- [targets.json](targets.json): target positions, frozen clocks and complete preserved local profile pairs, planning decisions, neighbor requirements.
- [events.csv](events.csv): 64 nominal event opportunities and noncalibrated timing envelopes.
- [neighbors.csv](neighbors.csv): coordinates, magnitudes, conditional eclipse requirements and illustrative precision targets.
- [plan.json](plan.json), [build.py](build.py), [provenance.json](provenance.json): bounded method, reproduction and SHA-256 hashes of every input and generated numerical output. Saved source reports retain original download URLs; no new raw data were fetched.
- [verify.py](verify.py), [verification.json](verification.json): independent decimal propagation, original-gate checks, neighbor arithmetic and Astropy forward UTC-to-BJD round trips. Run `uv run python results/followup-planning-20261013/verify.py`.

The first verifier stopped on exact floating-point equality after division/multiplication by five in one illustrative precision value. Replacing that inappropriate exact comparison with a relative tolerance of 1e-14 passed; no scientific output changed. Verification establishes arithmetic and retained-input identity, not model completeness, confidence coverage, observability or attainable sensitivity. No observation was obtained, reserved epoch opened, observer contacted or external entry submitted.
