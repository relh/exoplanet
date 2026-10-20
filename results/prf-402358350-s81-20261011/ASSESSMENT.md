# TIC402358350: sector81 favors the target region, with inadequate source fits

The later sector81 images add positive target-region evidence: the target ranks first in the whole stack both with and without scene-motion terms, and in both individual events with motion. However, large structured residuals and local-region sensitivity prevent secure host attribution. The signal remains unresolved (internal APC), without a planet probability or promotion to a validated candidate.

The period11.769544332days, epoch2392.992868940BTJD and duration0.144day were copied unchanged from the expanded primary model frozen **before sector81 photometry**. No81 timing fit, alternate phase search or clock selection occurred. Sector81 photometry had been deliberately opened and verified by the coordinator before this source test downloaded81 target pixels. This is a source diagnostic in a separate observing epoch, not a new independent photometric recovery or a reason to relax the original timing gate.

| Whole-stamp model | Preferred host | Target chi-square / dof | Runner-up / chi-square |
|---|---|---|---|
| Source + plane |402358350|576.74 /117|1918682446 /610.62|
| Source + scene gradients + plane |402358350|554.46 /115|1918682446 /573.56|

Target amplitudes are positive; motion-only chi-square is706.65. These formal improvements are conditional on an inadequate model and do not give calibrated significance or host odds. The scene residual RMS is0.633% of peak, with nominal registration[0.01535,0.00421]pixels away from the bound. The difference-image residuals are much more structured than diagonal pixel errors explain.

There are two usable image events (95 and96). Both prefer the target under scene-motion fits. Source-only fits prefer the target for95 and402358383 for96. With two events, leave-one-out stacks repeat the other event and provide no additional independent tests. The smaller local region prefers a different source:

| Region | Preferred motion-model source | Best chi-square / dof | Target chi-square / dof |
|---|---|---|---|
|2.5-pixel radius|1918682448|223.63 /13|246.94 /13|
|3.5-pixel radius|402358350|338.02 /31|338.02 /31|

The local-model figure was inspected: strong neighboring positive and negative residuals remain near the target, even where the target wins. A source coefficient with high formal SNR in these fits cannot override their model mismatch. The test strengthens evidence that the signal originates near the target region, but neither fixes the earlier sector-dependent host ambiguity nor rules out close stellar companions.

## Methods and verification

The same catalog-ratio scene, T-band flux assumptions, magnitude/geometry selection, approximate proper motions, fixed nominal scene registration and source/plane models used previously are retained. Motion terms are0.01-pixel finite differences of the entire catalog-ratio scene. Their free coefficients are not measured pointing offsets. All99 geometric source hypotheses, both events, both omission stacks and both diagnostic regions are retained. Registration uncertainty was not marginalized or scanned in this run.

`frozen.json` links and hashes the pre81 expanded model and the completed held-out photometry execution/verification records. `pixels/localization.json` retains the target-pixel URL, retrieval time, SHA-256 and FITS checksum results. `models.json` and `download_models.py` retain PRF URLs and hashes. The source plan, script hashes, fitted values and arrays are preserved; no other new observations were opened.

`verify.py` reconstructs both raw event images and the combined difference image, checks FITS identity and pixel/PRF hashes, and reproduces693 hypothesis comparisons using an independent QR solver. This includes source-only/motion-only comparisons, whole stamps, events, omissions and local regions. It also checks that the original expanded freeze preceded81 photometry, that held-out photometry completed before the pixel retrieval, and that the exact same primary clock was used here. Matched-template additions verify coefficient arithmetic, not empirical PRF accuracy. All checks passed.

Retain this positive target-region result together with its failed fit adequacy and the [original frozen-clock photometric test](../heldout-402358350-s81-20261011/ASSESSMENT.md). Further useful work needs discriminating physical/binary or instrumental evidence; selecting another favorable fit of the same pixels would not independently establish the host. No new planet or numerical host probability is claimed.
