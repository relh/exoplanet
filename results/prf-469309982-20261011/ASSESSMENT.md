# TIC469309982: source attribution fails to agree between discovery epochs

The 2.8905-day, approximately 140-ppm photometric dip remains measured, but the images do not establish dimming on the target. Eight events in sector9 and eight in sector36 were measured at the unchanged expanded-discovery clock. Sector9's conditional PRF comparison favors TIC469310012; sector36 favors TIC469309967. These are different stars. The source remains unresolved, and this lead is deprioritized as a likely on-target planet pending a better explanation of the image residuals.

| Sector | Preferred hypothesis | Best chi-square / dof | Target chi-square / dof | Event-omission stacks |
|---|---|---:|---:|---|
|9|TIC469310012 (T14.31)|274.25 /117|353.96 /117|8/8 prefer the same neighbor|
|36|TIC469309967 (T17.18)|1632.63 /117|1830.99 /117|8/8 prefer the same neighbor|

The sector9 hypothesis persists at all nine tested registration offsets. Sector36 prefers TIC469309967 at eight offsets and TIC469309974 at one. Individual-event winners vary widely: the target is preferred in only one sector9 event and no sector36 events. These repeated omissions are correlated tests, not independent confirmations. The sector36 fit is especially poor: large positive and negative structures remain around the bright source, and the single-source model cannot explain them. The figures were inspected. The pattern warrants a pointing/motion-residual diagnostic; it does not prove a specific instrumental cause or identify a physical eclipsing source.

The out-of-event scene uses catalog T-magnitude flux ratios, a common registration and a plane; fractional residual RMS is1.32%/1.62%. Linear TIC proper motions are applied. Neighbor alternatives within three pixels and small registration offsets are conditional, selected from the local geometry. Raw TIC Gaia identifiers are DR2-era catalog values and are not assumed to establish DR3 identities. The separately queried nearby VSX eclipsing binary has a different period and is not established as the cause.

All 16 raw event-difference images reproduce from hashed FITS data, whose target/sector identities were checked. An independent QR calculation reproduces 884 source-hypothesis fits, including stacks, individual events, event-omission stacks and registration checks. Matched synthetic registration recovers the inserted shift numerically; this is not an empirical host-attribution calibration. PRF and raw-image hashes are retained. Formal chi-square differences are not calibrated host probabilities, and remaining model mismatch is material.

Sectors63 and reserved64 remain unopened. No independent-epoch planet confirmation or planet radius is claimed. Keep the favorable photometric checks and possible secondary dip together with these unfavorable source diagnostics. No full-domain discovery pass was established by this seeded-search experiment.

A subsequent [motion-nuisance comparison](../prf-motion-469309982-20261011/ASSESSMENT.md) favors a common neighbor in the stacks but leaves large residuals and inconsistent signed target amplitudes. It does not resolve the physical source.
