# Sector 104 offset repeats in two chronological event groups

The first four locally measurable events give a positive difference feature
with maximum formal S/N 13.19 and moment 1.062 pixels from the target. The last
four give maximum formal S/N 7.22 and moment 1.211 pixels from the target.
Both inspected maps place the feature in the same off-target direction.
The original full-image difference and uncertainty were reproduced exactly
before splitting, using the existing difference-events and centroid functions.

This supports repeatability within the discovery sector and strengthens the
contamination concern. It does not uniquely resolve the nearby faint sources
or provide calibrated astrometric confidence. The chronological groups were
fixed before measuring them, but the ephemeris and common centroid region
were selected from the original full data. Thus this is a post-selection
diagnostic, not an independent validation set. Background covariance and PRF
mismatch are not modeled by the formal errors. No phase or background tuning
was used, and no new photometry was opened.

See plan.json, results.json, images.npz, and split.png for groups, hashes,
numerical results and retained images. The failed Sector 103 image remains
unchanged and supplies no cross-sector localization.
