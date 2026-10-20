# TIC96166003: sector59 disagreement follows clock choice more than detrending

Both fixed expanded clocks were crossed with both detrending windows and SAP/PDCSAP reductions, using only already-opened19/43/44/59. Sector59 dimming persists at the primary clock across all four processing combinations, while the sensitivity clock yields near-zero or negative measurements in each. Thus the earlier mixed nominal59 comparison is primarily sensitive to the alternative ephemerides, not simply a PDC correction or change of detrending window. This does not establish which clock or astrophysical interpretation is correct.

| Sector59 processing | Primary depth ± error(ppm) | Sensitivity-clock depth ± error(ppm) |
|---|---|---|
|SAP1.5day|264.0±51.5|−15.7±56.0|
|PDCSAP1.5day|264.9±51.9|−74.5±56.4|
|SAP2.5day|243.4±56.9|−30.7±61.9|
|PDCSAP2.5day|260.3±57.2|−72.4±62.4|

The primary formal SNR ranges4.28–5.13. This positive evidence survives the tested processing choices and is retained. It cannot override the original1.35-day timing spread or select a preferred profile island after seeing59. The original frozen outcomes remain timing-inconclusive. The sensitivity clock also has a different duration; the comparison separates whole fixed timing/shape hypotheses from processing, not period alone.

The plan predates this analysis but follows inspection of59. Both clocks themselves were frozen before59. This factorial check is therefore retrospective, not another blind test. Every sector has separate results, and combined totals remain in `results.json`; totals mix discovery and fitted training data with59 and are not independent confirmation significance. All reductions share photons, and flux dilution/noise/baseline corrections can alter depths.

The inspected per-sector comparison plot preserves all32 measurements, including unfavorable ones. No original clock, phase, duration or event selection was changed. No new observations were downloaded. Source attribution, correlated noise and whether the dip is planetary remain unresolved; no numerical planet probability follows.

`verification.json` reconstructs raw identities/hashes and masks, all processed arrays,32 sector total/event measurement sets and8 combined sets using independent precision-sum arithmetic. It checks the two exact pre59 clocks and byte-level FITS checksums. Arithmetic agreement is not independent astrophysical validation. No earlier cache-absence verifier was rerun after the deliberate59 opening.
