# TIC 435878345: initial review

Rounded central depression with an asymmetric deeper portion after the fitted center; eight supported events.

Discovery plot visually reviewed. Refined period 2.974070955 days, depth 0.00248553, duration 0.133056 days, training sectors [57], supported events 8. Original flags retained: ['crowding_or_missing_crowding'].

Reserved sector 17: timing_prediction_inconclusive; timing spread 0.969833 days. This neither confirms nor excludes the signal. Source checks and catalog checks remain pending; no credible new planet or novelty claim.


## Initial source inspection

Both the raw TESScut and processed SPOC sector57 stacks, plus all nine individual event images from each product, were visually reviewed (18 individual maps). Every event shows a compact dimming feature near TIC435878339, away from the target. The raw moment is3.727pixels from the target and0.0515pixels from435878339; the processed moment is3.723pixels from its header target and0.0796pixels from435878339. A faint neighbor TIC611541749 lies about0.23pixels from either moment, so these moments do not uniquely establish the host. Strong neighboring-source contamination is favored over a planet around435878345. Raw/processed formal pixel SNR309/303 are not calibrated host probabilities. These products reuse the same observations and do not constitute an independent epoch.

Events0,1,2,3,5,6,7,8,9 pass unchanged raw gates. Most have57–58 inside samples; event3 has14 quality-zero inside samples and115 baseline samples, excluding one quality128 sample. Other baseline counts are159–230. Event4 has no available inside samples. Nine pixel windows are not nine independent detections; eight events supported the clean QLP fit. Raw FITS SHA256:74d8cbaa96598dd2ccaf76732375ddc0d7d29bde88c124acaafe9713ee19caca. The processed FITS was retrieved successfully; identity, clock, hashes and saved stack/event arrays were independently checked by reconstructing the frozen-clock differences.

The TIC cone returned27 entries. All five catalog sources within3pixels of the raw difference moment have Gaia identifiers; five DR2-to-DR3 mappings lead to five returned DR3 sources. Gaia returned no variability-classifier or eclipsing-binary rows for those sources. Raw CSV and saved JSON agree. This does not exclude an unlisted eclipsing binary, and the target lies outside this moment-centered Gaia subset.

The exploratory secondary scan selected SNR3.17 near phase0.486 after300 trials; it is not independently significant binary evidence. An exact-TIC web search returned no results, not a novelty test. The original reserved-sector test remains inconclusive. Initial source inspection is complete; unique neighboring host and physical cause remain unresolved. No credible new planet is claimed.
