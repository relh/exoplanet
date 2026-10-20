# Retrospective mask-aware re-screen

Only the three mixed-mask stars from the original32-star cohort were reprocessed.
Instrument offsets distinguish CCF mask and pre/post-fiber configurations; nightly
bins do not mix masks. Original results remain in rv-coverage-search-20261010.

GJ9255's full model still predicts worse than a baseline on the old test sample.
HD85512, a known activity false positive, also predicts worse. HD297396's periods
remain near4.2689/0.9923/0.8742d, but its first-component prediction improvement is
weak(+5.63 under training-refined nuisance periods). No new candidate is promoted.

The test nights had already been opened. This is a sensitivity reanalysis, not
fresh blind validation, and no threshold was calibrated on these repeated checks.
