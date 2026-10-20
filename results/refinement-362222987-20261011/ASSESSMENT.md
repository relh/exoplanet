# TIC 362222987: discovery-only clock refinement

Refined peak 0 using only the original sectors 17–18, with the existing follow-up routine and max_sectors=0. No held-out photometry was loaded. Frozen period 8.924437042 days, epoch BTJD1772.34868016544, duration0.18144 day, box depth195.30 ppm. The 150 conditional period/epoch profile pairs span8.917038810–8.931736631 days and do not touch the refinement boundary.

Timing is already a limitation: illustrative propagation50 days after the reference gives a0.10090-day spread, exceeding the0.09072-day half-duration; at1500days the spread is1.29942days. These calculations are not sector observations. The profile ignores red noise and competing period aliases. A later-sector nominal non-detection alone may therefore be inconclusive. Preserve this frozen clock for any later tests, without optimizing on the reserved sector.

The discovery and raw training hashes were verified, and sector85 was absent from cache at this check. The freeze records source hashes and its creation time.

Reproduction: call `exoplanet.followup.follow_target(Path('results/review-362222987-20261011/discovery.json'), new_output_path, max_sectors=0)` with the source versions hashed in `frozen.json`. Output must be a new directory.
