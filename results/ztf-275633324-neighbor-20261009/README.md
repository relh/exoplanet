# TIC 275633324 contamination check

ZTF photometry at neighboring TIC 275633326 shows deep recurring dimming near
the original 1.265539-day TESS eclipse phase in g/r. Original discovery timing
was saved before downloading these data. The fixed-window fitted magnitude
changes are 0.0452/0.0178 mag (formal S/N 10.9/7.2), but folded eclipses are much
deeper and smeared: the short original TESS baseline does not ensure precise
phase prediction over all ZTF years. No period refinement has been applied.
The group-intercept fit's formal errors do not include that model mismatch.

Combined with offsets in TESS 14/15, contamination is supported. Neighbor-template
pixel controls improve Sector 15 agreement; neither template explains Sector 14
perfectly. No calibrated source probability or binary characterization follows.
Reserved TESS Sectors 57/60/84 remain unopened. A longer training-only ephemeris
could test the match more sharply, but would now be a post-inspection analysis.

Raw download source, hashes, request, script, processed data and plot are retained.
Timing/magnitude method matches the separately archived 399450592 neighborhood
analysis, including midpoint MJD UTC -> BJD TDB and per-object intercepts. The
analysis embeds a deterministic eclipse-plus-offset recovery check.
