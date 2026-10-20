# Eclipsing-binary catalog refresh, 2026-10-10

Neither refreshed catalog identifies a listed eclipsing binary within 126 arcsec
of any of the 1,322 new late-sector search targets. Neither has a binary within
360 arcsec of TIC 80387959. The 706 cached TIC neighbors of 80387959 also have no
exact-ID match to the Kostov catalog. These negatives do not resolve its host or
establish planetary nature or novelty.

Sources and reproducible comparisons:

- [Kostov et al. 2025](https://doi.org/10.3847/1538-4365/ade2d8),
  [VizieR J/ApJS/279/50](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/279/50).
  Complete Table3 (7,936 new binaries) and Table4 (2,065 previously known),
  10,001 unique TIC IDs. Their search used TESS Sectors1–82. Retrieved full tables
  via VizieR TAP, with URLs and SHA-256 in `kostov-table*-source.json`.
  `crossmatch.py` checks row counts and compares sky positions, preserving matches
  in `kostov-crossmatch.json`. The separate ~900,000 unvetted machine-learning
  detections were not used as a catalog of established binaries.
- [Live Villanova catalog](https://tessebs.villanova.edu/search): 4,584 returned
  ephemeris entries, 4,578 unique TIC IDs; six stars have two entries each.
  The requested CSV is actually HTML-wrapped text, and the body places sectors
  before coordinates despite the requested-order header. `parse_villanova.py`
  explicitly parses and validates that order, retaining all entries. Raw response
  is cached with URL/hash in `villanova-source.json`; derived records and
  positional comparison are saved in `villanova-parsed.json` and
  `villanova-crossmatch.json`.

Coordinates are compared as published, without proper-motion propagation; the
126-arcsec screening neighborhood is six nominal TESS pixels, not a measured
aperture. Both catalogs are incomplete for faint contaminating binaries. These
comparisons supplement, rather than replace, image-based source attribution.
The downloaded arXiv source archive had no machine-readable tables; the complete
published tables were obtained from VizieR instead. No downloaded code executed.

The same positional check of the original11,851-star selection found15 nearby
catalog entries (`original-search-crossmatch.json`). One is an exact match:
**TIC148894196, P4.939775d, is already in Kostov2025 Table3**. This independently
supports our earlier binary rejection. The other14 entries are neighbors49–123
arcsec away; proximity alone does not demonstrate contamination. None changes
the unresolved status of TIC80387959.
