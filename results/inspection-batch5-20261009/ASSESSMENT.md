# Batch-five follow-up checkpoint

No likely new candidate established. Discovery snapshots here preserve completed
target evidence while the parent 1,000-target run continues.

## TIC 47961197

The 1.41722-day, 223-ppm SPOC feature is broad. QLP formal S/N is only 1.34 and
3.94 in Sectors 34 and 35, with depths 39 and 153 ppm. Sector 34 has a strong
off-target difference residual, about 2.20 pixels from the header target.
Sector 35 instead has a strong positive/negative dipole, with a different moment
about 1.23 pixels away. These are not consistent clean localization measurements
of a unique contaminant. The combined extraction and image evidence does not
support promotion. Sectors 61/62 remain unopened.

## TIC 83968926

Retained as an unresolved lead, **not a likely planet**. Four events in Sectors
17/18 yield P=13.52749 days, depth 885 ppm, formal S/N 16.32. An exposure-integrated
local-baseline fit gives P=13.52578 days, depth 971 ppm, beta-adjusted S/N 12.53;
all four events remain supported, without significant odd/even mismatch. This
is a diagnostic box fit, not a physical planet fit.

QLP Sector 18 supports both covered events (combined depth 845 ppm, S/N 9.59).
QLP Sector 17 has no usable event measurement; that is not a failed detection.
Both pixel sectors show central positive residuals and nearby positive/negative
structure. Their global moments are 1.26 and 1.13 pixels from the header target;
this is ambiguous and does not establish an off-target source. The neighborhood
snapshot includes TIC 83968917, Tmag 14.40, but no unique contaminant is established.
No block control exceeded observed power in 48 draws; that is not a planet
probability or protection against coherent systematics.

Sector 24 was added to training before freezing the first Sector 58 prediction.
It added no usable transit events. The frozen timing spread in Sector 58 is
0.776 days, too large for a decisive fixed-time test. Measured S/N is -0.54 versus
formal expected 11.74. An explicitly exploratory, post-opening scan of 161 epoch
shifts across +/-0.776 days gives maximum S/N 2.82 and only one supported event.
It therefore supplies no recovery; it is not an independently predicted detection
or a calibrated exclusion test. Sectors 78/85 remain unopened.

The exact-TIC web searches returned no results. Those searches and catalog
nonmatches do not establish novelty. Further consideration requires better
localization, timing/coverage and extraction checks before any planet claim.

A further Gaia DR3 query selected 29 TIC-matched Gaia sources within 90 arcsec
and Tmag <17. None matched `vari_eclipsing_binary`; `vari_classifier_result`
returned one RS-classified neighboring source (431843431013151232). This is a
limited catalog check, not exclusion of a faint/unresolved eclipsing system or
identification of the dip source. Query, selection, response and hashes are in
`gaia-83968926-neighborhood-20261009`.

QLP was subsequently checked for already-opened Sector 58, reusing the original
frozen ephemeris and its timing spread. The fixed-time S/N is -0.40. The same
explicitly exploratory 161-shift window gives maximum S/N 2.63 and only one
supported event. Neither extraction recovers the signal in this later sector;
this further weakens the lead. Timing remains imprecise, so this is not a clean
fixed-time rejection or a calibrated exclusion. The QLP check is archived in
`qlp-heldout-83968926-s58-20261009`; Sectors 78/85 remain unopened.
