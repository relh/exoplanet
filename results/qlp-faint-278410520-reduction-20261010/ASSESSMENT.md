# TIC 278410520: reduction-dependent depth

The frozen 2.982123829-day ephemeris was applied unchanged to discovery
Sectors 64–67. QLP gives roughly 5,100–5,700 ppm in every sector.
Available TESS-SPOC Sectors 65/67 give 1,427 ± 383 and 2,059 ± 467 ppm;
combined formal SNR is 5.69. Sector 64/66 TESS-SPOC URLs returned HTTP 404;
these are unavailable data, not non-detections. This is the same underlying
imagery, not independent observations or planet confirmation.

Two post-hoc native-cadence comparisons then matched unique exposures within
5 seconds, retaining original timestamps and the frozen ephemeris:

| Sector | Common exposures | QLP depth (ppm) | SPOC corrected depth (ppm) | SPOC raw SAP depth (ppm) |
|---|---:|---:|---:|---:|
| 65 | 9,848 | 5,560 ± 471 | 1,514 ± 387 | 1,340 ± 346 |
| 67 | 7,373 | 5,337 ± 561 | 2,059 ± 467 | 1,703 ± 415 |

The common samples contain 281 and 239 in-event points respectively. Both
SPOC reductions retain positive dips, but their depths are much weaker than
QLP. Different time coverage alone does not account for this, and SPOC's
PDC correction alone does not explain it because raw SAP is also weaker.
The uncertainties share images and must not be treated as independent.

Aperture differences or contamination are plausible explanations, not proven
ones. Source attribution remains essential. The signal is still an unresolved
screening lead, with all earlier timing-inconclusive tests retained.

[Initial comparison](results.json) ·
[Sector 65 matched evidence](../qlp-faint-278410520-matched-s65-20261010/results.json) ·
[Sector 67 matched evidence](../qlp-faint-278410520-matched-s67-20261010/results.json).
Each directory retains its executable script, preread plan and source hashes.
