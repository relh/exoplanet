# QLP-expanded target selection, 2026-10-10

**288 additional untouched stars** have viable adjacent QLP training sectors and
separate reserved epochs. The selection is frozen in `selected.json` before
photometry downloads. This expands coverage beyond the earlier SPOC-based
selections, reaching Sector104. The directory's historical `qlp-only` name does
not mean these stars lack every SPOC product.

From the same60,026-star TIC small/nearby sample, after original physical/crowding
cuts and exclusion of all previously selected/opened targets and exact known
catalog matches,29,549 targets remained. We queried QLP metadata for the first
2,000 ranked by the original radius/brightness proxy. All eight250-target MAST
queries completed with row-count/hash checks.1,930 stars have QLP products;
288 have an adjacent pair plus a sector at least eight sector numbers away.

The earliest qualifying adjacent pair is training; all sufficiently separated
other sectors are reserved. Training pairs span Sectors3–104. The2000-target
metadata sample is not a random sample, a completeness estimate, or evidence
that other astronomers have not studied these stars. Catalog exclusion is exact
ID-based; promising signals still need alias/positional and contamination checks.

`../campaign-qlp-expanded-20261010` runs all288 with10-minute bins and published
uncertainties, searching0.5–20d. The maximum permitted training baseline is120d.
QLP's missing aperture-crowding estimates remain an explicit flag; peaks passing
all other checks are review priorities, never automatic planet candidates.

Early failures show usable Sector103 flux with all-NaN published uncertainties.
For example TIC303655974 has8,663 quality-zero positive-flux points there and
zero usable error values; Sector102 has7,862 usable flux/error pairs. Original
failures are preserved. A separate empirical-error recovery is required before
claiming coverage of these targets; failure is not a null detection.

Final outcome:287 usable searches and one unusable target, all processes terminal.
[Final audit and limitations](../audit-qlp-expanded-20261010/ASSESSMENT.md).
