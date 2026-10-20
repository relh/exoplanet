# TIC429034844: older epochs disagree on the close-pair host

New processed-pixel downloads for sectors42 and43 were tested with the same retained joint short clock, quality-zero event gates and mission PRF method used for70. These are distinct observing epochs, but their light curves already contributed to the clock; this is not blind timing confirmation. Initial download/analysis wrappers both succeeded. Their33 and40 usable event windows were independently counted; no gate was relaxed.

Both aggregate difference images and both PRF model/residual plots were inspected. Each shows compact dimming in the blended target region, with structured residuals remaining. Individual event maps at this clock have not yet been reviewed in this two-sector extension; aggregate appearance alone must not imply all events are clean.

| Sector | Events | Free scene: target / neighbor chi-square | Catalog-ratio scene: target / neighbor chi-square | Preferred hypothesis |
|---:|---:|---:|---:|---|
|42|33|403.63 /483.58|405.76 /471.17|Target429034844|
|43|40|468.71 /276.64|366.05 /327.55|Neighbor611135702|
|70 (previous)|43|983.47 /357.18|364.57 /295.58|Neighbor611135702|

The ratio-constrained preference remains unchanged across all five tested factors(0.25,0.5,1,2,4) within each sector, so varying that constraint does not reconcile sector42 with43/70. These conditional chi-square values must not be summed into a host probability: diagonal formal errors omit scene alignment and PRF mismatch, and shared model errors are not calibrated.

Each new sector recovers both synthetic hosts100/100 under matched formal noise and41/41 in shifted empirical stacks. Ten noiseless ratio-constrained scene controls recover the known alignment within1e−5 pixel. Passing these controls alongside conflicting real-data host preferences demonstrates their limited scope: the same PRF is used for injection and recovery, and registration/model mismatch is not sampled. Empirical controls overlap and are not independent trials.

Disposition: the host remains unresolved across epochs. A close-neighbor eclipse remains viable; neither the target nor neighbor is securely established as the variable source. The Gaia RV variability still strengthens binary/blended-spectrum alternatives, without an orbital phase match. No likely new planet is claimed. Deprioritize more equivalent conditional fits unless there is a new way to constrain instrument-model error or independent spatial/spectroscopic information.

[Sector42 stack](../spoc-pixels-429034844-s42-20261011/analysis/difference.png) · [Sector43 stack](../spoc-pixels-429034844-s43-20261011/analysis/difference.png) · [Sector42 PRF residuals](../prf-429034844-s42-20261011/prf-fits.png) · [Sector43 PRF residuals](../prf-429034844-s43-20261011/prf-fits.png) · [Coverage](coverage.json) · [Verification](verification.json).

Raw pixels/model hashes, common-clock identity, exact stack reproduction, conditional fits, independently counted event gates, predetermined ratio grids and ten recovery controls passed verification. Existing algorithms were reused; no fresh full-suite test claim is made for this configuration-only extension. Original held timing tests remain inconclusive.
