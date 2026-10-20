# Independent TESS image-epoch coverage check

TESScut’s position-based sector service returns only91 for TIC422626648,92 for TIC241928959 and91 for TIC196681132. These are the already-opened discovery epochs. Request coordinates, raw response hashes and returned sectors were independently checked. No photometry was opened by this metadata query.

This strengthens the existing coverage limitation for these positions in the current service. It does not establish absence from every mission, alternative archive or future TESS release. TIC positions were not proper-motion propagated. The three unresolved signals still lack an independent TESS epoch through this service.

A separate3arcsec ZTF light-curve query was launched with the existing TESS clocks and hashes frozen beforehand. Downloaded data will require source identity, quality, blend and time-system checks plus extrapolation uncertainty before any independent recovery claim. Merely returning ground-based points is not a validation.
