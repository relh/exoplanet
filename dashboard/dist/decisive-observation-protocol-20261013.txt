# Proposed source-attribution observation

**Draft for feasibility assessment; no observations requested or booked.**
This protocol is aimed at identifying the source of the 4.19217-day dip in the
TIC 80387959 field. A successful localization is an intermediate result, not
planetary validation. TIC 402358350 first needs ephemeris recovery; its broader
windows are retained in the separate timing packet.

## Scientific question

Does the named target dim, or can a resolved neighboring source account for
the TESS aperture decrement? Observe the target and viable neighbors together,
so atmospheric and timing conditions do not differ between host hypotheses.
The principal nearby alternative is TIC 80387965 at 13.76 arcseconds. Include
TIC 80387961, TIC 937808821 and TIC 80387968 where measurable. The latter's
sparse SkyMapper observations weaken only a particular flat-bottom eclipse
explanation; it remains in the field list.

The target signal is roughly 600–800 ppm in the inspected reductions. A
contaminating eclipse can be much deeper on a faint neighbor. The previous
flux-budget assessment supplies model-dependent requirements and stress tests;
they are not observed eclipse depths or universal lower bounds. No passband
conversion should be assumed without an explicit stellar/eclipsing-source model.

## Before scheduling

1. Confirm usable observing access and instrument availability. Select dates
   only from an actual site-specific visibility calculation using the complete
   timing envelope, duration and baseline, not the nominal midpoint alone.
2. Obtain instrument specifications and test images or a demonstrated comparable
   performance record. Check that the primary remains unsaturated while the
   relevant faint neighbors have useful precision. Detector pixel scale alone
   does not establish resolving ability or photometric accuracy.
3. Confirm source identities on astrometrically calibrated images. Use proper
   motions where available and account for seeing-dependent contamination.
   Preserve comparison-star choices independently of any apparent transit.
4. Freeze dates, original clocks, timing envelopes, passband, exposure cadence,
   calibration, aperture/PSF choices, quality exclusions and decision rules
   before accessing the new event photometry. Retain a no-selection outcome
   if the prerequisites fail. Define any alternatives in advance.

## Observation design

Cover the complete retained event envelope and at least the stated one-hour
baseline on both sides; the current provisional total is about 5.6 hours.
Allow additional operational margin for acquisition and interruptions. Seek
at least two separate fully covered events. This repetition target is a
planning requirement, not a universal validation rule.

A 60–120-second cadence and target event-depth uncertainty near 100 ppm are
initial performance objectives from the existing packet, not demonstrated
capabilities. A neighbor-focused experiment can be useful even if that primary
precision is unattainable, provided its measured sensitivity can test the
specified contaminant hypothesis. Do not claim that a flat primary or neighbor
has been excluded without sufficient timing coverage and sensitivity.

Retain raw images, bias/dark/flat products, masks, pointing, sky background,
seeing, airmass, exposure start/end times and the time standard. Preserve
unfiltered and quality-selected series for all sources. Convert exposure
midpoints to BJD_TDB consistently, with the actual observatory location.

## Analysis and decisions

Use out-of-event baselines and stable comparison sources. Quantify correlated
noise and aperture/PSF cross-talk. Test recovery of signals injected independently
of the fitted source-response assumptions; synthetic agreement with a single
assumed PSF is not proof of accurate real-source localization. Record practical
injection sensitivity, false localization and missed-signal behavior.

| Observed outcome | Defensible conclusion | Additional requirement |
|---|---|---|
| Repeated resolved neighbor dimming at the TESS phase | Evidence for that source as a contaminant | Show its captured flux, depth and timing quantitatively explain the TESS dip; establish eclipse/variability origin before declaring a nonplanetary signal |
| Repeated dip on the primary, with adequate neighboring-source constraints | Stronger target-host attribution | Constrain unresolved stellar companions and other false positives with appropriate imaging, spectra/RVs and validated modeling |
| No dip, inadequate timing coverage or precision | Inconclusive | Improve timing or sensitivity; retain the negative observation |
| Repeated non-detection with predeclared adequate coverage and empirical recovery | Evidence against the tested periodic signal model | Audit clock alternatives, passband and signal evolution before broader rejection |
| A likely instrumental correlation or unstable source fit | Candidate observation remains unreliable | Demonstrate a reproducible artifact explanation, rather than selecting a favorable reduction |

The new active goal is complete only with a defensible physical classification
for each investigated signal. Source localization, a proposal, a telescope
reservation or a conditional model percentage is not that classification.

## Evidence and access boundaries

Inputs: [current timing packet](../followup-planning-20261013/ASSESSMENT.md),
[neighbor budget](../paper-host-vetting-20261012/ASSESSMENT.md),
[new resolved checks](../followup-overview-20261013/ASSESSMENT.md), and
[failed localization controls](../strongest-host-identifiability-20261012/ASSESSMENT.md).
This draft opens no new flux and makes no inference about actual telescope
performance. Contacting observers, submitting proposals or candidates, booking
an instrument and spending require explicit user authorization. Public archive
access and preparation remain within the authorized scope.

## Feasibility findings relevant to this draft

The [site and mount screen](../site-visibility-20261013/ASSESSMENT.md) supplies
no full LCO one-meter track with the conservative mount margin. Its one nominal
pass on 20 March 2027 is close to the tracking boundary. Confirm another suitable
configuration or explicitly revise the experiment before choosing dates.

The [two archival baseline frames](../lco-archive-metadata-20261013/ASSESSMENT.md)
saturate the target and principal neighbor at 240 seconds in Sinistro's wide
filter. These settings fail ordinary core-photometry feasibility; shorter
exposures and their noise/neighbor sensitivity remain untested. Neither frame
covers the predicted dip. No source was excluded.
