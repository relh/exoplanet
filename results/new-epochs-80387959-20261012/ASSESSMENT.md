# TIC 80387959 sectors 64 and 99: collateral pixels, not usable stellar epochs

**Neither new footprint yields usable photometry of the target.** TESScut successfully returned both requested cutouts, but the catalog position projects into leading collateral columns outside the active science image in each sector. Both prespecified target apertures contain **zero science pixels**. These are **not transit non-detections** and do not weaken or strengthen the planet interpretation. Candidate assessment remains unchanged.

| Sector | Camera / CCD | Projected physical column | Physical row | Science pixels in r=1.5 / 2.5 apertures | Final disposition |
|---|---|---:|---:|---:|---|
| 64 | 2 / 1 | **40.68135** | 922.77465 | **0 / 0** | Invalid target photometry: leading collateral columns |
| 99 | 3 / 2 | **20.75945** | 1651.51644 | **0 / 0** | Invalid target photometry: leading collateral columns |

The [official TESS data-product document](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014-Rev-F.pdf), Figure 5 on printed page 41 (PDF page 44), defines the science region as rows 1–2048 and columns **45–2092**, preceded by 44 serial-register collateral columns. The cutout physical WCS origins are RAWX=33 and 13 respectively. Adding the catalog position within each cutout gives the values above. The largest aperture reaches only physical column43 in sector64 and23 in sector99. A one-pixel indexing ambiguity cannot change the rejection.

The [images](diagnostic.png) show vertical column structure, not a stellar image at the marked catalog position. Their physical-coordinate rejection is independently verified by an explicit tangent-plane coordinate calculation rather than merely trusting the initial WCS library call. The geometry is consistent with the lack of QLP/SPOC target products in these sectors; it does not establish the archive's exact omission decision.

## Preflight and observations opened

The [metadata query](metadata.json) returned 18 exact-target records across available collections and no light-curve products for sectors64/99. The [history audit](history-audit.json) searched 103 result JSON files mentioning this target and raw-cache paths, including coordinate-named cutouts. Its only sector64 hit was the unrelated TIC469309982 row in a mixed-target report. Previously opened target epochs were10/36/37/63/90/100; no prior64/99 target observations were located. Completed queue audits and live-process state were checked; no running search queue depended on these observations remaining unopened.

The immutable [plan](plan.json) was saved before either data request. It retained the original P=4.192168718052227 d, BTJD1575.375831123655, duration0.092736 d and full original timing-profile pairs, without refitting later observations. It predeclared sector-specific 15×15 cutouts, target-centered radii1.5/2.5 pixels, annulus4–6 pixels, quality-zero samples, local event slopes/intercepts, error treatment and recurrence gates. It explicitly required off-detector rejection. These downloaded files are now inspected evidence and must not be treated as fresh holdouts.

Sources: [sector64 response](source-s64.json), [sector99 response](source-s99.json). Both include request parameters, URL, timestamps, byte count, ZIP hash and member FITS hashes. [TESScut documentation](https://mast.stsci.edu/tesscut/docs/getting_started.html) describes the cutout endpoint and sector-specific requests. A footprint/cutout response is not proof that a requested sky position lies on active science pixels.

## Preserved failed interpretation

The first analyzer correctly checked the cutout boundary but did not yet apply the detector's science-versus-collateral column boundary. It attempted the frozen numerical aperture procedure on the returned arrays. This produced almost-zero background-subtracted signal in sector64 and extremely noisy normalized engineering-pixel values in sector99. Image inspection triggered the physical-coordinate audit before any astrophysical conclusion was accepted.

[results.json](results.json), curve arrays, fitted arrays and the initial plot are retained to make this failure explicit. Sector64 had no usable event; sector99's mechanically fitted negative depths are **invalid as target measurements**, not evidence of brightening or absent transits. [geometry.json](geometry.json) **supersedes all photometric interpretation of those calculations** and implements the frozen off-detector gate. No aperture shifting, period adjustment or further flux download was used to rescue the result. The next analysis of any TESScut target should apply the physical science-boundary check before extracting a stellar light curve.

## Verification and limits

[verify.py](verify.py) checks both request times follow the frozen plan; hashes of raw ZIP/FITS files and official geometry documentation; complete metadata paging; exact sector/time-system headers; all six FITS HDU checksums; and independent manual sky-to-pixel plus physical-column arithmetic. It independently checks the preserved invalid fits' linear algebra without treating them as stellar evidence. [verification.json](verification.json) passes. Both the data plot and official detector-geometry figure were visually inspected.

```sh
OPENBLAS_NUM_THREADS=1 uv run python results/new-epochs-80387959-20261012/verify.py
```

[Implementation notes](implementation-notes.md) retain an initial NumPy-boolean serialization failure and its non-scientific fix. The browser PDF route timed out, while a direct request succeeded and its original bytes/hash were retained in [geometry-source.json](geometry-source.json). The failed browser route was not interpreted as unavailable documentation. No shared scientific module, candidate clock, source attribution, or disposition changed.
