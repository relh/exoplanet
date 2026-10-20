# TIC 198186473: matched Sector 83 exposures

The post-hoc check preserves the frozen native QLP ephemeris and the predeclared
five-second matching tolerance. QLP and each SPOC flux series have 6,004 unique
matched exposures. The fixed-event measurements all use 19 in-event points:

| Reduction | Depth (ppm) | Formal SNR |
|---|---:|---:|
| QLP | 14,645 ± 1,472 | 9.95 |
| SPOC PDCSAP | 151 ± 1,230 | 0.12 |
| SPOC raw SAP, detrended identically | −469 ± 1,202 | −0.39 |

No usable event measurement remains in the excluded QLP points. Matching removes
unequal event coverage as the explanation for this sector's discrepancy. The
SPOC raw and corrected flux both fail to reproduce the strong QLP dip. Different
apertures, contamination, and reduction artifacts remain possible; this check
does not identify the host or establish a specific instrumental cause.

The reductions use the same images. Their comparison is not an independent
observing epoch. No new reserved sectors were opened or ephemeris refitted.
The signal remains unpromoted, substantially weakened by this discrepancy and
the structured discovery noise. This is not proof that the target has no planets.
Raw-data hashes, provenance and exact measurements are retained in results.json.
