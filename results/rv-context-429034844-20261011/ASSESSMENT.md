# TIC 429034844: Gaia radial-velocity variability strengthens the binary alternative

The exact TIC Gaia-DR2 identifier2750531317313142528 maps uniquely in the retained neighborhood response to Gaia DR3 source2750531317313142528. The original raw Gaia CSV and parsed JSON agree exactly for this row. This examines previously downloaded spectroscopy-related fields, adding physical context to the TESS image and timing evidence; it is not a new independent observation campaign.

| Gaia field | Value |
|---|---:|
| Robust radial-velocity range |95.04051 km/s|
| RV observations |22|
| Observations involving spectral deblending |19|
| RV time span |1010.459 days|
| RV renormalised goodness of fit |22.57065|
| RV constancy p-value as stored |0.0|
| RV template temperature |4000 K|
| Median RV and reported uncertainty |−13.0559225 ±6.596504 km/s|
| RVS magnitude |11.878106|
| RUWE |1.5581727|

The source satisfies the recommended catalog variability criteria: p<0.01, goodness of fit>4 and at least10 observations. Its template is also within the conservative3900–8000 K range discussed in the [Gaia RV validation paper](https://www.aanda.org/articles/aa/pdf/2023/06/aa44220-22.pdf). The [official data model](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) defines the robust range after outlier removal, rather than an orbital semi-amplitude; the RV error describes the combined median, not an individual epoch. Deblended observations used at least one deblended CCD spectrum. Catalog p=0 is finite-precision output, not literal zero probability.

This substantial catalog RV variability strengthens a stellar-companion or blended-spectrum explanation for a system with short-period eclipse-like dips. It does not establish an orbital period, companion mass, or which component produces the TESS dips. Nineteen of22 RV observations required deblending, a material caveat. We have neither fitted epoch velocities nor demonstrated phase alignment with0.466995 days or its doubled period. An unrelated longer-period companion or contaminated spectroscopy remains possible.

The source has non_single_star=0 and no released epoch-RV, RVS-spectrum or epoch-photometry flags. These are availability/catalog flags, not evidence against a binary. Earlier empty photometric classifier/EB queries must not be interpreted as absence of variability: the main-source RV fields supply a distinct diagnostic.

Disposition: binary/blended-spectrum alternative strengthened; no likely new planet. Preserve target-region localization and original inconclusive reserved timing tests. Before a planet interpretation, spectroscopy contamination and the relation of velocity variability to the eclipse clock need resolution. A tighter photometric timing grid alone cannot resolve this.

[Extracted evidence and hashes](results.json) · [Reproducible extraction](run.py) · [Verification](verification.json). Existing raw-download provenance and identity were verified; no science algorithm or timing fit changed, and no new full-suite test claim is made.
