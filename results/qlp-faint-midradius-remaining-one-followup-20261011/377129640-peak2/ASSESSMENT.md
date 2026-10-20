# TIC377129640 peak2: target-region eclipselike signal, period unresolved

Sector72 native refinement gives P=2.4615823853 days, duration0.032days and depth3.0805±0.0470% (formal selected-fit error), with eight supported events. Original alternate-detrending and missing-crowding flags remain, so this is diagnostic-only. Reserved sectors45/46 have timing spreads0.05725/0.05542days and inconclusive predictions. Those outcomes neither confirm nor reliably exclude recurrence at the frozen clock.

The native discovery plot at the original seed was inspected. It shows deep regular dips, with three dips per selected 2.46-day cycle. The discovery search also finds0.8205804 and1.6408085days: the former retains inconsistent-event-depth flags and the latter secondary/variability and detrending flags. The refined longer period divided by three is0.82052746days. An off-phase dip near phase0.6653 has depth2.75% and formal selected SNR54.93; this is an uncalibrated diagnostic supporting an alias concern, not an independent detection or proof of a binary. A shorter clock and its doubled-period eclipse interpretation need explicit tests.

## Source images

Both raw and processed sector72 stacks were inspected, followed by all nine raw and eight processed individual maps. The stacks show compact positive differences at the target region; processed moment distance to the catalog target is0.083pixel (raw0.068pixel). These are uncalibrated image moments, not astrometric confidence or exclusion of unresolved blends. All eight processed individual maps retain compact target-region structure. Raw event4 is dominated by a negative field offset; its processed window is fully flagged4096 and excluded. Raw events1/7 have additional extended structure. These exceptions are retained rather than calling all nine raw maps clean.

Raw usable events0–8 contain13 or14 inside exposures and43–56 baseline exposures. Event−1 has14 inside samples all flagged2048. Processed event−1 and event4 each have14 samples all flagged4096, with no quality-zero baseline; the other eight have13/14 inside and42–56 baseline exposures. Raw and processed reductions share telescope photons and do not supply independent epochs.

A22-row neighbor query is retained. The four catalog sources within three pixels of the processed difference moment were queried in Gaia using DR2-to-DR3 mappings. Four source rows and no variability-classifier or eclipsing-binary rows were returned. This does not exclude uncataloged variability, binaries or unresolved companions, and does not establish novelty.

The images support a recurring dimming in the target region at the sampled events, but period aliases, event-depth consistency, a possible eclipsing interpretation and unresolved blends remain. No likely new planet is claimed. Next: fixed shorter/doubled-clock comparisons and parity checks in the already-opened photometry, clearly labeled posthoc; preserve the original inconclusive predictions.

## Shorter-clock comparison

All six panels in folds.png were inspected. At the fixed shorter period 0.8205274617772741 days (the frozen longer period divided by three), sectors45,46 and72 each show deep, recurring dips. Alternating events have similar morphology; the doubled clock 1.6410549235545482 days shows two similar dips per cycle. This does not distinguish a planet from a nearly equal-eclipse binary or an unresolved blend.

The older-sector dips occur approximately0.04 day before the fixed center. Consequently the fixed narrow windows miss their centers and their local baselines include dimming: the reported negative depths in sectors45/46 are biased measurements, not absent transits. Sector72 parity depths are0.0315792 and0.0316304 (formal errors0.0004425 and0.0004431); these overlapping estimates do not exclude binary scenarios. The visually deepest points approach4%, and a box depth is not a physical radius estimate.

This uses already-opened data and a posthoc alias hypothesis. It is evidence for recurrence, not a successful blind prediction; original held-out timing-inconclusive results remain unchanged. Next fit a joint ephemeris with timing uncertainty and compare physically plausible transit/eclipsing models, while checking known-object catalogs and unresolved contamination. No likely new planet or novelty claim.

The verifier checks input/code/raw/plot hashes and four noiseless equal/unequal parity controls. These validate fixed-window arithmetic, not astrophysical classification or realistic noise. Core algorithms unchanged; no new full-suite test claim.

[Reproducible comparison](../../alias-377129640-20261011/ASSESSMENT.md) · [Folds](../../alias-377129640-20261011/folds.png).

## Superseding novelty assessment

Kostandyan, Gigoyan and Gigoyan's March9,2026 preprint, [Three Low-mass M-type Eclipsing Variable Stars Found in the Third Catalogue of Dfbs Late-type Stars](https://www.researchsquare.com/article/rs-9006720/v1), identifies TIC377129640 as DFBS J095623.83+064801.9 and reports eclipsing variability with period0.821301days. DOI:10.21203/rs.3.rs-9006720/v1. The repository's Gaia identity3850549957388322816 also matches its table. The name-based coordinate differs from the TIC position by0.304arcsec.

This is an existing reported signal, not our new candidate. The prior report supports deprioritizing a planetary interpretation; it is a preprint and does not independently validate the physical classification. Its period differs from our posthoc0.820527462days by0.000773538day; no exact timing agreement is claimed. Both analyses use TESS data. Prior Gaia variability-table nonmatches were never evidence of novelty and do not contradict the literature identification.

The original photometry, alias checks and inconclusive frozen predictions remain unchanged. Further fine period fitting is deprioritized for the new-candidate search. The downloaded paper stays in ignored data with URL, retrieval time and SHA-256 recorded; verification checks the exact TIC/Gaia strings, unique Gaia mapping, coordinate proximity and period arithmetic. No new scientific algorithm or full-suite test claim.

[Identity verification](../../literature-377129640-20261011/verification.json).
