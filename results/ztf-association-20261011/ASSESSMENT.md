# ZTF source associations and duplicate-time audit

All ten retrieved ZTF reference-image positions are closest to the intended target among the Gaia scene entries already queried. There are no same-filter pairs within two seconds among the1903 quality-zero, finite, positive-error measurements, including comparisons across separate object IDs. These checks support using the records for follow-up; they do not establish a transit or exclude blended photometry.

| Target | Separation from Gaia reference position | Nearest other returned Gaia source, minimum separation |
| --- | --- | --- |
| TIC422626648 | 0.290–0.314arcsecond | 24.07arcseconds |
| TIC241928959 | 0.022–0.209arcsecond | 9.86arcseconds |
| TIC196681132 | 0.199–0.328arcsecond | 35.24arcseconds |

The table uses Gaia's stated reference positions, not an assumed ZTF epoch. ZTF objra/objdec are reference-coadd positions; the effective reference epochs are not supplied in these records. Linear target-position propagation over2016–2026 is retained as a range diagnostic in results.json, without fitting an epoch to minimize separation. It omits parallax and is not a per-exposure astrometric verification. The earlier large offsets from the TIC catalog do not indicate a different nearby source in this returned Gaia scene.

The duplicate audit compares all quality-screened records within each target and filter, retaining original HMJD timestamps. The two-second threshold exceeds the schema's0.864-second timestamp quantization. No records were removed. Absence of near-identical timestamps is not proof of independent noise or of unique exposure identifiers: the exported schema lacks exposure IDs, and correlated calibration effects may remain.

verify.py independently recalculates30 reported angular separations using the haversine formula and checks every same-target timestamp pair by brute force. All checks pass, and input/export hashes match. No scientific measurement module changed. The association comparison covers only returned Gaia entries and cannot exclude unknown or unresolved sources or photometric contamination.

The cloud/TAP observation-count discrepancies remain unresolved. HMJD time-scale verification and conversion are still needed before a precise frozen-TESS-window test; no period, phase or depth was searched here. No new candidate is promoted.
