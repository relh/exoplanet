# TIC 5546257: new QLP sectors 89 and 99

**Dimming recurs at the unchanged expanded pre-sector62 clock in both newly opened epochs.** Sector89 gives271 ±28ppm and sector99 gives239 ±33ppm with the primary1.5-day detrending. Both predictions still fail the predeclared timing-precision gate, so these are informative nominal-clock recoveries, not passed frozen validation. The original coarse discovery clock does not recover the dips. Nothing in these target light curves resolves the host; the [resolved-neighbor Gaia evidence](../extension-402358350-5546257-20261012/ASSESSMENT.md) remains particularly relevant.

## Preserved prediction and measurements

The [plan](plan.json) was saved before either flux download. It records the exact two products from the parent's metadata query, prior opened sectors9/35/36/62, history/cache/process preflight, both immutable clocks, all saved timing-profile pairs, quality masks, processing choices and decision gates. No ephemeris was fitted to the new observations. The coarse seed has no saved uncertainty profile and is explicitly inconclusive.

| Sector | Detrending | Expanded-clock depth, ppm | Supported events / measured events | Timing spread / allowed half-duration |
|---|---|---:|---:|---:|
|89|1.5 d|271 ±28|10/13|0.1070 /0.06653 d|
|89|2.5 d|283 ±29|9/12|0.1069 /0.06653 d|
|99|1.5 d|239 ±33|5/8|0.1224 /0.06653 d|
|99|2.5 d|221 ±36|4/7|0.1224 /0.06653 d|

Supported events have local formal SNR≥2, using the unchanged event windows. The total expanded-clock formal SNR is 9.84/9.89 in 89 and 7.16/6.17 in 99. Event-scatter errors are 23/26 ppm and 45/47 ppm respectively; these reveal additional variation but are not calibrated red-noise errors. The original seed gives depths−37/−28 ppm in 89 and−57/−16 ppm in 99. All eight clock/window/sector combinations remain labeled `timing_prediction_inconclusive`; none of the unfavorable seed results is discarded.

The [inspected folded plot](fixed-clocks.png) shows a coherent dip near the expanded prediction and displaced from the original seed prediction. Its bins are for display only; native-cadence data provide measurements. [Results](results.json) retain every measured event, expected formal sensitivity, and phase-offset control. Controls are dependent and not a survey false-alarm probability.

## Processing differences and source limits

Both FITS products provide `DET_FLUX` and published `DET_FLUX_ERR`; no missing-error fallback was needed. There are 11,156 quality-zero finite positive pairs in 89 and 7,005 in 99 before our cleaning. Both use BJD−2457000 in TDB. The frozen analysis separately applies the existing 1.5/2.5-day flattening at native cadence.

QLP adopted TGLC processing starting with sector94, according to the [official MAST release description](https://archive.stsci.edu/hlsp/qlp). We preserve the complete [sector89 headers](headers-s89.json) and [sector99 headers](headers-s99.json). The column names remain the same, while `BESTAP` changes from `3.0:4.0:3.0` in89 to `3x3 square` in99, with corresponding smaller/larger aperture definitions changing too. This is not proof that every contaminating source was removed. Depth differences can reflect processing, aperture throughput or dilution; they do not establish intrinsic evolution, a planet or an on-target origin. Alternate aperture columns were recorded as metadata and not selected after viewing their flux.

The new epochs extend recurring dimming, while the independent resolved-neighbor Gaia investigation makes off-target contamination more plausible. That report also retains a potential mismatch/alias in the neighbor's catalog period. These QLP target data alone do not decide that alias or determine the neighbor's orbit.

## Verification and evidence

[verify.py](verify.py) passed784 checks. It verifies frozen input hashes, access chronology, FITS identity/time context, raw masks and reconstruction through the existing flattening; independently recomputes total, individual-event and phase-control depths/errors with QR; checks supported-event counts and scalar timing-profile propagation; and confirms all eight inconclusive classifications. Flattening and the FITS reader are shared implementations, so this is arithmetic and provenance verification, not independent astrophysical validation. [Verification record](verification.json).

The two raw FITS files and download manifests are isolated in ignored `data/new-epochs-5546257-20261012/`; committed results retain source URLs, retrieval times and SHA-256 hashes. The new sectors are now opened evidence and cannot be reused as fresh holdouts. Both downloads and the bounded analysis completed. No new clock search, pixel acquisition, shared scientific-code edit or external submission occurred.
