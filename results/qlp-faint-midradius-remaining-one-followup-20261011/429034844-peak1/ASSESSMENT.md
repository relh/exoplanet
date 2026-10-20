# TIC 429034844: unresolved screening signal

Native refinement: P=1.400465271 days, duration=0.032000 days, box depth=0.01594738 ± 0.00029915 (formal). Training sectors [70]; 14 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Deep regular dips with three similarly spaced minima in the selected period fold. A shorter alias and eclipsing interpretation need evaluation. Original alternate-detrending flag remains; source and novelty checks pending, no new planet claim.

Reserved-sector timing tests: sector 42: timing_prediction_inconclusive, timing spread 0.102381 days; sector 43: timing_prediction_inconclusive, timing spread 0.098894 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 46.03384997860008. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Posthoc alias check

A0.466822-day dip sequence (one-third the original period) appears across all three opened sectors, with older dips displaced from the original predicted windows. Sector70 alternating depths differ somewhat under the0.933644-day doubled clock. An eclipsing binary and source contamination need vetting. This neither validates the original ephemeris nor establishes a planet. [Six panels, measurements and controls](../../alias-429034844-20261011/ASSESSMENT.md).

## Initial source images

All16 raw and14 processed sector70 individual difference maps were inspected at the original frozen1.400465-day clock. They repeatedly show a compact target-region feature. Raw event−1 has a positive field offset and event17 a strong negative offset; both are fully flagged in the processed data. All14 usable processed maps have a positive compact residual near the target. The raw aggregate moment is0.129pixels from the catalog target; the processed aggregate is0.130pixels from the bright-source moment (a different reference). These moments and formal pixel SNRs are not calibrated host probabilities. Close unresolved blends remain possible.

Raw usable windows contain13–14 quality-zero inside exposures and28–56 outside exposures; processed usable windows contain12–13 inside and56 outside exposures. Raw events6/7 and processed−1/6/7/17 have no quality-zero inside samples. No gates were relaxed. These maps check only the original every-third-dip selection, not all intervening events of the shorter alias. Raw/processed/QLP use the same photons, not independent observing epochs.

The three-pixel scene around the raw moment contains five TIC neighbors with Gaia identifiers. All five mapped to Gaia DR3; no classifier or eclipsing-binary rows were returned. This incomplete catalog check does not exclude a binary or establish novelty. The source favors the target region, while unique host and physical interpretation remain unresolved. The shorter-period alternating dip sequence still requires binary vetting; no likely new planet is claimed.

[Raw events1](../../tesscut-429034844-s70-20261011/events-1.png) · [Raw events2](../../tesscut-429034844-s70-20261011/events-2.png) · [Processed events1](../../spoc-pixels-429034844-s70-20261011/analysis/events-1.png) · [Processed events2](../../spoc-pixels-429034844-s70-20261011/analysis/events-2.png) · [Gaia query](../../gaia-429034844-scene-20261011/plan.json). Raw ZIP/FITS, processed FITS, frozen inputs, catalog downloads, coverage selection and plot hashes passed the source verifier. Initial source checks are complete; full physical vetting is not.

## Alternating dip source check

Both alternating families of the exact shorter clock now have processed image checks:21/22 usable events, all43 inspected. Both repeatedly localize to the target region, with aggregate moments0.02739pixel apart. Close blends and binary/planet interpretation remain unresolved; this uses the same opened sector, not independent confirmation. [Maps, coverage and provenance](../../parity-pixels-429034844-20261011/ASSESSMENT.md).

## Joint timing diagnostic

A posthoc joint fit aligns sectors42/43/70 at0.466995132days. Alternating-depth contrast varies between sectors; binary/planet nature remains unresolved. The period profile has only one grid point, so its zero-width range is not a measured uncertainty. Original frozen predictions remain unchanged. [Joint plots, controls and limitations](../../joint-clock-429034844-20261011/ASSESSMENT.md).

## Local period-grid refinement

The finer local grid retains the same joint best fit and resolves six conditional likelihood-profile points, spanning0.466994573295–0.466995187526days. This supersedes the coarse single-point resolution limitation but is not a calibrated timing posterior or global cycle-count exclusion. Physical classification is unchanged. [Refinement evidence](../../joint-clock-fine-429034844-20261011/ASSESSMENT.md).

## Gaia radial-velocity context

The exact matched Gaia source has a95.04051 km/s robust velocity range across22 observations and satisfies the catalog variability cuts (p<.01, renormalised goodness of fit>4, at least10 observations;4000 K template within the conservative temperature range). Nineteen observations involved deblending. This strengthens the binary/blended-spectrum alternative but supplies no orbit or phase match to the TESS signal; epoch velocities are not released for this source. Earlier photometric-classifier nonmatches do not negate this independent catalog diagnostic. See [reproducible RV assessment](../../rv-context-429034844-20261011/ASSESSMENT.md). No likely new planet claimed; original timing tests remain inconclusive.

## Explicit close-neighbor alternative

TIC611135702 is2.205834 arcsec from the target at the Gaia catalog epoch, approximately0.105 nominal TESS pixels. Equal-throughput mixing with catalog T magnitudes permits a28.84–33.32% intrinsic neighbor eclipse to reproduce the joint-fit sector/parity depths. This illustrative possibility is not an aperture or host measurement. The parallaxes are formally compatible but proper motions differ; physical association is not established. No epoch spectroscopy/scan geometry identifies the cause of the Gaia RV variation. The existing TESS image localization cannot exclude this close neighbor without calibrated subpixel source tests. [Calculation, checks and caveats](../../close-blend-429034844-20261011/ASSESSMENT.md).

## Conditional PRF source comparison

Sector70 at the joint short clock favors close neighbor611135702 under the fitted scene registration (chi-square357.18 versus983.47). Both host injections recover100/100 under formal noise and41/41 in shifted empirical stacks, but those tests fix the same PRF/registration. A+0.125pixel alignment perturbation reverses the host preference while refitted scene fluxes absorb much of the displacement; no calibrated alignment bound excludes that region. Neighbor contamination is favored conditionally, not uniquely established. [PRF evidence, residual plot and limitations](../../prf-429034844-s70-20261011/ASSESSMENT.md). Original timing tests remain unchanged.

## Scene-flux constraint sensitivity

The free scene fit assigned nearly zero target flux and nearly all pair light to the fainter neighbor. Linking their fluxes at the catalog T-band ratio changes registration and reduces the conditional neighbor chi-square advantage from626.29 to69.00. All five tested ratio factors(0.25,0.5,1,2,4) still favor611135702; this is sensitivity, not a calibrated host probability. Five matched-model registration controls and49 repository tests passed. [Detailed evidence](../../prf-ratio-429034844-20261011/ASSESSMENT.md). The exact host and physical classification remain unresolved.

## Older-epoch source comparison

Processed sectors42/43 provide33/40 usable image windows at the joint clock. Sector42 favors target429034844;43 favors neighbor611135702, matching70. The disagreement survives all five brightness-ratio constraints. Both aggregate stacks/PRF residuals were inspected; individual event maps at the revised clock were not reviewed in this extension. Fixed-template formal/empirical injections and ratio recovery controls pass, showing those controls do not calibrate the model mismatch behind inconsistent real-data attribution. [Full comparison](../../prf-epochs-429034844-20261011/ASSESSMENT.md). Unique host and physical classification remain unresolved; further equivalent fits are deprioritized.
