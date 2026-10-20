# TIC396160833: background ramps accompany all four discovery events

The inspected diagnostics show curved rises in SAP_BKG around all four fixed
centers in sectors18/19. This recurring background evolution is an instrumental
warning, not proof of a causal relation to the flux dips. No correction was
fitted to remove the transit signal, and no planet exclusion follows.

A local linear baseline was fitted outside one duration but within three
durations; the mean residual inside half a duration was compared with the
outside residual scatter. Background offset/scatter ratios are+0.91,−2.96,−1.60,
−1.03 for events0–3. Their signs are not uniform, and a straight-line baseline
is inadequate for some curved ramps. These ratios are not standard-error
significances, calibrated probabilities or evidence of four independent effects.

Position-correction ratios stay within0.73 in magnitude; moment-centroid ratios
stay within1.18. Signs vary between events. This check therefore establishes no
consistent centroid displacement and cannot localize the source or exclude a
blend. Background is in FITS flux units and pointing/centroid channels in pixels;
the plots show median-subtracted values only for display.

The combination of repeated background evolution, the period's proximity to the
observing-block rhythm and lack of convincing recovery in sectors25/79 warrants
continued skepticism. The signal remains unresolved and is not upgraded. A causal
instrumental diagnosis would require pixel/background or ensemble evidence.

`verify.py` independently reconstructs20 local regressions using polynomial fits,
checks hashes and masks. A deterministic synthetic linear-trend/known-offset test
passes in the run script. These verify arithmetic, not an astrophysical noise
model. All discovery data and the frozen clock were already inspected earlier;
no independent validation data were used here.

The test suite passed49 tests in36.37s.
