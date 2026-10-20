# TIC284383833: deprioritized discovery peak on a known rotational variable

The13.0788462-day screening pass is a poor new-planet lead after discovery-only review. The target is an **exact identifier match** to the VSX rotational variable Gaia DR3 1204798632166244096. Its selected minima sit in broad, asymmetric undetrended variations; one of the three formal supporting events is an edge-truncated feature and disappears from the original transit window with longer detrending. This favors stellar variability/processing over a stable isolated transit, without proving the star has no planets or assigning a calibrated probability.

Only already-cached sectors24/25 were read. Added51 and reserved78 were not downloaded or opened, and their light-curve caches remain absent. The parent batch was confirmed live during this review; no generic follow-up was run.

## Evidence

- [Discovery record](discovery.json): period13.078846225288412d, box duration0.18d (the screening grid maximum), BLS depth779.49ppm, formal SNR10.586, correlated-noise-adjusted heuristic SNR7.555. Three screening events have depths510.65,1203.65,894.38ppm and formal SNR3.51,8.17,6.08. The first center is only0.094d from the cleaned edge. These were screening measurements, not independent validation.
- [Exact identity](identity.json) and [VSX response](results.json) establish that the sole60-arcsec VSX result is the target itself, through the shared Gaia DR3 identifier. VSX labels it ROT and supplies no period; we do not claim an exact13.08d catalog-period match.
- [NASA TOI and confirmed-planet queries](planet-catalogs.json) completed successfully and returned zero exact-TIC rows. This limited nonmatch is not exhaustive novelty evidence.
- At the unchanged original clock, independently reconstructed local-baseline depths are862.68±84.09ppm with1.5d detrending and1015.35±105.35ppm with2.5d detrending. The latter has only two usable events because the longer edge mask removes event0. These local-baseline values differ from the original BLS/global-baseline depth by construction.
- The campaign's separately searched2.5d alternative was13.1042625d and1198.92ppm; it is retained in discovery.json but was not adopted as a new clock in this review. Do not mistake its stronger formal significance for fresh confirmation.
- [Folded plots](discovery.png) and [individual events](events.png) were visually inspected. Event0 lacks a complete local baseline; event2 has several broad neighboring excursions; event3 sits at an asymmetric change in the undetrended baseline extending well beyond the0.18d box. The plots support a variability concern, not a quantitative stellar/planet odds estimate. “Raw quality flux” in the plot means the quality-selected PDCSAP input before our flattening, not uncalibrated detector counts or SAP.

## Disposition and next action

Deprioritize this searched interpretation; do not promote it to the README's unresolved planet shortlist. A definitive astrophysical false-positive classification is not established, and known rotation alone would not exclude a superposed planet. Given the combined morphology and edge dependence, new source downloads or opening51/78 are not currently justified ahead of stronger leads. Revisit only with a specific test capable of separating the broad variability from a repeatable compact transit, retaining the original-clock negative evidence.

## Reproduction and limits

Run `uv run python results/review-284383833-20261011/verify.py`. [Verification](verification.json) checks discovery/raw/source hashes, exact catalog identity and saved CSV parsing, reconstructs both cached discovery reductions, and independently recomputes weighted total/event depths and errors: five event measurements across two windows. It does not independently reimplement detrending, rerun the global search, validate the source or calibrate noise/planet probabilities. Catalog queries, their raw URLs/hashes and raw-data provenance are retained in the linked records; downloaded responses remain under ignored `data/targeting/`. No shared source, docs or candidate submission was changed by this worker.
