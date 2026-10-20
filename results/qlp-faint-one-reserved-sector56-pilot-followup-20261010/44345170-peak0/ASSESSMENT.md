# TIC 44345170: likely neighboring-source contamination

A screening-eligible Sector 56 QLP signal has a native refined period 5.831666915637 days, epoch BTJD 2828.496294464757, and duration 0.1584 days. Four supported events give a local depth of 7,358 ± 340 ppm. The native discovery plot was visually inspected: it shows a localized dip with positive shoulders and substantial scatter. It does not establish the host.

The only reserved sector, 83, gives 941 ± 369 ppm at the fixed prediction. Its conditional timing spread is 0.44292 days, exceeding the duration; the held-out conclusion is timing_prediction_inconclusive, not confirmation or rejection. No extra archived target sector is in the frozen metadata selection.

Same-epoch fixed-ephemeris processing comparison gives QLP 7,274 ± 340 ppm versus SPOC 207 ± 297 ppm. This strong processing dependence raises an aperture, contamination or processing concern; both products use the same images. It neither identifies a contaminant nor alone excludes a planet.

The TIC cone returned 67 entries. Both raw TESScut and processed SPOC difference images were visually inspected. Four event windows produce a compact positive feature away from the target. The raw moment is 2.747 pixels from the target and 0.190 pixels from TIC 44345176. The processed moment is 2.642 pixels from the catalog target and 0.101 pixels from that neighbor. Per-event processed moments cluster in the same off-target region. These are local difference moments, not calibrated PRF confidence intervals; formal pixel SNRs of 72/108 do not give host probabilities.

Two raw-image spatial-background checks (2- and 3-pixel source masks, 50 and 16 fitted background pixels) preserve the compact peak at pixel (6,8), 2.345 pixels from the target. Both background plots were visually inspected. The raw image has a negative baseline, but the positive neighboring feature persists after both background fits. Same photons and approximate catalog positions remain limitations.

TIC 44345176 has Tmag 14.3483 and maps from Gaia DR2 to DR3 source 1884450062564855936. Gaia classifies it as ECL and lists an eclipsing-binary frequency 0.26645245252983984/day (period 3.75301481 days). That period does NOT match the 5.83167-day TESS signal; the Gaia label supports a variable-neighbor hypothesis but does not establish that the same eclipse period was recovered. The target is classified SOLAR_LIKE. All three queried DR2-to-DR3 mappings and the faint nearby source 2040097639 are retained; absence of its variable entry is not exclusion.

The neighbor QLP query provided no Sector 56 or 83 product. Both missing-product errors are retained, not interpreted as null light curves. No independent neighbor-aperture recovery was obtained.

Taken together, processing dependence and consistently displaced compact pixel residuals favor neighboring-source contamination over a transit on TIC 44345170. TIC 44345176 is the leading positional hypothesis, but the catalog-period mismatch and possible faint blend prevent uniquely identifying the physical variable or its period. No new planet or novelty claim is made. Further resolution would require validated source separation or spatially resolved time-series photometry.
