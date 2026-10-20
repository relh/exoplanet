# HARPS pilot, 2026-10-10

64 seeded targets downloaded from1489 RVBank entries passing4000–6500K, V<10.5,
distance<100pc, excluding positions within60arcsec of current NASA confirmed
planets and the externally reported HD32564. This does not exclude all published
candidates or establish underexploration.

Only six targets have at least30 usable observing nights and150days baseline.
Three-component circular screening uses a trend, pre/post-upgrade offsets and
2m/s white jitter, with a0.8–100day period grid. Results are exploratory peaks,
not candidates. Large variations and near-daily aliases predominate:

| Target | Nights | Initial leading period(days) | Assessment |
|---|---:|---:|---|
| HD192865 |37|1.2497|Sparse; requires activity and alias checks|
| HD27536 |39|1.0419|Near-daily alias; requires activity/longer-period analysis|
| HD19230 |66|0.9974|Near-one-day peak; sampling/long-period ambiguity|
| HD85119 |37|1.1705|Sparse; requires activity and alias checks|
| HD13357 |52|47.5557|Large RV amplitude; requires binary/long-period checks|
| HD138799 |40|0.9963|Very large RV variation; no planet promotion|

The remaining58 are not searched because they fail this pilot's sampling cuts.
No planet candidate is promoted. Future RV selection should prioritize published
well-sampled series rather than randomly drawing from the mostly sparse archive.
Raw source URLs/hashes, selection seed and known-planet catalog provenance are
preserved in selection.json/downloads.json; screening.json records every target.
