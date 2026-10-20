# TIC 80387959: resolved archival test of neighbor 80387968

**Two new SkyMapper measurements show no dimming of TIC 80387968 during one predicted event. This weakens a specific same-depth, flat-bottom eclipse explanation for that neighbor; it does not exclude the neighbor as the host or establish a planet.** Neither candidate grade nor model probabilities should change from this test alone.

TIC 80387968 is 35.34 arcsec from the target, outside the prior 25-arcsec SkyMapper search. Its exact Gaia DR3 identifier is 5362389509421660800; SkyMapper DR4 object 411683754 lies about 0.047 arcsec from its TIC coordinate. Its small catalog proper motion makes the identity secure at these epochs. This is a newly examined resolved series, not a repeated analysis of the previously tested neighbor 80387965.

## Fixed-clock result

The [hashed plan](plan.json) was saved before accessing flux. It retained period 4.192168718052227 days, epoch BTJD 1575.375831123655, duration 0.092736 day, all five original timing-profile pairs and the heuristic epoch floor. No phase, period or duration was fitted to SkyMapper. The 47 detections span 47 images; 43 meet strict quality cuts and 44 meet the separate relaxed cuts. Both selections yield the same two in-event measurements, in one event on 2021-04-25.

| Band | Phase from fixed midpoint | Dimming relative to nine other-night measurements | Formal error |
|---|---:|---:|---:|
| i | −0.01838 day (−26.46 min) | −0.04383 mag | 0.02007 mag |
| z | −0.01795 day (−25.85 min) | −0.01537 mag | 0.01270 mag |

Positive magnitude differences would indicate dimming; both measurements are slightly brighter than their separate same-filter weighted baselines. Each exposure lies within every retained timing-profile transit window, including the heuristic epoch floor and half-exposure allowance. This is a conditional timing assessment, not a calibrated confidence interval. Times use UTC exposure start plus half exposure, converted to geocentric BJD TDB; the omitted topocentric correction is at most 0.022 seconds.

The prior TRICERATOPS sector-36 aperture model assigns this neighbor a flux fraction of 0.007582. Explaining its fitted TESS dip would require an illustrative 9.07% neighbor eclipse, or 0.1033 mag. That is **not a lower bound**: the aperture response is assumed, and colors, eclipse geometry and sector-dependent dilution matter. The SkyMapper formal three-sigma upper differences are 0.0164 and 0.0227 mag. These numbers disfavor an achromatic flat-bottom 0.1033-mag dip at those exposure times. They are not physical upper limits on an arbitrary eclipse: an observation inside the overall transit duration need not sample full depth, particularly for grazing or V-shaped events, and a twice-period binary may alternate eclipse depths.

Only one event was sampled, failing the predeclared requirement of at least two distinct events for repetition or exclusion. There is no simultaneous reference-star calibration; quoted PSF errors omit possible zero-point and blending systematics. Different optical filters need not reproduce the TESS depth. The two colors from one event are not independent eclipse repetitions. The predeclared exclusion gate therefore fails even though the formal precision is useful. [Figure](skymapper-fixed-clock.png), [all measurements and timing decisions](analysis.json), [per-band comparisons](comparisons.json).

## Gaia availability and remaining competitors

Successful exact-ID queries recovered the target, TIC 80387965 and TIC 80387968 in Gaia DR3. All three have `has_epoch_photometry=false` and `phot_variable_flag=NOT_AVAILABLE`; the classification query returns no rows for these IDs. Thus no public DR3 epoch light curve is available for this test through the documented flag. This is not evidence of constant brightness or an eclipse exclusion. Their RUWE values are respectively 0.828, 1.008 and 1.043; ordinary astrometric residuals do not exclude eclipsing companions.

The previously examined TIC 80387965 remains a possible contaminant. Its prior SkyMapper constraints are too weak for the approximately percent-level eclipse explanation; NSC did not sample predicted events. Those results were reviewed and not relabeled as new evidence. Other unresolved blends remain possible. No TRICERATOPS scenario was removed, and no posterior was recalculated from these sparse data.

## Sources and verification

Official [SkyMapper DR4](https://skymapper.anu.edu.au/data-release/dr4/) and [access documentation](https://skymapper.anu.edu.au/how-to-access/) describe its catalogs. Gaia's [epoch-photometry documentation](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_photometry/ssec_dm_epoch_photometry.html) defines availability through `has_epoch_photometry`. Each saved query JSON contains the full request URL, query, UTC timestamp, HTTP status, parsed rows, ignored raw-file path and SHA-256. All five requests succeeded; there were no failed requests. No new TESS observations, external submissions or contacts occurred, and completed search scopes remain complete.

Run `uv run python results/resolved-followup-803-20261013/verify.py` for 219 offline provenance, identity and arithmetic checks. The verifier does not establish calibration accuracy, independently validate the barycentric library, or validate a planet. Experiment scripts live only in this isolated result directory; shared algorithms were unchanged. Existing prior neighbor reports: [SkyMapper](../skymapper-80387959-20261010/ASSESSMENT.md), [NSC](../nsc-80387959-q3c-20261010/ASSESSMENT.md), [TGLC](../tglc-80387959-20261009/ASSESSMENT.md).
