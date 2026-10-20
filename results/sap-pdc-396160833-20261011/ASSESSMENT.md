# TIC396160833: discovery dip exists in SAP as well as PDCSAP

Using the same initial quality/finite-positive mask, the fixed refined clock and
identical separate detrending, both discovery-sector flux products show a dip:

| Window | SAP depth / formal SNR | PDCSAP depth / formal SNR |
|---|---|---|
|1.5days|306ppm /12.34|179ppm /9.88|
|2.5days|318ppm /12.64|192ppm /10.29|

Each measurement has27 in-window points. These are local-baseline weighted
measurements, not the BLS objective's reported box depth; small numerical
differences from the earlier discovery/refinement are not new epochs or retiming.

The feature is not confined to PDCSAP, so a correction-only artifact is less
plausible. This does not distinguish astrophysical dimming from instrumental
signals already present in aperture flux. SAP is extracted aperture photometry,
not unprocessed pixel data. Both reductions share the photons, and their common
dip is not independent confirmation. The deeper SAP signal also demonstrates
processing-dependent depth; no companion radius is revised from it.

Only sectors18/19 were reanalyzed. The negative/inconclusive sector25/79 tests
remain unchanged, and this result does not upgrade the signal to a credible
planet candidate. Source localization, background/pointing correlations and
other instrumental causes remain unresolved.

`verify.py` reconstructs all four measurements and cleaned arrays from raw FITS,
checks input hashes and common initial masks. Separate detrending can retain
different clean points; the per-product counts are preserved. The plotted
comparison was inspected. No threshold or period was reoptimized in this check.

The test suite passed49 tests in35.28s.
