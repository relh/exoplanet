# TIC402358350: dimming persists in aperture and corrected flux

The periodic dip is present in SAP (aperture) as well as PDCSAP (corrected) flux in each already-opened sector40/41/54/81. Under these fixed-clock tests it does not require the PDC correction to appear. This is a descriptive comparison of shared photons, not independent detection or proof of an astrophysical origin or host.

All16 sector/reduction/window measurements use the same expanded primary11.769544332-day clock, epoch2392.99286894 and0.144-day duration. No clock is refit or chosen by the test. The plan and input hashes precede analysis. A common quality-zero, finite-positive mask for both reductions is applied before separate identical sector-local detrending; final cleaned coverage can differ. The2.5-day PDCSAP81 result is therefore a new same-clock processing comparison, not a replacement for the previously frozen2.5-day alternative-clock test.

| Sector | SAP1.5day depth(ppm) | PDC1.5day depth(ppm) | SAP2.5day depth(ppm) | PDC2.5day depth(ppm) |
|---|---|---|---|---|
|40|683±93|606±76|698±93|608±76|
|41|730±76|534±77|752±76|551±76|
|54|606±79|744±84|645±103|740±115|
|81|629±64|635±72|661±64|636±72|

Combined fixed-clock depths are648±38ppm(SAP) versus621±38ppm(PDC) for1.5-day detrending and688±40ppm versus615±40ppm for2.5-day detrending. These combined values reuse discovery and training data and are not independent confirmation significance. Reduction-dependent amplitudes and errors may reflect dilution, correction, baseline and noise differences; this calculation does not correct them into intrinsic transit depths. No model has identified which star supplies the dip.

The inspected eight-panel comparison retains both reductions, all sectors and their noise. Raw and corrected curves both show central dimming. Instrumental effects shared before PDC, blends and eclipsing binaries are not excluded. Existing timing-inconclusive81 prediction and source-localization ambiguity remain unchanged.

Verification reconstructs16 raw/common-mask/detrended arrays, independently checks their total/event depth arithmetic and four combined measurements, and verifies fixed-clock identity and input hashes. The initial Astropy `checksum=True` call warned about extension checksums. These products lack DATASUM; the repository's documented byte-level FITS checker supports CHECKSUM without DATASUM and verifies all12HDUs. The warning and resolution are preserved in `verification.json`; no raw files were modified and no warnings were interpreted as missing astronomical data.

No downloads, additional observations, scientific-source edits or period optimization were performed. The method does not provide a calibrated false-positive or planet probability.
