# TIC96166003: selected-family block controls do not reproduce the observed maximum

All120 bounded block-permutation controls yield smaller selected-family BLS maxima than the observed all-sector statistic. This supports continued investigation under these specific randomization models, but is **not** the original discovery-search false-alarm probability, a survey-wide significance, or a planet probability. It does not resolve the host or the imprecise original sector59 predictions.

The observed maximum over the original narrow period family and three durations is49.139 in BLS likelihood units (period0.955530767day, depth236ppm, formal SNR9.60). An inverted-flux search over the same family reaches18.149 (formal SNR5.83). Both are descriptive post-selection comparisons using all already-opened19/43/44/59. The original pre59 primary-clock measurement is retained separately; the all-data best is not substituted into the historical prediction.

| Block length(d) | Exceedances / draws | Conditional Monte Carlo fraction | Binomial95% interval |
|---|---|---|---|
|0.25|0/40|0|0–8.81%|
|0.5|0/40|0|0–8.81%|
|1.0|0/40|0|0–8.81%|

The120 controls comprise40 per distinct block model. They are not pooled to manufacture a smaller upper bound. Intervals describe finite Monte Carlo draws conditional on each generator, not uncertainty in its astrophysical validity. Zero counts cannot establish zero false-alarm probability.

The plan predates null generation. Flux/error pairs are permuted as contiguous blocks within each sector and gap-separated segment, with fixed random seeds and no omitted events. Short within-block structure survives; long correlations and coherence do not. Blocks introduce seams, retain signal fragments and are not guaranteed exchangeable under stellar/instrumental noise. Approximate durations derive from cadence and final blocks can be shorter. The star, period family, detrending and inclusion of all epochs were selected from previously viewed data. This test therefore cannot calibrate the original43/44 full-period search or its target-selection process.

Four separately planned deterministic300/600ppm box injections at two fixed phase offsets were applied to raw quality-screened PDCSAP flux before the same sector-local flattening and selected-family search. All four recover the injected period/epoch; `verify_injections.py` independently reconstructs their masks and repeats the four raw-to-search calculations. These small sanity checks retain existing variability and show processing can recover those imposed signals; they do not measure completeness or validate the null assumptions. The injection plan follows the initial null results and did not alter their statistics or settings.

The inspected histogram plot retains each block model and the inversion comparison. Verification independently rebuilds all120 permutations, checks bijection and sector membership, reconstructs raw/preprocessed data, reruns nine prespecified null searches and both observed/inverted searches. Search reruns share Astropy BLS; this verifies construction and arithmetic, not a second scientific model. No new observations or shared scientific-source changes occurred.
