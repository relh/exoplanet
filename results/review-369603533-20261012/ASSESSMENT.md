# TIC369603533: known rotational variability and broad minima

Deprioritize this8.7035-day peak as a new-planet lead. The exact target is the VSX rotational variable Gaia DR3 4935884138639534976. The selected minima are broad and asymmetric, extend well beyond the0.18d search box, and the global fitted depth doubles with alternate detrending. Known rotation alone does not exclude a superposed planet; the combined morphology and processing sensitivity weaken this particular interpretation.

Only original discovery sectors2/3 were used. Added29/30 and reserved69 were not opened; their caches remain absent.

Original BLS depth is795.73ppm at P8.70349994d, duration0.18d (maximum searched duration), formal SNR13.49. Alternate-window BLS prefers8.68465541d and1632.89ppm, a2.05-fold depth change. [discovery.png](discovery.png), visually inspected, shows an extended trough surrounding the selected box in both reductions, especially the2.5d reduction. This morphology differs from an isolated compact transit.

At the unchanged original clock, local-baseline total depths are563.25±65.94ppm and661.36±69.92ppm. The smaller change than the BLS depth is expected because the local baseline itself falls within the broad depression; these are different baseline estimators, not conflicting measurements. Four events are measurable and three have individual formal SNR≥2. The first-sector event at BTJD1375.65 is only150.26±140.32ppm. Sector totals are445.07±96.31ppm and667.47±90.47ppm with1.5d detrending;576.64±95.40ppm and748.57±102.79ppm with2.5d. No secondary is detected at half-phase (−33.90±65.22ppm), which does not overcome the other concerns.

[identity.json](identity.json) contains the exact TIC/Gaia join; [results.json](results.json) contains the matching VSX ROT record. The catalog provides no rotation period, so no exact8.7d catalog-period match is claimed. NASA TOI/confirmed-planet exact-TIC queries succeeded with no rows; nonmatches do not establish novelty.

[verification.json](verification.json) checks source/raw/catalog hashes and identity, reconstructs both discovery reductions, and independently reproduces eight event depth/error measurements. [sectors.json](sectors.json) independently checks four sector totals. Detrending is shared, global search significance is not independently calibrated, and no host/planet probability is measured. Reproduce with `uv run python results/review-369603533-20261012/verify.py` and the sibling `sectors.py`.

No source downloads or new observations are currently warranted ahead of stronger leads. This disposition applies to the searched signal, not every possible planet around the star.
