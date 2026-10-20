# Alternate-product coverage of unused stars

Exact numeric target-name queries for SPOC and TESS-SPOC completed for1885 targets:1485 with one previously returned QLP sector and400 with none. All19 query chunks completed and their returned row counts match MAST pagination totals.1108 have no exact-name match,768 only the previously known sector, and9 have additional epoch metadata. No light curves were opened.

| TIC | Previously returned QLP sectors | Additional product sectors |
| --- | --- | --- |
|139637952|32|106,107|
|469011270|45|1751|
|98672442|3|107|
|138935386|98|6,32|
|59598282|45|1751|
|166749887|4|105,106,107|
|307989555|21|1751|
|124186757|33|107|
|146343560|none|106,107|

These are search opportunities, not candidate signals. NASA’s [observation dates](https://heasarc.gsfc.nasa.gov/docs/tess/sector.html) identify1751 as the January15–22,2026 special3I/ATLAS observation. Its label must not be used to infer chronological order or ordinary sector length. The source page and retrieval hash are retained. The short span limits transit repetition and timing tests.

`audit.py` independently reconciles all1885 requested identities, source hashes, complete response/pagination counts, provenance filters and nine additional-epoch records. An exact-name nonmatch does not prove no observations exist: alternative target names and other products were not queried. Different processing of the same sector shares photons and is not an independent observing epoch.

Next: recover stellar metadata and freeze discovery/reserved product choices for these nine before opening light curves. Check FITS identity, quality and temporal coverage, especially1751. Preserve the existing screening gates and negative evidence. Known-object/source checks remain necessary for any promising signal; catalog availability does not establish novelty.
