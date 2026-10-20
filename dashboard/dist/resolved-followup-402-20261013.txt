# TIC 402358350: resolved-neighbor follow-up

**All 72 fixed-clock comparisons are inconclusive.** New ZTF photometry provides no convincing eclipse at the saved TESS predictions, but timing uncertainty prevents excluding this neighbor. This extension examines TIC 74037550 (Gaia DR3 4318715445843282432), an eligible contaminating source 25.46 arcsec from the target. The candidate remains unresolved. No target-planet probability or source attribution follows from archive access alone.

## Measurements

All six frozen streams were retrieved: **836 raw measurements, 545 passing quality cuts**. The 72 comparisons cover six individual streams and three combined filters, four unchanged clocks and both time-scale interpretations. Every comparison fails the timing and/or event-count gate. None of the fitted dips or brightenings exceeds 1.70 times its formal error. No period or phase was retuned.

For the expanded primary clock under the UTC interpretation:

| Band | Quality samples | Samples in predicted events | Fitted dip | Scatter-adjusted error | Timing-profile spread |
|---|---:|---|---:|---:|---:|
| g | 141 | 3 in 2 cycles | −1.29% | 1.04% | 0.1527 d |
| r | 355 | 1 in 1 cycle | −1.74% | 2.42% | 0.1518 d |
| i | 49 | 0 | Unmeasurable | — | 0.0942 d |

Negative fitted depths mean slight brightening. Timing spreads exceed the 0.072-day half-duration in every listed band; the additional time-scale difference is about 0.000801 day. The g/r sampled depths would be sensitive to the nominal 13.09% eclipse at approximately 12.6/5.4 scatter-adjusted error units **if** the predicted times and TESS-to-optical depth transfer were accurate. They are not established, so those sensitivity figures are not eclipse exclusions or evidence for an on-target planet.

The [diagnostic plot](ztf-diagnostic.png) shows percent-level scatter and sparse coverage, with no convincing fixed-phase eclipse. One r-band measurement falls near relative flux 0.883, outside the nominal transit window; an isolated low point without recurrence does not identify an eclipse. We did not search for a different period around it. [All measurements](ztf-results.json).

## Source and access

The existing TRICERATOPS catalog assigns TIC 74037550 T=15.0253 and a nominal aperture flux fraction 0.00444756. Explaining the model's 582.2-ppm total-flux decrement would require a 13.09% intrinsic eclipse. That is a model-dependent TESS-band estimate, not an observed eclipse or a measured contrast limit.

Exact Gaia DR3 metadata give G=15.582, parallax 0.5509 ± 0.0314 mas and RUWE 0.986. Its epoch-photometry flag is false; this indicates unavailable DR3 epoch photometry, not constant brightness. The target's parallax is 8.5321 ± 0.0167 mas, so the neighbor is not simply a same-distance bound companion. Neither the parallax nor normal RUWE excludes an eclipsing background star. SIMBAD returns no exact-source identity record in the bounded query; no novelty claim follows.

IRSA TAP returned HTTP 200 with a VOTable database error (`ORA-12541: TNS:no listener`). The raw response is retained as an error. The [official cloud alternative](https://caltech-ipac.github.io/irsa-tutorials/ztf-lightcurves/) subsequently returned six object records in g/r/i within 0.061 arcsec of the Gaia position, totaling 836 listed epochs. The metadata projection excluded the light-curve column and all timestamps. Two additional Gaia sources in the five-arcsecond cone are about three arcseconds away and more than four magnitudes fainter. Positional association does not guarantee uncontaminated photometry.

The known pulsator TIC 402358249 and TIC 1918682563 were already investigated in the [prior external follow-up](../web-402358350-20261012/ASSESSMENT.md). Their inconclusive tests remain in force; those flux series were not downloaded again. The target's previously failed ZTF association and unavailable Gaia epoch flag also remain unchanged.

## Frozen policy

The [plan](ztf-plan.json) and SHA-256 digest precede access to all six selected cloud streams. Four saved TESS clocks and their timing profiles are retained unchanged. All streams and bands are included; no period or phase search, outlier clipping or favorable-stream selection is allowed. Catflags must equal zero and errors must be finite and positive. Each stream has its own normalization and intercept; combined fits are within filter only. Duplicate timestamps within one second retain the lowest OID deterministically.

HMJD is converted through Palomar heliocentric correction to barycentric TDB under both UTC and TDB interpretations. A usable fixed-clock comparison requires the saved timing-profile spread plus time-scale ambiguity and one second to be smaller than half the event duration, and at least two distinct predicted events sampled. A conditional sensitivity discussion additionally requires a modeled eclipse/scatter-scaled-error ratio of at least five. Failure of any timing or coverage gate is inconclusive even if a nominal fold looks favorable. The earlier sector-81 timing failure (0.09142 day versus the 0.072-day gate) remains a separate unresolved concern.

## Verification and completion

[Metadata verification](metadata-verification.json) passes 23 checks of raw response hashes, exact identities, six positional associations, frozen inputs and the required-eclipse arithmetic. [Photometry verification](ztf-verification.json) passes 563 checks, independently reconstructing quality selections, heliocentric-to-barycentric times, event counts, saved timing-profile propagation, QR fits and scatter-scaled errors. Verification reproduces the calculations; it does not validate the source model or the candidate. The six-stream diagnostic figure was inspected.

Raw responses and exported cloud rows are retained under ignored `data/resolved-followup-402-20261013/`, with query URLs, timestamps and SHA-256 hashes in the adjacent manifests. JSON cloud files are exported representations, not original Parquet bytes. Retrieval uses pinned `lsdb==0.11.0` and `s3fs==2026.9.0` in an ephemeral uv environment; shared repository dependencies were not changed. The fetch, analysis and QR verifier are adapted from the previously reviewed ZTF experiment, with all six new streams and three filters retained. No new TESS epoch, external submission or contact occurred. This bounded extension is complete; earlier completed goals stay complete.

**Next discriminant:** precise resolved photometry covering the full current timing uncertainty of the 11.77-day event, measuring the target and relevant neighbors together. The present archival observations do not securely place an eclipse on TIC 74037550 or eliminate it. Other neighboring and unresolved companion scenarios also remain.
