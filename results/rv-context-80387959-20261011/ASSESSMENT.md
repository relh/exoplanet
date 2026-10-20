# TIC80387959: available Gaia RV context does not resolve the transit host

The four previously tested host hypotheses were checked against their TIC Gaia identifiers, newly queried DR2-to-DR3 neighborhood mappings and the retained raw DR3 source CSV. Each maps uniquely to the source used in the earlier analysis. This adds spectroscopy-related catalog context to the unresolved4.19217-day signal; it does not repair the conflicting pixel/PRF host tests.

| TIC | RV km/s | RV observations | Constancy p-value | Renormalised RV goodness of fit | Interpretation |
|---|---:|---:|---:|---:|---|
|80387959|7.02097 ±0.32064|26|0.17881|0.44365|Does not pass suggested variability cuts|
|80387965|−6.66485 ±4.84510|29|Unavailable|Unavailable|Variability diagnostic unavailable|
|80387961|Unavailable|Unavailable|Unavailable|Unavailable|Unavailable|
|937808821|Unavailable|Unavailable|Unavailable|Unavailable|Unavailable|

The target has a5000 K RV template and a997.7128-day time span;10 of26 observations involved spectral deblending. Its robust catalog RV range is5.955348 km/s. This number is not a semi-amplitude or a companion-mass measurement, and does not override the nonsignificant catalog constancy diagnostic. TIC80387965 has9 deblended observations among29, but its combined-RV error is not an epoch scatter or variability detection. None of the four has released epoch RVs or RVS spectra according to these source flags.

The [official Gaia data model](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) suggests p<0.01, renormalised goodness of fit>4 and at least10 observations for selecting potential RV variables. Missing values are unavailable diagnostics. Failing the cuts does not demonstrate constant velocity or exclude a companion: no sensitivity, orbital phase coverage or mass bound was calculated here. RUWE0.8283 for the target and zero non-single-star flags are not planet validation.

Disposition: Gaia supplies no strong RV-variable flag for the target under this criterion, but cannot resolve the competing neighbor hypotheses. The recurring TESS signal remains unresolved; no likely planet promotion or exclusion is justified. Further work needs genuinely discriminating host information or a new viable search sample, rather than repeating these catalog summaries.

[Identity mappings](mapping.json) · [Extracted values, missing fields and cuts](results.json) · [Reproducible query](run.py) · [Verification](verification.json). Original raw source CSV and new mapping download are hash-verified; no scientific search algorithm changed or new full-suite test claim is made.
