# Gaia lookup leaves the two nearby sources unclassified

The two TIC Gaia identifiers were looked up through the DR2-to-DR3 neighborhood
table before querying DR3. Four neighborhood links connect two DR2 identifiers
to two DR3 identifiers. Each has a close match (0.308 or 1.359 milliarcseconds)
and a roughly 1.977-arcsecond cross-link to the other source. Every mapping is
retained rather than treating all links as unique identities. The brighter
source's identifier changed between releases.

Both distinct DR3 sources are present in gaia_source. Neither appears in the
queried vari_classifier_result or vari_eclipsing_binary tables; both have
phot_variable_flag=NOT_AVAILABLE and has_epoch_photometry=false. This is no
variability classification or public DR3 epoch-photometry support for either
source, not evidence that they are constant or cannot be eclipsing binaries.
The TESS contaminant remains unidentified.

Queries, parsed rows, raw source URLs and hashes are retained for all four
tables. The [Gaia neighborhood documentation](https://gaia.aip.de/metadata/gaiadr3/dr2_neighbourhood/)
explains why source IDs cannot simply be carried between releases. See also
the [classifier table documentation](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_variability_tables/ssec_dm_vari_classifier_result.html)
and [eclipsing-binary table](https://gaia.aip.de/metadata/gaiadr3/vari_eclipsing_binary/).
