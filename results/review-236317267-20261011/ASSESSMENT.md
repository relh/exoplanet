# TIC236317267: compact discovery signal warrants source and later checks

The2.1971798-day signal remains an unresolved transit-like lead, not a planet discovery. Its compact folded dip persists under alternate detrending, but the discovery significance is concentrated in sector24; sector25 is noisier and weaker. Source attribution, later repeatability and false-positive checks remain undone. Internal APC is appropriate if listed, with this asymmetry retained prominently.

Only already-opened discovery sectors24/25 were used. Added51 and reserved78 remain unopened; their light-curve caches were verified absent. The live parent batch's terminal audit must precede any opening, followed by a frozen timing/decision plan.

## Discovery evidence

Original BLS period2.1971797863d, duration0.092d, depth530.56ppm, formal SNR9.38. At this unchanged clock the local-baseline combined depths are545.87±62.05ppm and581.54±65.68ppm for1.5/2.5d detrending; each reduction has seven events with formal SNR≥2. Local-baseline depths differ from BLS's baseline by construction. The alternate global search selected2.19719135d and605.23ppm, consistent within the coarse discovery period family; it was not adopted as a new clock here.

| Detrending | Sector24 depth±error(ppm) / SNR | Sector25 depth±error(ppm) / SNR |
|---|---|---|
|1.5d|613.14±71.90 /8.53|346.76±122.82 /2.82|
|2.5d|643.14±75.84 /8.48|390.65±131.45 /2.97|

All seven individually supported events occur in24. Sector25 has positive aggregate dimming but no individual SNR≥2 event. The1.5d sector-depth difference is about1.87 formal sigma under independent white errors, so this is a limitation rather than a demonstrated contradiction. Combined half-phase depth is−14.52±63.64ppm in the original diagnostic; no detectable secondary there does not exclude diluted binaries. Event consistency and beta1 are conditional screening statistics, not calibrated likelihoods.

[discovery.png](discovery.png) was visually inspected: a compact shallow dip with relatively flat nearby folded baseline persists in both reductions. The underlying short baseline and coarse30-minute discovery cadence limit ingress and source interpretation.

## Catalogs and verification

SIMBAD identifies the exact target as Gaia DR3 1316215203425174400. VSX within60arcsec and NASA TOI/confirmed-planet tables by exact TIC returned zero rows, with successful schemas and raw responses retained. These nonmatches are limited catalog checks, not proof of novelty or absence of variables.

[verification.json](verification.json) records raw/source/catalog hashes, exact identity, two preprocessing reconstructions and32 independently recomputed event measurements across the two windows. [sectors.json](sectors.json) preserves independent precision-sum checks of each sector total. The arithmetic verifier shares the existing detrending routine and does not rerun the global search or calibrate astrophysical probabilities. Run `uv run python results/review-236317267-20261011/verify.py` and `uv run python results/review-236317267-20261011/sectors.py`.

Next: discovery-sector source localization, then a properly frozen additional-sector timing test after terminal batch reconciliation if the source evidence warrants it. No shared scientific source, docs or candidate submission changed in this review.

## Subsequent discovery-image evidence

Subsequent preliminary discovery difference images show strong flux about3.4pixels off target in both sectors. This supersedes the initial planet-priority suggestion: deprioritize an on-target planet pending neighbor identification. Image source SNR is not photometric transit significance. See [sector24](../pixels-236317267-s24-20261011/), [sector25](../pixels-236317267-s25-20261011/). No added or reserved sector was opened by this review.
