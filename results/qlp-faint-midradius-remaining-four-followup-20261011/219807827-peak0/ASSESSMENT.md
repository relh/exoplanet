# TIC 219807827: artifact-suspect transit-like diagnostic

The discovery screen admits the peak near 13.021936 days with only the unmeasured-aperture-crowding flag. Native refinement gives period 13.027622 days, duration 0.1584 days and depth 2,605 ± 297 ppm (formal fit error). Three training events have positive local support. The discovery plot was inspected: the folded depression is present amid substantial scatter, gaps and other structure. Selected fit significance is not a calibrated discovery probability.

Reserved sectors 14 and 15 both return timing_prediction_inconclusive, with extrapolated timing spreads approximately 3.192 and 3.148 days. They neither confirm nor reliably exclude the proposed signal. The exploratory off-phase maximum has selected SNR about 4.81; it is not a calibrated false-alarm probability.

Same-epoch source and quality checks now favor an artifact-suspect interpretation. Host attribution and catalog novelty are unestablished. This is not a credible new planet candidate. No submission or external contact has been made.

## Source and processing checks

The inspected raw Sector 84 difference image combines two event windows and is negative across the entire cutout, with broad spatial structure. It does not locate a dimming source. Its reported image moment and formal pixel SNR must not be treated as astrometry or source-identification confidence. The neighboring-star query returned 53 entries; no neighboring variable is identified by this negative image.

The processed Sector 84 pixel check fails because it has fewer than two valid events: all 137 in-event exposures (68 and 69) have quality4096, the automatic stray-light flag. The failure and exact counts are retained. This raises instrumental concerns without proving the precise physical cause.

Sector 83 differs: its first event has 68 quality-zero exposures with finite processed flux and errors. A strict five-second timestamp match excludes the event despite matching 6,012 other cleaned samples, so that comparison alone cannot compare event depths. A separate retained diagnostic matches unique CADENCENO identities instead, with no ephemeris retuning. It matches 9,775 cleaned exposures across each pair of reductions. In that common exposure pool QLP measures 3,013 ± 510 ppm, compared with PDCSAP 597 ± 416 ppm and detrended SAP 540 ± 380 ppm (formal errors). Each product retains its original times, so the event-window boundary includes 69 QLP versus 68 processed points. These estimates show reduction disagreement, not independent confirmation or a definitive astrophysical exclusion.

The same observing photons underlie these products. Together, two flagged later events, a nonlocalizing negative raw image and a weaker first event in both processed flux series favor the artifact-suspect classification. A planet or exact variable source is not established.
