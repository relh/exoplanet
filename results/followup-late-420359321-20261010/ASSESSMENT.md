# TIC420359321: screening pass not promoted

The 10-minute-binned Sectors65/66 screen selected P=11.91464d, duration0.18d,
761ppm, nominal S/N29.1, with no automated flags. Native-cadence refinement gave
11.90286d, 0.216d and 745.5ppm. This is not evidence for a credible new planet:

- The native-cadence [diagnostic plot](discovery.png) shows broad, irregular
  structure around the fitted event, extending well outside the box duration.
- Frozen predictions in previously unopened Sectors12/39 yield -144±79 and
  -26±41ppm. However, propagated training-profile timing spreads are 2.63/1.35d,
  much larger than the fitted event: the original test is **inconclusive**, not
  a precise-ephemeris falsification.
- An explicitly post-hoc scan across the saved training period/epoch profile
  finds a maximum combined held-out depth of only102±33ppm (selected S/N3.08),
  with zero/one individually supported events. It is not a calibrated null
  probability or an exhaustive transit-model search.
- Independent QLP reduction of the same training images measures59±84ppm in
  Sector65 and11±69ppm in Sector66 at the discovery ephemeris. Neither supports
  the ~761ppm SPOC dimming. These are independent reductions, not observations.

Retain the original screen, frozen record, failed/inconclusive checks and QLP
aperture measurements. Status: **unpromoted, likely reduction/variability signal**;
no host localization, planetary interpretation or novelty claim is justified.
