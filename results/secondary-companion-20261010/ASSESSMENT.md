# Off-phase eclipse companion diagnostic

The original search tests a secondary at phase0.5. TIC395477762 demonstrated
that a displaced eclipse can escape this test. The new `exoplanet.secondary`
companion scans other phases and durations after discovery. It excludes the
primary and its surroundings, retains the strongest brightening as a control,
and counts individually supported events for the selected dip. The selected
SNR is explicitly **not calibrated significance** and adds no automatic planet
or binary classification. Original running searches/settings remain unchanged.

Three deterministic tests recover a displaced secondary, prevent the primary
from contaminating the scan, and verify that a single isolated dip does not earn
repeated-event support. The complete suite has42 passing tests.

Training-only results for the three initial late-sector screen passes:

| TIC | Selected dip phase | Depth ppm | Selected SNR | Supported events | Assessment |
|---|---:|---:|---:|---:|---|
|395477762|0.47287|2011|58.43|4|Recovers the manually identified deep secondary; strong binary evidence|
|68286478|0.11303|257|6.44|2|Weak, selected feature; not a credible companion detection|
|420359321|0.19811|517|16.60|1|Large nominal SNR without repeating individual support; not a credible secondary|

A separate retrospective run on already-opened SPOC Sectors10/36/37/63 for
**TIC80387959** finds a maximum off-phase dip147±51ppm (selected SNR2.87),
comparable to the largest brightening's absolute SNR2.85, with zero supported
individual events. No convincing secondary is found. This does not exclude
an eclipsing binary or resolve the host-star ambiguity; the strongest original
signal remains unresolved. Per-sector measurements reuse the selection data and
are not independent validation.

`plan.json` records the late-screen inputs; `80387959.json` records the prior
primary ephemeris hash, source hash, sector provenance and separate policy.
