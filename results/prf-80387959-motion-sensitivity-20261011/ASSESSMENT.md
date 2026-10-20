# TIC80387959: image-gradient sensitivity

This post-hoc test adds fixed x/y gradients of each archived reference scene
as two unconstrained nuisance templates, alongside the original host PRF and
background plane. It uses all eleven events in Sectors63/90 and exactly the
same414 control windows and injection amplitudes as the preceding analysis.
Ephemeris, reference registration and host templates remain fixed. Original
fits are preserved; all new chi-square values satisfy the nested-model check.

Sector63 event345's minimum conditional chi-square falls from1987.74 to732.9
(115 nominal degrees of freedom with the extra templates). The target's
disadvantage relative to the best host falls from211.56 to27.97. The best host
remains80387965, but every model still fits poorly. The reviewed residual image
retains structured positive/negative features. This is not a clean neighbor
localization or proof that motion alone explains the event.

The recorded POS_CORR outside-minus-inside means for event345 are
(+0.005741,-0.002438)pixels, larger than for the other inspected Sector63 events.
This is consistent with investigating a pointing contribution; it is not an
independent causal attribution or calibrated motion measurement. Sector90's
POS_CORR columns contain only zero values, so their zero differences cannot
establish absence of motion. No placeholder values were treated as such evidence.

Across374 positive-amplitude target-injection controls, the correct target is
preferred152times with the gradient model versus130times previously. The40
zero-amplitude event523 controls remain null controls, excluded from recovery
counts. Overlapping windows, identical injected PRFs and uncertain exchangeability
prevent interpreting these counts as completeness or confidence. Extra nuisance
terms can absorb astrophysical structure; improved fit alone is not validation.

All three generated residual plots were visually reviewed. Host preferences
remain model-dependent and the recurring signal is not promoted to a likely
planet. Remaining limitations include PRF/registration mismatch, correlated
noise, and whether more flexible scene terms confound the source itself.
