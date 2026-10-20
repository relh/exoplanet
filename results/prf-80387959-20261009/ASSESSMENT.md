# Mission PRF source attribution: TIC 80387959

The repeatable 4.19217-day signal remains unresolved. Mission PRF fits favor
inconsistent hosts across sectors; empirical pixel controls do not justify
promoting it to a likely new planet.

This analysis uses the archived start_s0004 mission PRF grids with TESS_PRF 0.1.3.
`models.json` records download URLs, hashes, detector coordinates and raw pixel
hashes. Gaia DR3 positions for four hypotheses were propagated linearly to each
sector's mean epoch (parallax omitted). Reference scenes use catalog stars with
T<17 within the stamp plus a one-pixel margin, nonnegative free stellar fluxes and
a background plane. A shared positional shift is fitted using out-of-event median
images. The difference image is then fitted separately with each host's PRF and
a background plane, using formal diagonal pixel errors. Reference registration
uncertainty and PRF mismatch are not propagated.

| Sector | Lowest conditional chi-square host | Target chi-square | Winning chi-square | Correct target injections / 41 real-pixel controls |
|---|---|---:|---:|---:|
| 36 | 80387959 | 96.60 | 96.60 | 21 |
| 37 | 80387959 | 109.09 | 109.09 | 29 |
| 63 | 80387965 | 524.30 | 431.44 | 24 |
| 90 | 80387961 | 255.96 | 236.54 | 23 |
| 100 | 80387959 | 261.54 | 261.54 | 28 |

Each fixed-host fit has 117 nominal degrees of freedom. Later-sector residuals
show that the assumed noise/model does not fully describe those images. These
chi-square differences are diagnostics, not probabilities or calibrated host
exclusions. A free-position fit can absorb some residual structure and is likewise
not a secure astrometric solution.

Controls inject matched mission PRFs into 41 shifted-phase difference images per
sector after masking real transits from both control events and baselines. They
preserve real pixel covariances, but windows overlap and may not be exchangeable
with the actual transit windows. Injections also omit PRF mismatch. These recovery
counts demonstrate ambiguity; they do not supply a formal false-positive rate.
The independent Gaussian-noise controls in `fits.json` make stronger assumptions.

A T<15 reference-scene sensitivity run in `scene-mag15/` retains all five winning
hosts, with registration shifts differing by less than 0.02 pixel. Main scene
residual RMS is 0.13–0.28% of the brightest pixel, not an astrometric error bound.
Faint sources, outside-stamp wings, duplicate-catalog handling and approximate
proper-motion propagation remain model limitations.

Validation: 33 project tests pass, including blended-scene registration and injected
target/neighbor eclipses against a sloping background. Fifteen additional archived
mission-PRF injections recover positions within 0.0001 pixel and preserve total
flux on a sufficiently large stamp, including either side of a pixel boundary.
This checks interpolation/fitting behavior, not astrophysical model accuracy.

Reproduce from the repository root:

```
uv run python results/prf-80387959-20261009/download_models.py
uv run python results/prf-80387959-20261009/analyze.py
uv run python results/prf-80387959-20261009/controls.py
uv run python results/prf-80387959-20261009/scene-mag15/analyze.py
uv run python results/prf-80387959-20261009/plot.py
uv run pytest
```

These scripts are the original run record; use a new output directory for a new
investigation to preserve current results. Raw downloads remain ignored locally.

Source: [MAST mission PRF archive](https://archive.stsci.edu/missions/tess/models/prf_fitsfiles/),
[NASA-listed analysis tools](https://heasarc.gsfc.nasa.gov/docs/tess/data-analysis-tools.html),
[TESS_PRF implementation](https://github.com/keatonb/TESS_PRF).
