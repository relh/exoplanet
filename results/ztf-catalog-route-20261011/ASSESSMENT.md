# Independent ZTF observations: catalog associations found, time series pending

Direct IRSA TAP queries succeeded for all three unresolved TESS target regions. The DR24 catalog returns two source records near TIC422626648, five near TIC241928959 and three near TIC196681132. The summed catalog nobs values are782,989 and1041, respectively. These are catalog counts across filter/field records, not verified unique exposures or downloaded light curves.

The metadata schema query identified ztf_objects_dr24. Each subsequent query requested at most100 objects within3arcseconds of the existing TIC position. All returned rows are preserved, and none reached that limit. catalog-audit.json verifies CSV hashes, exact parsed rows and the cone geometry. Offsets from unpropagated TIC coordinates are2.49–2.50arcseconds,0.31–0.47arcseconds and1.32–1.48arcseconds, respectively. These preliminary associations still require Gaia proper-motion/epoch and neighboring-source checks. Multiple ZTF object IDs can represent one astrophysical source observed through different filters or fields.

All three follow-up light-curve requests using the exact returned IDs and COLLECTION=ztf_dr24 terminated with60-second read timeouts. No automatic retry was made. This is a terminal download failure, not a nondetection or absence of ZTF observations. No light-curve epoch, quality, timing or transit-recovery claim is possible from this run. The previous position-query failures remain untouched.

The original TESS clocks were hashed before these requests and were not adjusted. Earlier propagation estimates already show that narrow predicted windows far from the TESS epoch cannot support strong exclusions. Those limits continue to apply when observations become available.

A distinct route is available: the DR24 cloud collection.properties file downloaded successfully from the official S3-hosted collection. Its URL and hash are in cloud-metadata.json. This verifies metadata access only, not access to the light-curve partitions. Next work can retrieve the selected IDs via the cloud catalog and audit their observations before any photometric comparison.

Documentation consulted: [IRSA light-curve API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_lightcurve_api.html) explains ID requests and collection selection; [IRSA's DR24 cloud tutorial](https://caltech-ipac.github.io/irsa-tutorials/ztf-lightcurves/) describes the separate HATS catalog and indexed access. Downloaded raw metadata remain under ignored data/ with committed manifests. No external submission or contact was made.
