# TIC402358350: no common large pointing excursion in the eight fixed event windows

Cached light-curve telemetry from sectors40/41/54/81 was tested at the unchanged expanded primary clock. None of the eight event windows has a large mean pointing or centroid offset relative to its local residual scatter in these diagnostics. Background behavior differs between events. This does not establish instrumental cleanliness, a host or a planet; it supplies no coherent shared pointing/background explanation for all eight dimmings under the tested model.

Five channels were retained for every event: SAP_BKG, POS_CORR1/2 and MOM_CENTR1/2. A local linear trend is fitted outside one duration but within three; its mean in-window residual is divided by the outside residual scatter. The statistic is a descriptive ratio, not an error on the mean or a Gaussian significance. All channels vary; no constant placeholder column was mistaken for evidence of stable pointing.

Controls use the same local fits at eight predetermined offsets of±0.2,±0.3,±0.4 and±0.5period, excluding true-transit neighborhoods from control samples and baselines. In/out counts must each be within20% of the original event's counts. Coverage failures and unmatched controls remain saved. Depending on event, zero to seven controls survive. The±0.5period windows and other controls can repeat across neighboring events; they are not independent draws or a survey false-alarm distribution.

| Event | Background offset/scatter | Matched controls with at least that absolute ratio | Largest absolute pointing/centroid ratio |
|---|---|---|---|
|S40 event0|−0.92|4/4|0.38|
|S40 event2|−0.40|4/4|0.50|
|S41 event3|−0.82|3/7|0.34|
|S41 event4|0.19|1/3|0.48|
|S54 event33|−1.46|3/7|0.32|
|S54 event34|−1.21|No count-matched controls|0.55|
|S81 event95|1.79|0/3|0.16|
|S81 event96|0.01|6/6|0.33|

S81 event95 has the largest background ratio and exceeds its three matched controls, but that small correlated comparison is not calibrated significance. Its other channels are modest, and the next81 event lacks a similar background offset. S54 event34 has no count-matched controls, preventing an empirical comparison there. No event was excluded, no clock was refitted, and no favorable subset replaced full-data photometry or images.

The matched-control plot was visually inspected. Independent centered scalar regressions reproduce285 usable event/control measurements and verify count matching, constant-channel flags and control ranks. Input hashes and fixed timing are retained. The analysis uses only cached light-curve telemetry, not an independent pointing reconstruction from pixels. Rapid excursions averaging to zero, nonlinear backgrounds, aperture changes and common detector effects outside these channels remain possible. Existing image-source ambiguity and timing caveats remain; prior SAP/PDC and source fits were not rerun.
