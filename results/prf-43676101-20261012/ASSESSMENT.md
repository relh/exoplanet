# TIC43676101: discovery dip is strongly off-target near TIC43676071

Deprioritize the on-target planet interpretation. Both discovery image stacks place strong dimming about3.6–3.8pixels from the target, near neighbor TIC43676071 at82.34arcsec separation. This is **not** the previously identified27.77arcsec ROT neighbor TIC43676092. The neighbor's astrophysical classification remains unresolved, and the image model's imperfect residuals do not justify exact host probabilities.

Only discovery sectors52/53 were downloaded as target pixel files at the coordinator-frozen original2.1477693228d clock. No additional26/79 or reserved80 photometry/pixels were opened.

| Sector | Events | Image offset(pixels) | Peak image SNR | Best neighbor chi-square/dof | Target chi-square/dof |
|---|---|---|---|---|---|
|52|5|3.791|276.8|1053.19/117|206559.63/117|
|53|9|3.645|349.6|1070.98/117|316803.91/117|

The target-only fitted amplitude is negative in both sectors. Every one of14 individual events, all14 leave-one-out stacks and all18 chosen common-registration perturbations favor43676071 among the tested sources. The stack and omission neighbor amplitudes are positive. These sensitivity checks are not independent observations or probability estimates. The large displacement and consistent event images are stronger evidence against the target than a modest poor-fit PRF ranking alone.

Neighbor43676071 has T=11.1483 versus target10.013 and TIC Gaia DR2 identifier4548836254456444544. Its flux lies near/beyond the stamp edge, so image moments are truncated and exact attribution to it or a fainter close companion is not proved. The scene also includes a fainter T18.3036 neighbor43676070 near the edge, excluded by the declared T≤18 scene cutoff; this incompleteness and the large best-fit residuals matter for distinguishing close sources. The result still strongly excludes the named target as the dominant source of these dips under the tested scene.

## Model and checks

[plan.json](plan.json) declares a posthoc catalog-ratio scene, linear proper-motion approximation, common registration and single variable source plus plane. Hypothesis radius was explicitly expanded to5pixels because the visible difference flux lies beyond the standard3pixel search radius. It was frozen before fitting, with the original clock unchanged. [registration-sensitivity.json](registration-sensitivity.json) retains all±0.1pixel grid trials; this grid is illustrative rather than a measured registration uncertainty.

[raw-verification.json](raw-verification.json) reconstructs all14 event differences from hashed pixel FITS. [verification.json](verification.json) independently reproduces728 linear fits with a QR solver and checks raw/PRF hashes and the synthetic registration recovery. These verify arithmetic under the model, not real-world PRF accuracy. Pixel and model/residual plots were visually inspected; residual structure is concentrated near the stamp-edge source, while the target position is far from the main dimming.

The initial [discovery review](../review-43676101-20261012/ASSESSMENT.md) remains preserved and is superseded for target candidacy by this localization. No added/reserved data are needed to deprioritize the on-target interpretation. Any investigation of the neighbor's physical nature needs a separately explicit plan; this report does not label it an eclipsing binary or a planet.
