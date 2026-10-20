# TIC106583384: discovery images strongly favor an off-target source

The searched 2.468146633-day signal is a contaminating event near TIC106583444 / TIC780959515, about2.85pixels from TIC106583384. Deprioritize the on-target planet interpretation. This does not establish whether the off-target event is a stellar eclipse or planet, nor exclude other planets around the target.

Only discovery sectors33/34 were opened, at the unchanged [original frozen clock](../source-check-106583384-20261012/frozen.json). Each contributes ten usable image events. Extra sector7 and reserved61 remain unopened by this investigation. No period/timing optimization was performed.

| Sector | Difference peak SNR | Moment offset from target, pixels | Target source fit χ² | Preferred neighbor χ² | Fit dof |
|---|---:|---:|---:|---:|---:|
|33|266.3|2.642|161575.7|1784.1|117|
|34|306.7|2.923|192672.4|724.8|117|

Both stacked maps and all20 individual maps visibly concentrate the lost light near the neighbor, away from the target. These figures were inspected: [stack comparison](prf-comparison.png), [individual events](events.png). Target position is black; preferred neighbor position is green. All individual and leave-one-out fits favor one of two close neighbor entries rather than the target. All18 common-registration perturbations on the ±0.1pixel grid retain a neighbor winner; this is sensitivity analysis, not an uncertainty distribution.

The nominal best template is labeled780959515 because the magnitude-sorted catalog deduplication retained that row first. [The preserved TIC catalog](../neighbors-106583384-20261012/neighbors.json) explicitly marks it DUPLICATE of106583444, with identical coordinates and Gaia source5616909889859313536. TIC106583444 is marked SPLIT. Nearby780959519 is associated with Gaia5616909889865304064 and has duplicate_id106583444 but distinct coordinates, about0.1pixel away. Some sector34 events, leave-one-out results and perturbed registrations favor this second entry. The exact close-component identity is unresolved. The prior [VSX review](../review-106583384-20261012/ASSESSMENT.md) includes a VAR entry at the first Gaia identifier, with a different catalog period; it is not an exact match to this searched clock, and Gaia-release identity has not been independently reconciled.

## Assumptions and verification

The scene uses TIC positions linearly propagated from J2000, fixed Tmag relative fluxes, one common image registration and a plane. Source hypotheses include catalog stars within3pixels of the target; image-scene sources use T≤18 and a stamp margin. This is a conditional comparison, not exhaustive catalog completeness. Models are mission PRFs at surrounding detector positions. The isolated model cache is `data/prf-106583384-20261012/`; pixel/catalog/model download URLs and SHA-256 hashes are retained in localization manifests, neighbor source.json and models.json.

[Independent QR verification](verification.json) reconstructed1050 linear source fits for stacks/events/leave-one-out images, checked input hashes and recovered a same-model synthetic registration. [Raw reconstruction](raw-verification.json) checked20 event maps; [independent event arithmetic](event-verification.json) separately reconstructed raw in/out means, formal variances and precision-weighted stacks. Registration tests and plots preserve their scripts. These checks establish reproducibility, not real-world PRF accuracy.

Preferred fits still have poor residuals (χ²/dof≈15.2 and6.2), visible in the inspected residual images. Calibration mismatch, scene incompleteness and diagonal-error assumptions prevent calibrated host probabilities and secure close-component selection. Nevertheless the resolved ~2.85pixel displacement, recurring in all20 maps, provides strong direct evidence against the target hosting the searched dip. No intrinsic eclipse depth, binary classification or planet probability is inferred here. Investigating the neighboring system would need its own explicit source/dilution and catalog review.
