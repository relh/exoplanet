# TIC378761120: repeatable dimming localized away from the target

**Rejected as a planet signal around TIC378761120.** The1.32724d dips repeat,
but two difference-image epochs place the variability~2.3–2.4 TESS pixels away
from the target. Larger QLP apertures deepen the signal, supporting contamination
by another star. Independent ZTF photometry identifies a deep eclipsing source
at **TIC378761130**, about50.6arcsec away, at the frozen TESS ephemeris.

## Retained positive evidence

The initial QLP Sectors17/18 search found~1.32727d,~1,000ppm. Nominal-phase dips
also appear in52/58, but the original prediction tests are timing-inconclusive.
Using only these four already-opened sectors, a second ephemeris was frozen:
P1.3272415468d, epoch1767.7082881 BTJD, duration0.1112832d, depth925±58ppm.
Previously unopened Sectors78/85 then pass the preset recovery checks:

| Sector | Depth,ppm | Formal SNR | Supported events | Timing spread,d |
|---|---:|---:|---:|---:|
|78|1058±186|5.70|3|0.03775|
|85|993±124|8.04|7|0.04077|

Both use published uncertainties; their off-phase control maxima are1.94/1.02.
The timing intervals and SNRs are conditional diagnostics, not planet probabilities.
Sector86 remains unopened. No original inconclusive check was overwritten.

## Evidence against the target hosting the dip

- SPOC reductions of the same17/18/52 epochs give much shallower519±251,
 271±142 and218±120ppm, respectively.
- Across all six opened QLP sectors, small-aperture depths are239–462ppm;
 main-aperture depths789–1085ppm; large-aperture depths900–1756ppm.
- Sector17 difference images stack16 events, with peak formal SNR9.11 and a
 moment offset2.43pixels from the catalog target. Sector52 stacks15 events,
 peak SNR29.66, offset2.32pixels. Neither peak is stamp-edge limited. The offset
 is much larger than the target's proper-motion displacement.
- The variable image lies in a group of faint neighbors around~50arcsec from the
 target, including TIC378761130/378761126 and fainter sources. Moment centroids
 do not uniquely assign it to one of these stars; PRF probabilities are not claimed.
 Ground photometry subsequently identifies the eclipsing neighbor as described below.

The TIC radius would have implied~1.52 Earth radii **only if the target hosted the
signal**. That interpretation is contradicted by localization and should not be
used as a planet-radius estimate. Gaia DR3 supports the target's~62pc distance,
but that does not identify the contaminating source.

No exact match was found among the433 TIC-cone neighbors in the dated TOI,
confirmed-planet,CTOI,Villanova,Kostov2025 or DTARPS tables checked. This negative
catalog result does not establish novelty or planetary nature. All discovery,
frozen predictions, aperture checks and pixel evidence remain available.

## Independent ground-based resolution

A15arcsec ZTF cone around the Sector52 off-target difference centroid was queried
only after freezing the TESS ephemeris. No ZTF period or phase optimization was
performed. Four independently catalogued field/filter light curves coincide with
TIC378761130 within0.05arcsec and show the same eclipse:

- Main r-band object:0.2420±0.0037mag,55 in-window measurements across54 events.
- Main g-band object:0.2470±0.0089mag,50 in-window measurements across50 events.
- Secondary field coverage:r0.2499±0.0140mag;g0.2468±0.0314mag, fewer observations.

The formal uncertainties are not survey-calibrated probabilities. Nevertheless,
the deep phase-aligned eclipses, two off-target TESS images and aperture-depth
trend jointly give strong contamination evidence. The neighbor is~4.90 TESS
magnitudes fainter; a~20% intrinsic flux loss would produce~2,170ppm if its full
flux entered the target aperture. Partial throughput readily explains the
~1,000ppm QLP signal. This is an approximate cross-band dilution check, not a PRF
model or a definitive physical classification of the eclipsing system.

[Ground-photometry analysis and plot](../ztf-378761120-contaminants-20261010/analysis.json)
retain all objects, weak/empty cases, quality cuts, time conversion and source
hashes. [Folded plot](../ztf-378761120-contaminants-20261010/fixed-phase.png).
