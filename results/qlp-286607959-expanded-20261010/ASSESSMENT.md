# TIC 286607959: resolved eclipsing-neighbor contamination

Rejected as a planet around TIC286607959. Two pixel epochs and direct neighboring
QLP photometry explain the repeating target-aperture dip.

At the existing frozen P10.45923770d ephemeris, sector8 (two events) and sector34
(two events) show dominant flux loss about5pixels from the target. Both differences
are near the stamp edge, so their moments are not calibrated astrometry; no PRF
probability is claimed. Nonetheless, their sky positions both lie near bright
neighbor TIC286608026, about109.8arcsec from the target. Formal pixel SNRs exceed700,
which ignores correlated systematic errors and does not validate a planet.

The neighbor's own QLP extractions in sectors8/9/34 show fixed-phase eclipse depths
of20.64%,20.67%,21.01%. Phase plots also show a second deep eclipse roughly3.2days
before the primary (~15% at its bottom). This is strong eclipsing-binary evidence
and identifies contamination of the shallow target-aperture signal. Measurements
used the pre-existing target ephemeris without period or phase optimization.
Separate extractions share TESS images; they are not independent observations.

Neighbor Tmag11.2551 is only0.3582mag fainter than target Tmag10.8969, so a small
amount of aperture leakage can explain the~0.1% target signal. Exact throughput
was not fitted. No companion masses or binary orbital solution are claimed.

See ../qlp-286608026-contaminant-20261010/{plan.json,measurements.json,fixed-phase.png},
../pixels-286607959-s8-20261010 and ../pixels-286607959-s34-20261010.
Dated TOI/confirmed/CTOI/EB, Villanova/Kostov2025/DTARPS exact-TIC checks across685
neighbors found no match. Catalog nonmatches do not establish novelty or exclude
alternate identifiers. URL/SHA provenance is retained; target sector89 remains
unopened. The earlier mixed independent-sector evidence is preserved below.

## Earlier assessment, superseded by source localization

# TIC 286607959: mixed independent-sector evidence

Not promoted to a likely planet candidate. Four already-opened sectors (8,9,34,36)
refined the period to 10.45923770 days, duration 0.13412 days, depth 1309 ±107 ppm.
The updated prediction was frozen before downloading sectors61/62; sector89 remains
unopened. These are follow-up tests of an existing signal, not a fresh discovery.

Sector61 measures 347 ±182 ppm (formal SNR1.91) versus expected SNR7.21, with only
one supported event. It fails the preset recovery criterion despite expected
sensitivity. Sector62 measures 1146 ±204 ppm (SNR5.63), with two supported events,
and passes the preset criterion. Timing spreads are 0.0457/0.0462 days, below the
fitted duration. The two measured depths differ by about2.9 formal standard errors;
correlated noise and aperture effects remain unmodeled. Neither success nor failure
is erased by combining the sectors.

Source attribution, instrumental-systematic checks and comprehensive catalog vetting
remain incomplete. Preserve the sector61 negative evidence in any later assessment.
See followup/frozen.json and followup/heldout.json for data provenance, timing profiles,
events and dependent phase controls (not survey false-alarm probabilities).
