# TIC 207468583: ZTF coverage is insufficient

The 45-arcsecond query returned 1296 rows spanning MJD 58263.35–60510.30.
After quality filtering, 48 object identifiers remain. No individual object
meets the fixed measurement requirements of at least three in-event points
and five local out-of-event points. The download succeeded on attempt three;
both earlier timeout failures remain in the source manifest.

Five light curves associate with suspected source TIC 207468583 within
0.22 arcsecond (positions not propagated for proper motion):

| ZTF object identifier | Filter | Clean samples | In event | Local baseline |
|---|---|---:|---:|---:|
| 1798116100000856 | zg | 31 | 0 | 5 |
| 1798216100001485 | zr | 63 | 1 | 4 |
| 1798316100001617 | zi | 13 | 0 | 3 |
| 1829103400006022 | zg | 18 | 0 | 1 |
| 1829203400008563 | zr | 58 | 1 | 4 |

The original target's native TESS period, epoch and duration remained fixed;
there was no phase or period optimization. Each object identifier was retained
separately, avoiding assumptions about cross-field offsets or duplicate exposures.
The time conversion and quality selection are recorded in the analysis manifest.

This is insufficient coverage, not a non-detection or an eclipse-depth limit.
It neither excludes an eclipsing neighbor nor supports a planet classification.
The positive TESS Sector 83 recurrence, mixed secondary evidence, and unresolved
host attribution remain unchanged. These returned light curves do not establish
complete coverage of every available ZTF product or every possible contaminant.

[Request](request.json), [source and retry history](source.json),
[all object measurements](analysis.json), [analysis script](analyze.py).
