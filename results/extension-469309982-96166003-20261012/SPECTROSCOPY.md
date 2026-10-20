# Spectroscopy metadata extension: no matched observation in the checked releases

Ten-arcsecond cones around both exact TIC coordinates return valid empty tables in RAVE DR6 (`III/283/ravedr6`), APOGEE DR17 (`III/286/catalog`), GALAH DR3 (`J/MNRAS/506/150/stars`) and LAMOST DR7 low-resolution general, AFGK-parameter and medium-resolution general tables (`V/156/dr7lrs`, `dr7slrs`, `dr7mrs`). Thus these specific releases supply no newly matched spectrum or stellar/RV parameter row. No source association, binary exclusion or planet probability follows. This is not an exhaustive search of every later survey release or unpublished spectrum.

The cones use the already verified exact TIC coordinates, with a 10-arcsec margin to accommodate ordinary epoch/proper-motion offsets. No returned neighbor was silently substituted for the target. LAMOST general tables were checked as well as the parameter table so absence of fitted AFGK parameters alone was not conflated with absence of a listed observation.

Sources: [RAVE DR6](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=III%2F283), [APOGEE DR17](https://www.sdss4.org/dr17/irspec/dr_synopsis/), [GALAH DR3](https://www.galah-survey.org/dr3/the_catalogues/), [LAMOST DR7](https://dr7.lamost.org/). Even a single matched RV would supply context rather than establish velocity constancy; here no such measurement was obtained.

The initial guessed GALAH table suffix `galahdr3` returned no TABLE element, an invalid route retained explicitly. A TAP table-name lookup located `stars`; both corrected cones return real schema-bearing empty tables. These two initial responses are not counted as scientific nonmatches. `spectroscopy-cones.json` and `spectroscopy-recovery.json` preserve all 14 cone responses, URLs and hashes; extracted CSVs retain the 12 valid empty schemas. The independent XML verifier checks raw hashes, actual TABLE/TR elements and errors, distinguishing the two invalid routes from 12 empty results. `spectroscopy-verification.json` passes. The earlier bibliography assessment remains intact.

No flux, light curve or spectrum was opened, and no shared files were changed.
