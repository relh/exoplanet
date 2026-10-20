# TIC402358350: discovery images leave the host unresolved

The original11.772740-day clock produces compact positive difference flux near the target in sectors40/41. Image moments are0.586 and0.279pixels from the header target position, respectively. Neither these offsets nor the conditional PRF fits establish the host. Only already-opened discovery observations were used; added sector54 and reserved81 were not accessed.

| Sector | Preferred template | Chi-square / degrees of freedom | Target chi-square | Event/omission stability |
|---|---|---|---|---|
| 40 | TIC402358383 | 199.61 /117 | 213.88 | The two individual events prefer different hosts: target and402358383. |
| 41 | Target402358350 | 441.85 /117 | 441.85 | One event prefers target, the other1918682563. |

The nine chosen common-registration perturbations change the preferred host: sector40 favors402358383 in5/9, target in2/9 and1918682563 in2/9; sector41 favors target in6/9 and1918682446 in3/9. These fractions are sensitivity diagnostics, not host probabilities. All nominal stack and omission winners have positive fitted amplitudes.

Neighbor402358383 has T=17.4343 versus target9.43219;1918682446 has T=17.9009 and1918682563 T=15.8656. The crowded scene, uncertain flux allocation and inadequate residuals prevent assigning the shallow dip to the target or a particular neighbor. The sector41 residual map has substantial structure. A nominal target win cannot be treated as calibrated attribution, and the sector40 neighbor win alone does not exclude a planet.

The existing PRF method uses catalog T-band flux ratios, linear proper-motion propagation, out-of-event scene registration, then one variable-source template plus a plane. Its assumptions and template selection are preserved in plan.json. It does not model every instrumental effect or unresolved companion. Four individual event differences reconstruct from hashed FITS;880 linear fits reproduce with a separate QR solver. The synthetic registration test checks arithmetic under the assumed model, not real-world PRF accuracy. Registration sensitivity uses an illustrative ±0.1pixel grid, not an estimated uncertainty distribution. Difference and model/residual plots were visually inspected.

Together with the [discovery review](../review-402358350-20261011/ASSESSMENT.md), this supports retaining the signal for further investigation, internally APC, without claiming a likely planet. Next: after the parent batch terminal audit, freeze a timing profile and decision criteria from discovery data before opening additional observations. Source attribution and binary alternatives will remain necessary even if later dimming recurs.
