# TIC 30832104 sector-9 source check

The two sector-9 difference-image events favor **TIC 30832145** over the bright search target. Both individual events, and therefore both single-event omission stacks, favor that same neighbor; these are two events, not four independent replications. All nine common registration perturbations at −0.1, 0, +0.1 pixels on each axis also prefer it. This is strong contamination evidence for the original on-target planet interpretation.

The neighbor fit has chi-square 403.8 for 117 degrees of freedom, versus 2991.4 for the target. Residual structure remains, so the model is imperfect. These diagonal-error fit differences are not calibrated significances or host probabilities. The inspected plot places the positive dimming away from the target, near the neighbor; it does not determine the neighbor's physical variability or exclude unresolved companions there.

The existing PRF routine registers an out-of-event catalog scene using fixed Tmag flux ratios, a common displacement/normalization and background plane. Catalog positions are propagated linearly with TIC proper motions; parallax and catalog/PRF uncertainties are not propagated. The scene RMS is about 0.71% of its peak. Each difference-image hypothesis fits one source plus a plane. No transit clock is reoptimized for these images.

The verifier checks raw/mission-model hashes and independently reconstructs all 90 stacked, event and omission hypothesis fits using a QR solver. A matched-model synthetic registration check passes. Four DR2-to-DR3 mappings reconcile, including the preferred neighbor's identity as Gaia DR3 5331325247918681600. The source is listed VAR by VSX, but its catalog timescale differs greatly from the TESS feature, leaving the physical cause unresolved.

Only discovery sector 9 is localized here; no independent observing-epoch localization or later-sector recurrence is claimed. Sector 62 remains reserved. No new planet is established.
