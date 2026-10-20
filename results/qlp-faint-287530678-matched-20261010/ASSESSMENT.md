# TIC287530678: same-exposure reduction disagreement

The Sector63 disagreement persists when comparing matched native exposures.
Nearest-time matching within5seconds yields9024unique pairs; the measured timing
offset is approximately1.974seconds versus200-second cadence. Original timestamps
and the frozen QLP ephemeris are retained, without period or phase adjustment.
There are45in-event matched samples in each comparison.

| Matched native series | Depth | Formal error | SNR |
|---|---:|---:|---:|
| QLP | 0.005056 | 0.001126 | 4.49 |
| SPOC PDCSAP | 0.000553 | 0.000987 | 0.56 |
| SPOC SAP | 0.000354 | 0.000885 | 0.40 |

QLP points outside the match also show a dip, so merely selecting a different
set of timestamps does not explain the discrepancy. SPOC raw aperture flux (SAP)
as well as corrected flux (PDCSAP) lacks the corresponding dip under identical
median detrending. A PDC correction alone therefore does not explain this result.

This is additional evidence against promoting the QLP screening lead. It is not
independent photometry: all reductions share underlying images, uncertainty
estimates are conditional, and the matching tolerance was chosen post-hoc after
inspecting timestamp offsets. Different apertures or source contamination remain
possible. No physical source attribution, definitive stellar classification,
planet exclusion or false-alarm probability is claimed. Reserved epochs beyond
the previously opened10/11 were not used.

All input hashes, FITS integrity evidence, measurements and per-event results are
retained. Raw data are unchanged. The native comparison also avoids the earlier
QLP ten-minute binning versus native SPOC sampling difference.
