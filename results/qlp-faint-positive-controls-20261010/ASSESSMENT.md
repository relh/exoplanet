# Fainter-star sensitivity controls

No new planet candidates are claimed by these controls. The two-sector QLP
configuration recovered none of the four known periods among its top three peaks
across eight early/late datasets. Published fixed-ephemeris measurements generally
have low signal-to-noise; native cadence versus ten-minute binning makes little
difference. This is evidence of limited sensitivity, not a completeness measurement.

Four-sector QLP checks were possible for only two hosts, yielding four datasets.
TOI-1680 b appears in the late dataset at 4.802599 days (SNR8.82), below two
stronger artifacts. TOI-715 b appears in the early dataset at 19.284822 days
(SNR7.23). Neither passes every automatic gate. These are period recoveries,
not successful end-to-end candidate promotions. The other two datasets do not
recover the known period. See ../qlp-faint-controls-four-sectors-20261010/.

Two-sector TESS-SPOC checks produced five usable datasets and three HTTP404
failures. TOI-2120 b's early dataset recovers 5.803294 days (SNR7.16), with flags;
no other known period matches. Missing products are not negative detections.
See ../spoc-faint-positive-controls-20261010/.

TOI-1680 and TOI-2120 are inside the new magnitude cut. TOI-715 (T13.5308)
and TOI-2266 (T13.5042) are slightly outside and are boundary controls only.
Their published ephemerides and archive provenance are retained in truth*.json;
fixed-plan.json uses coherent period/epoch/duration from individual solutions.
Period matching within1% is a diagnostic, not independent planet validation.

Discovery policy: prioritize four consecutive QLP sectors ending at or before96,
retain the actual120-day baseline limit, reserve epochs at least eight sector
numbers from every training sector, and inspect all top-three peaks without
lowering quality gates. Freeze selection before opening discovery photometry.
Start with100 stars, then assess data quality and screening yield before scaling.
