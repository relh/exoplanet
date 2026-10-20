# First TESS search — 2026-10-09

**No new exoplanet candidate is established by this pilot.** All 96 selected
stars were successfully screened, and all have at least one final screening flag.
This is a small exploratory experiment, not a complete survey or a claim that
these stars have no planets.

## Data and sample

- NASA/MAST TESS-SPOC Sector 14 full-frame light curves (2019, approximately
  30-minute cadence), PDCSAP flux, strict `QUALITY == 0` filtering.
- 156,208 light-curve URLs in the sector manifest; 666 TIC IDs excluded by the
  saved TOI and confirmed-planet catalogs.
- Uniform random sample of 96 remaining TIC IDs; seed 20261009. No nearby-star,
  small-star or Earth-size selection was applied.
- Separate ExoFOP community-candidate snapshot: 5,138 rows, no exact TIC matches
  among these 96. This is a limited catalog check and does not establish novelty.
- Download hashes, retrieval timestamps, full catalog snapshots and all target
  results are retained. Raw FITS files remain in local ignored `data/` and are
  reproducible from the saved source URLs and hashes.

## Results

The initial screen (`pilot-s14-20261009`) left one unflagged object,
**TIC 272747181**, at a fitted period of **1.14093 days**, depth **1,325 ppm**,
and formal BLS S/N **10.18**. Eight local events had formal S/N >=2.

Inspection of its folded light curve showed repeated oscillations rather than
an isolated transit profile. A sinusoidal search found a **0.285279-day** period,
close to one quarter of the BLS period. Its likelihood improvement was **1.44×**
the box model's improvement. This favors a variability interpretation under the
pilot's heuristic comparison; it does not determine the physical cause. The
inverted curve also had a strong peak (formal S/N 8.28). Even assuming a genuine
on-target transit, the header stellar radius would imply roughly **9.2 Earth
radii**, not an Earth-sized planet.

The revised screen (`pilot-s14-v2-20261009`) adds that sinusoidal check and verifies
FITS checksums directly. It searched the **same 96 stars**, with **zero errors**
and **zero unflagged objects**. The thresholds are exploratory and the revision
was motivated by inspecting this sample; this is not a preregistered experiment.

Other high-ranking peaks had warnings for secondary eclipses, odd/even depth
mismatches, crowding, comparable inverted signals, large duty cycle or unstable
detrending. A screening flag does not definitively classify a source or exclude
all possible planets. Detailed measurements are in each run's `results.json`.

## Integrity and validation

All 96 files passed direct verification of every HDU CHECKSUM. Initial Astropy
warnings were traced to its handling of absent DATASUM keywords, not failed
whole-HDU sums. We use the [registered FITS checksum convention](https://fits.gsfc.nasa.gov/registry/checksum.html)
to check the original bytes. Tests cover valid files without DATASUM and a
corrupted file, as well as injected-transit recovery, a noise control, sinusoidal
variability and gap handling. Six tests pass.

This pilot has no pixel-level contamination test, independent-extraction
comparison, held-out-sector validation or calibrated survey false-alarm rate.
No external submission was made. The two example objects from the motivating
post were not reanalyzed, and its discovery and future-observation claims were
not verified.

## Reproduce and extend

```sh
uv sync --locked
uv run pytest -q
uv run exoplanet-search --sector 14 --limit 96 --seed 20261009 \
  --output results/reproduction
```

The catalog cache in local `data/` reproduces the original catalog selection.
On another machine, restore `catalog_toi.csv` and `catalog_confirmed.csv` from the
run into `data/catalogs/toi.csv` and `data/catalogs/confirmed.csv`, with matching
JSON sidecars from `run.json`'s `catalogs` entries. Otherwise catalogs are fetched
again and may select a different sample. This is why snapshot dates matter.

A useful next campaign would select small, relatively quiet stars with multiple
available sectors, calibrate sensitivity using injected shallow transits, and
hold out entire sectors for prediction tests. The present pilot is the baseline
for that work; it is not running an unattended background search.

Data references: [MAST TESS-SPOC](https://archive.stsci.edu/hlsp/tess-spoc),
[NASA Exoplanet Archive TAP](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html),
[ExoFOP community-candidate export](https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv).
