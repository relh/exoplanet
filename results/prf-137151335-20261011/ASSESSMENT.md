# Known shallow-planet control: source rankings are not reliable vetoes

Known Kepler-93 b (TIC137151335) is recovered photometrically at4.72674days and204ppm. Applying the unchanged source-comparison procedure to its two discovery sectors gives inconsistent rankings: the target wins sector40, but neighbor TIC137151319 wins sector41. This does not reclassify the known planet. It demonstrates a material limitation of this diagnostic at shallow depth.

| Sector | Preferred hypothesis | Best chi-square / dof | Target chi-square / dof |
|---|---|---:|---:|
|40|Target137151335|321.60 /117|321.60 /117|
|41|Neighbor137151319|389.91 /117|430.74 /117|

The target wins all six sector40 event-omission stacks and all nine tested registration offsets. Sector41 favors137151319 in five omissions and137151306 in one; all nine registration offsets prefer137151319. Individual-event rankings vary widely in both sectors. Thus even registration-grid stability and repeated omissions can accompany a wrong/unsupported source interpretation in a known-planet control. These tests are correlated and model-conditional.

The inspected image comparison shows large structured residuals, including unrelated stamp-edge structure and positive/negative residuals near the star. Neither sector has an adequate whole-image fit under its diagonal formal errors. Scene fractional residual RMS is0.91%/0.68%. The comparison does not establish a calibrated host probability or false-rejection rate. This one selected control is not a representative sensitivity study.

The simple sector40 moment routine initially failed on one event with no positive difference weight. That failure is retained. All twelve event images, including the failed-moment event, are retained in the PRF analysis with signed coefficients. Raw difference arrays and membership reproduce; an independent QR solver reproduces494 hypothesis fits, with raw and mission-PRF hashes checked. Matched synthetic registration succeeds numerically but does not validate real-data source accuracy. Reserved sector75 remains unopened.

Implication for new signals: unstable source rankings with poor residuals support an **unresolved attribution**, not a standalone planet rejection. TIC469309982 and TIC267545898 remain uncertain and have additional photometric concerns; their image behavior alone cannot establish a false positive. Strong, consistently displaced signals with much better neighbor fits (such as TIC22972044 sector7) carry different evidence, but still require explicit model-quality assessment. Keep all favorable evidence and avoid treating any PRF-ranking heuristic as a validated physical classifier.
