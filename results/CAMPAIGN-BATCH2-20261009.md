# Expanded search and contamination audit, 2026-10-09

**No likely new planet candidate established. The research goal remains active.**

## Search scope and technical outcomes

Ranks 301–1000 of the fixed 11,851-star eligible list were attempted: 698 of 700
successfully screened. Two SPOC inputs have no usable quality-zero positive
flux/error pairs; their original errors are retained. Combined with the first
batch, 997 of 1,000 selected stars have been screened. This is separate from the
96-star random pilot and is not a complete survey of any sector.

The second batch used 54 distinct training sectors in 1–55. Periods were 0.5–20
days; the strongest three separated peaks were screened. New diagnostics measure
transit-duration binned noise, event-depth consistency, event dominance and
proximity to cleaned segment edges. These remain heuristic cuts, not calibrated
planet probabilities or survey false-alarm rates. Source snapshots and original
results are preserved in `campaign-small-stars-batch2-20261009/`.

Known-planet controls recovered L98-59 c (3.69068 days) and GJ 357 b (3.93330 days).
The first control exposed a short-duration noise-bin limitation: requiring three
30-minute samples per bin could leave 0.04-day transits unmeasurable. Allowing two
samples fixed that case. `rescreen-batch2-20261009/` recomputes diagnostics without
rerunning discovery or overwriting its evidence. Both control planets pass the
corrected screen. This small control set does not calibrate completeness.

MAST returned 7,515 QLP observations for these 700 stars. 315 stars have coverage
beyond Sector 85. A saved selection of 53 quiet legacy targets with adjacent newer
sectors and an unused middle-era validation sector was attempted. An initial
reader failure used obsolete KSPSAP column names; the corrected reader supports
DET_FLUX and the original products. Newer products can also span about 54 days
per sector, exceeding the old 100-day two-sector search limit. A separate retry
allowed a 120-day baseline, retaining the same data and search resolution.

Final newer-sector outcome: **37 of 53 stars successfully screened, zero signals
passing every non-crowding cut**. Sixteen have unavailable/nonfinite uncertainties
in an input sector; these are technical failures, not null detections. No errors
were replaced by assumed errors. Attempted training sectors include 87, 88, 89,
90, 94–98, and 100–104. The failed and successful attempts are all retained in
`campaign-newer-qlp*-20261009/`. Their stars overlap the legacy batch and must not
be added to the unique-star total. QLP's missing aperture crowding values would
require pixel vetting even for otherwise clean detections.

The official [QLP update page](https://tess.mit.edu/qlp-update/) documents pipeline
and column changes and an existing multi-sector search. Newer or low-cadence data
are opportunities, not evidence that no one has searched them.

## Signals investigated

| TIC | Discovery period | Evidence and disposition |
| --- | ---: | --- |
| 101534291 | 3.48846 d | Strong dips in SPOC and QLP, recovered at a frozen refined ephemeris in Sector 62; difference images in 35/36 place them about 2.5 pixels away from the target. Off-target contamination. |
| 125918626 | 4.42647 d | Dips in both extractions, inconsistent discovery event depths. Difference images in 43/44 place them about 3.65 pixels away. Off-target contamination. |
| 22952891 | 0.88178 d | Automatic pass and QLP support. Difference images in 43/44 localize the source about 2.1 pixels away. Off-target contamination. |
| 405415381 | 9.52896 d | Automatic pass, but the dip is broad; inferred depth changes from 736 to 1,832 ppm with the detrending window. QLP Sectors 42/43/44 give highly discordant fixed-phase depths (229, −66, 7,111 ppm). Sector 44 difference image has a positive/negative dipole near the bright star, not clean isolated dimming. Not promoted; variability/systematics unresolved. |

For 101534291, adding older Sector 9 to training refined the period to 3.4881328
days **before** opening Sector 62. The later fixed-phase signal has formal S/N
24 and six supported events, with conditional timing uncertainty below half the
fitted duration. Despite this successful prediction, the signal is not on the
target. The Sector 36 difference moment lies about 1.5 arcseconds from TIC
101534303 / Gaia DR3 5463554509137583872, already classified ECL by Gaia.
Gaia's listed period (~10.608 days) does **not** match the TESS period; the Gaia
fit has poor reduced chi-square. Do not claim matching ephemerides or a newly
discovered binary. The repeated positional offset is the principal rejection.

For 125918626, two nearby sources lie within a few arcseconds of the difference
moment: TIC 125918599 (Tmag 13.39) and TIC 660622134 (Tmag 16.68). The images
establish that the signal is off the bright target but do not uniquely separate
those neighbors. For 22952891, the Sector 44 difference moment is about 2.45
arcseconds from TIC 22952896 (Tmag 16.53). Catalog non-matches for such neighbors
would not establish their nature or novelty.

Difference images use symmetric local out-of-event baselines, propagated formal
pixel errors, weighted event averages and positive-flux moments. Figures,
per-event moments, FITS integrity results, source URLs and SHA-256 hashes are in
`pixels-*-20261009/`. These are diagnostic localizations, not calibrated PRF fits
or astrometric error ellipses. Neighbor positions are not proper-motion corrected.
The repeated multi-pixel offsets and separate positive sources are convincing
contamination evidence; the dipole on 405415381 is explicitly not treated as
such a localization.

## Validation data already inspected

Newly opened later SPOC sectors: 101534291: 62; 125918626: 70/71; 22952891: 70/71.
For the latter two, propagated timing uncertainty is too large for their fixed
measurements to count as decisive successes or failures. The retrospective
independent Sector 70/71 searches on 125918626 are labeled exploratory; they are
not blind ephemeris predictions. No later sectors were opened for 405415381.

All discovery and QLP comparison sectors used in these runs are now training or
inspected data. Consult the exact manifests before reserving future validation.
A successful held-out prediction alone cannot distinguish a blended eclipsing
binary from an on-target planetary transit.

## Reproducibility and next work

Nineteen tests pass, including long-baseline synthetic recovery, gap-preserving
binning, expanded-training timing refinement and localization of an injected
background eclipse. Raw files remain in ignored `data/`, with provenance in the
committed evidence. This audit preserves unsuccessful searches and reader
failures as well as corrected results.

Continue beyond rank 1,000; improve variability and image-systematic diagnostics;
expand injection/recovery in real data and correlated-noise null calibration.
Any genuinely surviving lead still needs physical transit modeling, current
catalog/literature checks and convincing on-target evidence. Neither the search
thresholds nor the current null results establish survey completeness. No
external reports or messages have been sent.
