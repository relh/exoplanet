# TIC5546257: the known neighbor's catalog clock does not explain the selected dip train

The1.767290230-day TESS signal is not a matching harmonic of the7.248263937-day Gaia eclipsing-binary clock for neighboring TIC5546242. Fixed catalog-phase comparisons and even exploratory epoch-fitted harmonic folds do not reproduce the strong, repeated selected dips. The image evidence favoring the neighbor remains a separate source association; it must not be described as a demonstrated match to this catalog binary's ephemeris.

This is a new bounded clock comparison on already-opened sectors9/35/36/62. Previous reports established the period mismatch qualitatively but did not perform this test. No new observing sector, target photometry download, pixel reanalysis, period optimization or source-model ranking was performed. It does not establish an on-target planet or exclude additional variability in the neighbor/system.

## Frozen clocks and arithmetic

[plan.json](plan.json) predates calculations and retains the immutable candidate clock, existing Gaia row, raw FITS and code hashes. The exact Gaia frequency is0.13796407093363958/day with formal error0.000008243307/day. Its reciprocal is7.248263937TCB days with linear propagated period error0.000433081day. Gaia's reference time uses BJD(TCB)−2455197.5; primary/secondary phases refer to that reference, and durations are phase fractions. These semantics follow the [ESA data model](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_variability_tables/ssec_dm_vari_eclipsing_binary.html) and [Gaia@AIP metadata](https://gaia.aip.de/metadata/gaiadr3/vari_eclipsing_binary/). Documentation access provenance and errors are retained in documentation.json.

Astropy converts the reference/eclipses and interval into TDB/BTJD. The nominal eclipse epochs are441.251925 and444.130351BTJD, with widths0.386399 and0.778829day. TCB/TDB conversion changes the period by only~0.000000112day; it cannot repair the mismatch.

Among Gaia period divisions1–8, the nearest isP/4=1.812065956day, **0.044775726day (2.5336%) longer** than the candidate. Four candidate cycles accumulate0.179102904day mismatch against one Gaia orbit; the fourth-harmonic beat timescale is71.5219days. Enumerating frequencies|m/P+k/day| for m1–8 and k−2…2 still finds the unshifted fourth harmonic closest, differing0.013981725/day. This is a bounded common-harmonic/daily-alias check, not an exhaustive spectral-window or all-alias proof.

## Photometry comparison

Common quality/finite-positive masks were used for SAP and PDCSAP before separate1.5/2.5day detrending. Catalog epochs were held fixed; an additional comparison fitted **only epoch** at exactlyP,P/2,P/4 with candidate duration0.133056day. Those epoch fits are explicitly exploratory using all opened data. No profile maximum replaces the original candidate prediction.

| PDCSAP,2.5day reduction | Depth ± formal error, ppm | Formal SNR | Supported events |
|---|---:|---:|---:|
|Unchanged candidate clock|321.1±16.5|19.42|30|
|Gaia primary, candidate-width box|18.6±33.2|0.56|0|
|Gaia secondary, candidate-width box|−74.5±33.9|−2.20|0|
|Gaia primary, published-width box|−30.9±19.6|−1.57|0|
|Gaia secondary, published-width box|6.9±14.1|0.49|1|
|GaiaP, epoch fitted|151.0±34.8|4.34|2|
|GaiaP/2, epoch fitted|101.7±23.8|4.28|4|
|GaiaP/4, epoch fitted|88.7±17.2|5.16|9|

The alternate1.5day PDCSAP candidate SNR is19.63; fitted-period alternatives give4.18,3.98,4.09. SAP candidate SNR is18.58/17.89. All measurements, including per-sector and individual-event results, remain in results.json. These local-baseline formal SNR values are not likelihood ratios between equally flexible models, independent tests or planet probabilities.

The candidate's supported events span many Gaia orbital phases. With2.5day PDCSAP, only5/30 candidate event windows overlap either nominal Gaia eclipse window;9/30 overlap after expanding by an illustrative three formal timing errors. Across all four reductions the corresponding counts are3–5/26–30 nominally and6–9 after expansion. Centers are **predictions at the unchanged candidate clock**, not individually fitted minima. Frequency error was propagated from Gaia's reference plus phase error in quadrature; covariance, eclipse-width uncertainty, Gaia model error and real ephemeris evolution are not calibrated. These are descriptive mismatch counts, not rejection probabilities.

## Retained competing feature and limits

SAP with2.5day detrending does show a broader depression in the Gaia secondary window:114±14ppm, formal SNR8.33, versus SNR3.33 at1.5day and0.49/0.58 in PDCSAP. Sector9 contributes strongly (249±27ppm,SNR9.14);35/36/62 are weaker (SNR1.91/2.89/2.28). This is potentially relevant to actual binary contamination, but the broad feature is processing-sensitive and its published-width box/baseline is vulnerable to detrending. It is not silently discarded, nor equated with the narrow1.76729day train. No assertion that the Gaia binary is absent follows from weak corrected-flux folding.

The inspected [figure](clock-comparison.png) shows a clear candidate-phase dip in both flux streams; the Gaia-phase SAP feature and dispersed candidate-event orbital phases remain visible. Nearby binary contamination is still plausible from images. What fails here is the specific uncomplicated explanation that the **saved Gaia clock or these simple harmonics** accounts for the selected recurring TESS dips. Other periods, a catalog error, multiple variability components, a different close source or inadequate image calibration remain possibilities. Resolving those would require a separately scoped discriminant, such as resolved neighbor epoch photometry or a validated source response; this experiment did not obtain it.

## Verification

[verify.py](verify.py) reconstructs all four stream/window reductions from four hashed raw FITS files; independently recomputes1310 weighted depth/error measurements including1150 event measurements; checks nearest-cycle timing, Gaia conversion/harmonic arithmetic and overlap counts; and reproduces12 epoch-only searches. Flattening, Astropy BLS and time conversion are shared implementations, so verification establishes arithmetic/provenance, not independent astrophysical validation. `verification.json` passes. The report preserves the original candidate clock, catalog period, all unfavorable alternatives and source uncertainty. No shared scientific code or documents changed.
