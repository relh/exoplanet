# TIC 430216116: no exceedances in 48 conditional shuffle controls

None of 48 shuffled discovery light curves exceeded the original maximum dip-search power: 0/16 at each of 0.5, 1 and 2-day block lengths. This supports continued investigation of the discovery signal, but does not validate a planet or establish a small survey-wide false-alarm probability. In particular, zero successes in this small sample does not imply zero false-alarm risk.

The existing routine preserves flux/error pairs and short contiguous runs within gap-separated segments, with deterministic seeds, then searches the same period/duration domain for a maximum. It does not run all downstream screening gates. Block seams, disrupted longer correlations and surviving signal fragments limit the control family. Many stars were searched, adding a selection effect not calibrated here.

verify.py checks raw and code hashes, all 48 permutation bijections and count accounting, reproduces the observed search and independently reruns one control at each block length. The other 45 outcomes are reconciled without rerunning. Only discovery sectors 43–45 enter these controls. Independent-sector and source-attribution results must be assessed separately.
