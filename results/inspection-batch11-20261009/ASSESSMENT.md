# Initial inspection of new priorities

TIC 80387959 is a promising unresolved signal, not an established new planet.
P=4.19218 days, depth 815 ppm, nine supported discovery events, stable alternate
flattening, no obvious secondary in the full fold. QLP Sectors 36/37 show 729/996
ppm (formal S/N 5.01/7.72). Difference images in both sectors are centered on the
target (moments 0.17/0.085 pixels away), with modest peak S/N 4.85/5.53. This does
not exclude unresolved contamination.

Older Sector 10 was added to training before freezing and opening Sector 63.
The frozen 4.192251-day ephemeris gives five supported events in 63, depth
740 ppm and formal S/N 7.06 (expected 9.01). The timing spread is 0.052585 day,
slightly above the preset half-duration threshold; the original conclusion is
`timing_prediction_inconclusive`, preserved unchanged. Fixed-time support is
encouraging but does not satisfy the complete preset recovery criterion. Pixel
63, null controls and neighborhood checks are underway. Exact-TIC and coordinate
web searches returned no results, which does not establish novelty.

TIC 384603440 has modest QLP support: S/N 3.95/3.19, depths 708/454 ppm in 13/12.
Still requires image and event vetting; no reserved sector opened.
TIC 274454689 has weak QLP support (S/N 0.14/1.35/0.99 in 26/25/24), far shallower
than its SPOC dip; not promoted. No reserved sector opened.


Further 80387959 diagnostics: 0/48 block-control searches exceed original power;
not a calibrated false-alarm probability. Sector 63 difference moment is ~0.57
pixels from the target. Using the expanded frozen ephemeris and fixed aperture,
on-target injection offsets exceed observed in 38/47, 6/47 and 1/47 controls in
36/37/63. The later-sector offset warrants caution despite central discovery
images. Near neighbors include TIC 80387965 (T=13.62, 13.76 arcsec) and 80387961
(T=16.70, 7.54 arcsec); neighbor-template controls are being evaluated. Catalog
and alias web searches have not established novelty or a host assignment.


Neighbor-control runs are terminal. TIC 80387961 gives observed offsets from
control medians 0.290/0.128/0.783 pixels in 36/37/63 (11/47, 18/47, 0/47 controls
larger); TIC 80387965 gives 0.366/0.543/0.442 pixels (3/47, 0/47, 5/47 larger).
Neither neighbor hypothesis fits all three sectors consistently. Target remains
compatible with discovery-sector diagnostics but later localization unresolved.
Counts are conditional, dependent diagnostics, not source probabilities.


384603440 Sector 13 image has a strong positive/negative dipole, with positive
moment 1.29 pixels from target and adjacent negative flux. This is a motion or
extraction warning, not calibrated off-target attribution. Do not promote without
resolving it. Exposure-model companion retains 80387959 and 384603440 only.


## Later-sector recovery and current limitations

Sector 63 was explicitly reassigned to training alongside 10/36/37. A new
4.192168718-day ephemeris was written before downloading QLP 90/100. Both pass
the preset recovery rule: 621 ppm, S/N 6.33, four supported events in 90; 651 ppm,
S/N 5.73, two events in 100. Timing spreads 0.02477/0.02679 day are below half the
frozen 0.092736-day duration. Both use published uncertainties. Original Sector63
inconclusive outcome remains preserved. These later detections strongly support
a repeatable astrophysical signal, not its host identity or planet classification.

TESScut images for 90/100 are separately preserved, including raw and per-cadence
outer-pixel background-subtracted diagnostics. Sector90 has an extended changing
background; the subtracted image is more suitable for localization. Target-control
offsets 0.127/0.507 pixels have 37/45 and 6/45 controls larger in 90/100. Neighbor
80387965 offsets 0.356/0.369 have 12/45 and 9/45 larger; 80387961 gives 16/45 and
3/45. These dependent, approximate-template counts are not source probabilities.
No single contaminant fits every sector consistently; unresolved contamination
remains possible. Background-estimation covariance is not propagated in displayed
formal pixel S/N. Proper motion is small but not yet applied to these comparisons.

Six circular limb-darkened fits to already-opened SPOC 10/36/37/63 give conditional
2.52–2.59 Earth radii (including three stellar-prior trials and three free-axis
trials). This is sensitivity to fixed model choices, not a credible interval.
Dilution, eccentricity and host ambiguity remain unmodeled. The new QLP sectors
were not used to tune these physical fits.

Gaia DR3 returns no variability-classifier or eclipsing-binary rows for the target
and three close neighbors. Absence is not exclusion. SIMBAD identifies the target
as TYC 8203-2056-1 (PM*). NASA positional TOI/confirmed cone queries initially
returned HTTP403; separate rectangular queries succeeded with zero rows. All
failures/results retained; these catalog nonmatches do not establish novelty.


## TGLC and expanded catalog checks

TGLC raw/calibrated PSF/aperture extractions for target and neighbor 80387965 in
already-opened 10/36/37 are now checked. Both stars show the dip in 36/37, but their
out-of-event PSF light curves are strongly correlated (r=0.72–0.87 across sectors).
The relative eclipse-depth ratio resembles the shared-structure amplitude ratio.
This is not a clean independent neighbor eclipse or proof of on-target origin.
See ../tglc-80387959-20261009/ASSESSMENT.md and retained measurements.

Exact matching of all 706 TIC entries in the 0.06-degree neighborhood against the
same-day TOI/confirmed/CTOI/TESS-EB catalogs gives zero matches. A positional CTOI
check also gives no match within 216 arcsec. Catalog coverage is finite, especially
TESS-EB Sectors 1–26; nonmatches still do not establish novelty. Source hashes in
../catalog-neighborhood-80387959-20261009/crossmatch.json.
