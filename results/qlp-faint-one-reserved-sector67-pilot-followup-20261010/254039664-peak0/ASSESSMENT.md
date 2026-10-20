# TIC 254039664: likely neighboring eclipsing-source contamination

Frozen native QLP P=3.532664464928 d, duration 0.092736 d,
epoch BTJD 3128.701899016. Local depth 10761 ± 609 ppm, five supported events.
Only crowding/missing-crowding remains as a screening flag. The discovery plot
was inspected: deep noisy localized trough with positive shoulders and a large gap.

Reserved Sector 13 gives 4818 ± 639 ppm, but the timing spread is 0.706346 d.
The unchanged conclusion is timing-inconclusive: positive formal depth does not
establish independently predicted recurrence. Same-sector binned QLP gives
10641 ± 617 ppm while SPOC gives −812 ± 597 ppm. This discrepancy needs
source vetting; the products use the same photons, not independent observations.

TIC cone query returned 539 entries. Both raw and processed pixel difference
images show a compact off-target feature near TIC 254033964 (T=11.768).
Processed pixels have six usable event windows, a moment 3.906 pixels from the
target and 0.108 pixels from that neighbor. Raw pixels have seven event windows,
offset 4.079 pixels from target and 0.234 pixels from the bright neighbor.
These window counts differ from the five supported light-curve events.
Faint TIC 1821026498 (T=19.557) lies 0.035 pixels from the raw moment and
0.185 pixels from the processed moment: the exact physical variable is not
uniquely identified by these moments.

Processed/raw/background plots were visually inspected. Raw spatial-background
masks leave only one or zero usable background pixels, so both fits are unavailable.
Formal pixel SNRs ~481 and ~371 are not calibrated localization confidence.
The two processing products use the same photons, not independent observations.
The bright-image moment is not the catalog target position.

TIC 254033964's native aperture at the fixed ephemeris has Sector 67 primary
114397 ± 241 ppm (~11.4%) and half-phase depth 5959 ± 269 ppm (~0.60%).
Sector 13 gives primary 37793 ± 253 and half-phase 2660 ± 288 ppm, but the
original timing uncertainty remains: these depths are not a validated prediction
of recurrence, and no period was refit on reserved data.
Same-image apertures can share contamination.

Gaia lookup of target 254039664, bright 254033964 and faint 1821026498
returned three mapped sources and no classifier/eclipsing-binary entries.
Nonmatches do not exclude an eclipsing system or establish novelty.

Conclusion: likely neighboring eclipsing-source contamination, not a target
planet. The exact variable within the close neighbor group and fundamental
orbital period remain unconfirmed.

Evidence: [reduction](../../qlp-faint-254039664-reduction-20261010/results.json),
[processed pixels](../../spoc-pixels-254039664-s67-20261010/analysis/localization.json),
[raw pixels](../../tesscut-254039664-s67-20261010/analysis.json),
[background limitation](../../tesscut-254039664-s67-20261010/background.json),
[neighbor aperture](../../neighbor-254033964-20261010/results.json),
[Gaia](../../gaia-254039664-neighbors-20261010/results.json).
