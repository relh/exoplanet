# ZTF neighborhood data

Public IRSA ZTF light-curve API, 3-arcsec cones around the TIC positions. Target
query succeeded after a transient timeout. Original neighbor query failed after
three read timeouts; the separately recorded retry succeeded. Keep both outcomes.
Raw CSVs remain in ignored data/targeting; source manifests retain URLs and hashes.
API: https://irsa.ipac.caltech.edu/docs/program_interface/ztf_lightcurve_api.html

Fixed-TESS-ephemeris analysis now strongly supports an eclipsing contaminant
at TIC 399450579. ZTF object median positions are within 0.08 arcsec of that
neighbor and ~16.8 arcsec from the target. After independent object intercepts,
fixed-window dimming is 0.107/0.112/0.073 mag in g/r/i, supported by 30/166/5
measurements. Formal S/N is 10.6/60.5/7.6, but non-box eclipse structure and extra
scatter make these unsuitable as calibrated significance. Target g-band shows
0.00082 ± 0.00382 mag; this cannot exclude its much smaller proposed TESS dip.

The neighbor varies at the already-frozen TESS period and phase, without a ZTF
period/phase optimization. Combined with discovery-sector image offsets, this
strongly identifies contamination as the explanation. A rough two-star dilution
calculation predicts 532/556/367 ppm if each ZTF depth applied in the TESS band,
comparable to the observed ~500–650 ppm. Bandpass and aperture effects preclude
an exact contamination fit. Binary parameters and possible unresolved structure
of the neighbor have not been determined. No planet claim follows.

Script, processed arrays, original source hashes and figure are saved. The ZTF
schema specifies midpoint MJD; times were converted UTC -> BJD TDB at approximate
P48 coordinates without adding another half-exposure. catflags=0 only; separate
object offsets; original photometry retained. A deterministic injected eclipse
with distinct object offsets is recovered by the measurement routine.
