# Closely spaced reserved-sector pilot

The first 16 stars completed: 15 below threshold, one flagged, no errors and no fits eligible under either follow-up policy. No new planet candidate is established. TIC16041227 has variability, comparable inverted signals, large duty cycles and inconsistent event depths; its periods near0.504,1.003 and0.519 days are retained as rejected screening evidence.

All139 previously unused multi-sector stars had discovery/reserved splits frozen before opening photometry. Selection preserves original metadata order, takes the longest consecutive discovery block leaving at least one sector reserved, and breaks ties toward the latest block. These stars lack the earlier eight-sector separation criterion. Nearby reserved sectors provide a shorter prediction test, not an independent observing-year test. The remaining123 stars are still unopened in this QLP cache. “Unused” is scoped to this investigation, not a literature claim.

The first three stars, selected before screening, received24 exposure-integrated box injections before detrending. Periods were0.83 and2.37 days, duration0.04 days and fixed phase0.317. At one Earth radius none of six trials recovered the period or passed. At two Earth radii two of six recovered, one passed the non-crowding screen. At three/four Earth radii all12 recovered and eight passed that screen. All14 period recoveries also passed the three-point phase diagnostic. Crowding flags are retained; passing this screen alone cannot establish a candidate. Baseline arrays matched exactly at both detrending windows.

These three controls each use a single discovery sector. They do not measure multi-sector sensitivity or survey completeness. Fixed boxes and a tiny parameter grid omit realistic limb darkening, eccentricity and source contamination. The small-planet failures prohibit an Earth-sized-planet absence claim. Screening thresholds were unchanged.

`verification.json` checks139 metadata splits, input/source hashes,16 target identities and raw hashes, both empty terminal follow-up records, unopened reserves and24 injection result hashes/grid bounds. The initial verifier incorrectly expected the injection status label `complete`; the pipeline uses `screened`. That schema assertion was corrected without changing scientific results. No scientific algorithm changed; no new pytest result is claimed.

Next: search the remaining123 frozen targets with the same gates, retaining held sectors for eligible fits and documenting all negative results.
