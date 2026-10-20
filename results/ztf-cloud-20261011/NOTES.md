# ZTF cloud retrieval design

This run uses the ten DR24 object IDs already returned by the direct IRSA catalog queries in ../ztf-catalog-route-20261011. No period, phase, depth or variability selection was made on these photometric records. The TESS ephemerides remain frozen in the original single-sector reviews.

Access follows [IRSA's official DR24 HATS tutorial](https://caltech-ipac.github.io/irsa-tutorials/ztf-lightcurves/). Dependencies are supplied through `uv run --with lsdb --with s3fs`; versions are recorded in plan.json, without changing the project's dependency lock. The compute scheduler is single-threaded to limit concurrent partition memory.

The selected catalog spans three spatial partitions. Metadata access succeeds, and the indexed compute is monitored through its actual tool process handle. Do not interpret a slow compute or API failure as missing observations. Record its terminal outcome separately.

Schema source URL and SHA-256 are in schema.json; schema-fields.json retains the full field descriptions. HMJD is HJD minus2400000.5 at exposure midpoint, truncated to five decimal places. It is not the uncorrected MJD field from the older light-curve API. The schema does not explicitly identify the underlying time scale, so no BJD conversion or narrow transit comparison is justified by this metadata alone. The release notes checked are https://irsa.ipac.caltech.edu/data/ZTF/docs/releases/dr24/ztf_release_notes_dr24.pdf; further timing documentation may be needed.

Raw selected records are exported as named-field JSON under ignored data/ztf, preserving all quality flags. These are serialized selected records, not the original Parquet byte streams; manifests distinguish them. Source object coordinates are reference-image positions and stored as float32 in the cloud schema. Comparison with higher-precision catalog coordinates should allow that rounding. Final source association still needs proper-motion and blend checks.

The audit checks object IDs, filter identities, record counts, quality-zero finite measurements, HMJD coverage and repeated timestamps. It does not classify a transit or reject a planet. Timing uncertainty from the short TESS baseline and potential cross-object duplicates remain relevant.
