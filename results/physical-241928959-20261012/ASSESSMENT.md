# TIC241928959: short transit shape leaves radius and grazing ambiguity

The cached sector92 event can be fit as an undiluted target-host occultation, but the inferred shape is not a secure planet interpretation. Free circular fits prefer density about16g/cm³, substantially above the nominal catalog3.2g/cm³. A broad stellar prior instead gives a grazing configuration with a much larger radius ratio and almost no data-fit penalty. This degeneracy, uncertain stellar parameters and the already unresolved close blend prevent physical validation or a reliable planet radius.

The single declared comparison comprised both existing detrendings and three cases: target with free axis, target with a broad axis prior, and a diluted close-neighbor illustration. No additional observations, search families or subsequently tuned fitting matrix were added.

## Inputs, cadence and assumptions

The frozen [plan](plan.json) hashes the existing refined3.532592898d clock, raw QLP92 file, discovery metadata, TIC neighbor catalog and implementation. TIC241928959 has nominal mass0.62766±0.02076 solar masses, radius0.65071±0.02022 solar radii, Teff3396K. The mass/radius combination implies about3.21g/cm³; the plan retains the catalog's separate density field verbatim and the fit uses mass/radius directly. The SPYGLASS youth probability0.40 and lack of cluster assignment do not validate an age or radius; nominal stellar errors can understate model uncertainty.

The raw QLP `TIMEDEL` is200seconds; median timestamp spacing is200.016seconds. The existing fitter infers exposure from contiguous cadence blocks, giving0.002315d after rounding (200.016seconds), and supersamples11 times. Integration therefore uses cadence as a close exposure approximation, not a new measured duty cycle. Native published QLP errors and DET_FLUX are used; fluxes were not rebinned.

All five usable events enter the1.5d reduction. The unchanged2.5d detrending removes the in-transit samples of one event, as previously documented; this reduction contains four usable transits. The fitter reports **six local windows** in each reduction because it retains windows with at least eight samples even when only baseline survives. [cadence-events.json](cadence-events.json) makes this explicit; six windows do not mean six observed transits. No masked event was restored or selected out to improve the fit.

Circular orbits, a dark negligible-mass occultor, fixed quadratic limb darkening(0.4,0.2), beta1 independent errors and one local intercept/slope per window are assumed. Bounds and three impact starts are unchanged from the shared fitter. A local copy adds reporting of every start's parameters, termination and active bounds without changing its objective. The prior is Gaussian in log(a/R*) with sigma0.25, corresponding approximately to log-density sigma0.75 at fixed period—an explicitly broad illustration, not a stellar posterior.

## Conditional fits

| Window | Case | Radius ratio | Impact | a/R* | Duration(d) | Circular density(g/cm³) | Data chi-square/dof |
|---|---|---|---|---|---|---|---|
|1.5d|Target, free axis|0.1257|0.840|21.78|0.03870|15.66|562.96/543|
|1.5d|Target, broad prior|0.3072|1.135|17.18|0.04260|7.69|564.67/543|
|1.5d|Diluted neighbor illustration|0.5000|0.146|35.35|0.04749|67.01|567.41/543|
|2.5d|Target, free axis|0.1232|0.829|22.01|0.03874|16.17|459.75/441|
|2.5d|Target, broad prior|0.3112|1.142|16.60|0.04378|6.93|461.51/441|
|2.5d|Diluted neighbor illustration|0.5000|0.324|32.19|0.05116|50.60|464.99/441|

The target broad-prior fits are grazing (impact greater than1−radius ratio) and cost only about1.7 data chi-square relative to the free solutions. Using the nominal stellar radius, their radius scale is roughly0.20solar radii, versus0.08solar radii for the free fits. Neither is a robust companion size measurement. No uncertainties or population prior establish which branch is physical. Eccentricity, stellar-model error and unresolved dilution can change the density inference. A reduced chi-square near1 under supplied errors is not binary exclusion.

All18 starts report success; the three objectives within each case agree to better than1e−5. Target solutions have no active numerical bounds. Both neighbor fits hit the radius-ratio upper bound0.5, retained in the results. Consistent local convergence is not a guarantee of a global optimum.

## What the neighbor comparison does and does not mean

Close TIC241928961 has nominal mass0.69 and radius0.828855solar units, but **no catalog errors** on these parameters. They are not validated inputs and no uncertainties were invented. Its T=15.9232 versus target12.6135 implies a4.529% contribution in an illustrative equal-throughput two-star blend. Flux and errors were linearly transformed by that fixed fraction before fitting, equivalent to modeling the blended signal under this assumption. Actual QLP aperture throughput/crowding is unavailable, and other sources are ignored.

The constrained dark-occultor fit reaches its radius bound and high apparent density, exposing inadequacy/tension of this restricted model. It is **not a general eclipsing-binary test**: a luminous or massive companion, larger radius ratio, eccentric orbit or incorrect stellar/dilution inputs are outside the model. Thus the poor physical parameters do not invalidate the blend alternative already retained by source checks. No binary likelihood or FPP was calculated.

## Verification and outcome

[Verification](verification.json) reconstructs both reductions directly from raw FITS and independently solves weighted event baselines around a direct batman model, reproducing all six data chi-square values and prior penalties. It uses the same transit library, so does not independently implement occultation physics or prove optimizer completeness. The [figure](fits.png) was visually inspected at fine phase resolution; different physical assumptions produce similar shallow folded shapes. The initial verification attempt had a local variable-name collision and failed before writing a verification result; corrected verifier passes. No scientific fit changed because of that reporting error.

The prior source evidence still favors the target region, but parity is limited to one usable odd event and half-phase non-detection does not exclude binaries. Retain the signal as unresolved/internal APC, now explicitly noting grazing/radius/density ambiguity rather than reporting a secure planet radius. No more flexible models were added after this declared comparison. Independent observations or externally constrained stellar/binary properties are the useful next evidence.

Reproduce arithmetic and figure with `uv run python results/physical-241928959-20261012/verify.py`; inspect event coverage with sibling `cadence_audit.py`. No shared scientific source, docs or observations changed.
