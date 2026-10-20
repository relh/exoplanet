# TIC 469995081: adjacent epoch favors neighboring known-binary contamination

Sector 77 was opened at the unchanged Sector 76 period 6.227890386 days,
epoch BTJD 3371.098490706 and duration 0.133056 days. No refitting was used.
The inspected map shows a compact positive residual over three event windows,
with peak formal SNR 46.67. Its moment lies 1.320 pixels off target, near
TIC 469995046 (0.072 pixels), TIC 2019765753 (0.083 pixels) and
TIC 469995053 (0.179 pixels). The close entries cannot be uniquely resolved
by this moment calculation. Background modeling and PRF uncertainties remain.

The original Sector 76 map remains entirely negative and invalid for direct
localization. The [background-mask audit](../tesscut-469995081-s76-20261010/background-mask-audit.json)
finds zero background pixels under both two- and three-pixel T<17 catalog
exclusions, so no plane was fitted. Similar apparent residual positions in
that failed map do not make it an independent validated localization.

[Gaia queries](../gaia-469995081-neighbors-20261010/results.json) return three
DR3 sources and one eclipsing binary. The DR2-to-DR3 mappings for TIC
469995046 and TIC 2019765753 are ambiguous: both map to the same pair of
DR3 sources. The binary, DR3 2199086069466635392, has period 18.710369181
days, close to three times the selected TESS period (18.683671159 days),
with a 0.143% discrepancy. This is a harmonic correspondence, not exact
period or ephemeris agreement. The precise catalog component remains uncertain.
The neighbor QLP lookup has no Sector 76 or 77 product; explicit errors remain.

The adjacent-sector compact off-target signal, nearby known binary and harmonic
period favor contamination. This updates the original unresolved assessment;
it does not overwrite the failed checks or establish a new planet or binary.
