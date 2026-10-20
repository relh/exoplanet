# TIC402358350: scene-motion terms improve one sector but do not establish the host

The target becomes the preferred template in both discovery-sector stacks after adding two derivatives of the catalog-ratio scene as motion nuisance terms. This changes the source-only ranking in sector40 and makes the sector40 fit substantially better. It does **not** validate an on-target transit: sector41 retains large structured residuals, close alternatives remain, and individual events disagree.

| Sector | Target + scene-motion chi-square / dof | Target source-only chi-square / dof | Next template with motion | Next-template chi-square |
|---|---|---|---|---|
|40|116.62 /115|213.88 /117|1918682446|119.94|
|41|431.81 /115|441.85 /117|1918682446|439.44|

The target coefficient remains positive. Motion-only fits have chi-square228.08 and554.84, respectively. Adding a source component improves this limited model, but chi-square differences are not calibrated planet significance or host odds. The nearby-template alternatives differ only slightly once motion is included.

Each sector has only two usable difference events. Single-event and leave-one-out winners include the target and1918682563 in sector40, and the target and1918682448 in sector41. With two events, omission tests simply reproduce the other single event; these are not independent replications.

Both circular diagnostic regions also prefer the target, with the following conditional signed amplitudes. Positive denotes dimming.

| Sector | Radius (pixels) | Target amplitude / formal error | Target + motion chi-square / dof |
|---|---|---|---|
|40|2.5|9.29|17.91 /13|
|40|3.5|10.36|42.86 /32|
|41|2.5|11.11|127.73 /13|
|41|3.5|10.72|161.94 /32|

The local model/residual figure was inspected. Sector40's displacement-like structure is substantially absorbed; sector41 retains strong neighboring positive and negative pixels around the target. The simple first-derivative approximation is inadequate there. A better fit with added terms does not prove pointing is the cause, and a target-favoring nuisance model cannot be chosen as the definitive localization.

## Fixed inputs and verification

Only already-opened sectors40/41 were used, at the unchanged original discovery clock and the same nominal scene registration as the parent source-only analysis. All source hypotheses, per-event differences and omission stacks are retained. Scene stars use the same catalog T-band ratios, proper-motion approximation, magnitude limit and geometry as the parent run. The gradients here are finite differences of the **whole fitted catalog-ratio scene**, not the target PRF alone. The derivative step is0.01pixel. Nuisance coefficients are free signed linear amplitudes, not calibrated measured pointing offsets. Registration uncertainty is not marginalized.

models.json is copied from the parent analysis; its downloader-script hash identifies that original download record. No PRFs or pixels were downloaded. The verifier checks raw/PRF hashes and exact agreement of stacked and individual image arrays with the parent. A separate QR solver reproduces1232 hypothesis comparisons across whole stamps, individual events, omissions and local regions, including source-only and motion-only comparisons. Matched-template additions recover the inserted coefficient; these numerical controls do not test empirical PRF accuracy. Local-region plan/script hashes and unopened sector54/81 caches were checked. No shared scientific module changed.

## Effect on next steps

Keep the signal unresolved (internal APC), with more favorable but still model-dependent target attribution in sector40. This test weakens a simple interpretation of the sector40 source-only neighbor win; it does not resolve the sector41 model failure or establish a likely planet. Proceed with the separately frozen timing experiment only after the parent batch audit permits opening observations. Further source work should seek evidence that discriminates instrumental residuals and hosts, not repeatedly optimize the same images until one model favors the target. The [original source-only evidence](../prf-402358350-20261011/ASSESSMENT.md) remains part of the assessment.
