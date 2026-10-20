# TIC 432280723: likely neighboring eclipsing-source contamination

Frozen native QLP period 2.214113082130 d, duration 0.072 d,
epoch BTJD 3586.957713387. Local depth 3993 ± 467 ppm, eight supported events.
Only the crowding/missing-crowding screening flag remains. Discovery plot was
visually inspected: noisy localized trough against substantial point scatter,
with a long observing gap. Passing screening alone is not a planet claim.

Reserved Sector 57 measures 147 ± 526 ppm, but the propagated timing spread is
0.824721 d. The conclusion is timing-inconclusive, neither confirmation nor
exclusion. Same-sector 10-minute-binned QLP gives 3878 ± 481 ppm.
The SPOC light-curve request returned HTTP 404; unavailable data are not a null
measurement or independent corroboration. TIC cone query returned 78 entries.

The raw 11×11 cutout has a compact dip at its edge, 5.242 pixels from the
target. Because edge truncation biases moments, a 21×21 cutout was examined.
The wide difference feature remains compact and off target: moment offset
5.659 pixels from TIC 432280723, 0.231 from TIC 432277754, 0.424 from
bright TIC 369660279 and 0.572 from TIC 369660280. Twelve pixel event
windows are usable (distinct from eight supported light-curve events).
Both raw and both background plots were visually inspected. Wide spatial-plane
fits using 303 and 209 background pixels retain the compact off-target feature.
Formal pixel SNR ~426 is not calibrated attribution confidence, and these are
the same photons as QLP. SPOC processed pixels also returned HTTP 404.

Neighbor aperture checks at the unchanged ephemeris:
TIC 432277754 has a Sector 84 primary depth 363625 ± 1659 ppm (~36.4%)
and half-phase depth 120268 ± 1577 ppm (~12.0%).
Bright TIC 369660279 has primary 46403 ± 209 ppm (~4.64%) and half-phase
14909 ± 198 ppm (~1.49%). These nearby apertures are blended; their agreement
does not uniquely identify the physical variable. The large primary/secondary
eclipselike signals strongly favor a neighboring eclipsing system.

Sector 57 primary measurements are 12104 ± 1280 ppm for TIC 432277754
and 1556 ± 163 ppm for TIC 369660279, but the original propagated timing
uncertainty remains. These fixed-phase depths are not validated independent
recurrence. No ephemeris was refit using held-out data.

Gaia DR2-to-DR3 lookup for the target, 432277754 and 369660279 returned
three sources and no variability-classifier/eclipsing-binary entries.
TIC 369660280 was not included in that three-source query. Nonmatches do
not exclude variability or establish novelty.

Conclusion: likely neighboring eclipsing-source contamination, not a securely
attributed target planet. The exact variable within the unresolved neighbor
group and its physical/fundamental period remain unconfirmed.

Evidence: [reduction](../../qlp-faint-432280723-reduction-20261010/results.json),
[wide raw pixels](../../tesscut-432280723-s84-wide-20261010/analysis.json),
[wide background checks](../../tesscut-432280723-s84-wide-20261010/background.json),
[neighbor 432277754](../../neighbor-432277754-20261010/results.json),
[neighbor 369660279](../../neighbor-369660279-20261010/results.json),
[Gaia](../../gaia-432280723-neighbors-20261010/results.json).
