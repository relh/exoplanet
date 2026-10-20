# TIC387338903: apparent periodic strength is dominated by a background-correlated event

The locally refined9.7337-day signal is dominated by event2 near BTJD1514.345 in sector7. That event contributes97.9%/97.7% of positive event-SNR-squared across the two detrending settings and measures about2312/2322ppm with formal SNR34.2/34.6. Other measured dips are much smaller; odd/even mismatch is15.2/13.6sigma. These conditional diagnostics do not support a consistent repeated transit.

A posthoc omission removes the entire orbital cycle containing event2, retaining the original fitted period, epoch and duration without refitting. The remaining fixed-clock depths are **93.7±23.9ppm (SNR3.93)** and **89.4±24.0ppm (SNR3.73)**. Some positive evidence remains, but it does not preserve the original high significance or establish a planet.

The raw two-day event window shows a sharp background spike at the deepest flux dip, with another background excursion and alternating brightening/dimming shortly beforehand. The dominant dip itself has quality-zero samples; a nearby earlier exposure has nonzero quality and missing flux. Both SAP and PDC exhibit the structure, but they share photons and are not independent evidence. Raw centroids evolve across the window. The plotted telemetry was inspected. This strengthens a background/instrumental concern, without proving a specific cause or excluding an unrelated isolated astrophysical event.

The two unchanged-clock omission measurements reproduce; all exported raw columns reconstruct from the hashed sector7 FITS file. Nonfinite raw values are retained as JSON null rather than discarded. Two initial reporting failures (NaN serialization and a final console-summary dictionary lookup) are documented; scientific calculations were unchanged. Sector72 remains unopened.

The9.73-day interpretation is deprioritized. This is not a confirmed single-transit planet or an exclusion of all planets around the star. No additional source or independent-epoch claim is made.
