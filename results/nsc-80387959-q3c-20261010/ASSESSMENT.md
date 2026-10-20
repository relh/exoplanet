# TIC80387959: NSC photometry does not sample predicted events

No source attribution or contaminant exclusion from this archive. The public NSC
DR2 query returned15objects and134measurements on27DECam exposures. None falls
inside the existing TESS prediction, even under a generous conditional timing
profile envelope padded by a full exposure on both sides.

The field includes four measurements of TIC937808821 (position match0.12arcsec),
all flagged3 (blending/neighbors), and four of TIC80387965 (match0.16arcsec), flagged
2or3. They are retained under an explicitly relaxed exploratory quality check,
not treated as clean independent eclipse measurements. The target TIC80387959 and
close alternative80387961 are not returned as separately matched objects. Their
absence is not a nondetection or evidence against them. Nearest catalog matches
beyond1arcsec are explicitly not accepted; positions were not motion-propagated.

Exposure metadata had a real VOTable defect: the declared exposure-ID width24 was
shorter than the26-character TABLEDATA strings. Astropy truncated identifiers,
causing the initial exact-ID assertion to fail. That failure is retained. Reading
the original XML TABLEDATA strings recovered all27exact IDs without changing raw
files. Measurement/exposure filters and MJDs then matched; dateobs and MJD agree
within0.000068seconds. Source files, hashes and raw strings remain reproducible.

Interpret dateobs/MJD as UTC exposure start, add half exposure, then geocentric
BJD TDB; omitted topocentric correction<=0.022s. The full-exposure envelope padding
also covers start/midpoint convention sensitivity. No period or phase optimization.
The TESS timing profile is conditional and not a calibrated confidence interval.
No eclipse depth is inferred without phase coverage; strict and relaxed counts
and every original flag are in analysis.json.

Initial standard ADQL geometry query failed on this service; its error is retained
in ../nsc-80387959-20261010. Documented Q3C object-cone query then succeeded, followed
by indexed exact-object measurement and exposure queries. No contacts/submissions.
Official access/schema information: https://datalab.noirlab.edu/data/nsc .
