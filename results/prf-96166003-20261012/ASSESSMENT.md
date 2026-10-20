# TIC96166003: discovery images favor the target, with close-source limits

At the unchanged original discovery clock, both43/44 image stacks favor the target among the tested catalog sources. The residual chi-square is modest, unlike several strongly off-target campaign passes. This supports target attribution but does not establish it: low image SNR, faint close sources and registration/event sensitivity remain. No sector19 or59 data were accessed by this investigation.

| Sector | Events | Target chi-square/dof | Best alternative in T≤21 scene | Alternative chi-square/dof |
|---|---|---|---|---|
|43|23|121.57/117|661159657|122.33/117|
|44|23|90.59/117|661159657|99.15/117|

The original T≤18 scene gives target chi-square121.58/117 and90.59/117; all46 leave-one-out stacks and18 chosen registration trials favor target. Individual event winners vary widely because the individual differences are noisy. These are not46 independent host confirmations.

## Faint-source sensitivity

Inspection of the catalog revealed that the default T≤18 scene omitted close faint objects potentially relevant to a shallow dip. The separately frozen [faint-scene plan](faint-scene/plan.json) extends the cutoff toT≤21, retaining the same clock, geometry, fitting procedure and3pixel hypothesis radius. Both nominal stacks still prefer target, but sector43 is almost tied with TIC661159657 (T20.6092,13.43arcsec away). Fifteen of23 sector43 omissions and four of nine illustrative±0.1pixel registration trials prefer this close source; sector44's23 omissions and all nine registration trials remain on target. This shows that source selection matters and weakens the nominal complete stability claim.

Under the simplified assumption that target and neighbor contribute with equal aperture throughput and catalog T magnitudes represent their fluxes,661159657 contributes at most84ppm of combined flux even if fully eclipsed. Explaining281ppm would require about334% intrinsic dimming. This makes that faint source physically unfavorable under those assumptions, but is not a calibrated exclusion: unequal extraction throughput, catalog errors, unresolved sources and PRF model mismatch are not modeled. The somewhat brighter omitted neighbor661159648 (T18.5322,16.70arcsec) could produce570ppm when fully eclipsed and needs about49% intrinsic dimming to imitate281ppm. Its chi-square is154.83/117 in43 and104.04/117 in44; it remains a physically possible diluted-binary alternative despite the less favorable templates. These flux-ratio illustrations are not fitted eclipse depths or planet probabilities.

## Verification and interpretation

The standard scene uses catalog T-band flux ratios, linear proper motions, a common registration from the out-of-event scene and one variable-source template plus plane. Fixed registration is used for nominal event/omission fits. Synthetic registration checks test the assumed model only. Both model/residual plots were visually inspected; the dimming is near target, with weak residual structure rather than a spatially separate bright eclipse.

The original and faint-scene [raw reconstruction](raw-verification.json) checks each reproduce46 event differences from already-cached pixel FITS. Independent QR verification reproduces658 and2303 linear fits respectively, checking raw/model hashes and saved coefficients/chi-square. [Registration sensitivity](faint-scene/registration-sensitivity.json) is a selected grid, not a measured uncertainty distribution. Model comparisons are conditional on templates and diagonal errors; no calibrated host odds, binary exclusion or planet validation is claimed.

This analysis used only43/44 pixel files, with no photometric clock changes and no new target observation download. The parent separately owns additional-sector timing work. Retain the target as plausible pending that timing evidence and fuller false-positive constraints; do not translate template ranks into a percentage likelihood.
