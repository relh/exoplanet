# TIC 80387959: event-level host stability

The repeatable 4.19217-day signal still cannot be securely assigned to the
target. All five original stacked difference images, formal errors and fixed-host
chi-square values reproduce numerically before this sensitivity analysis.
The original pixel hashes and script provenance are verified.

We keep the frozen ephemeris, sector registration, four host templates and
background-plane fit unchanged. Each of 28 event images is fitted separately,
and each sector stack is refitted after omitting each event in turn. All outcomes
are retained; no preferred subset replaces the original result.

| Sector | Full-stack preferred host | Leave-one-out preferred hosts |
|---|---|---|
|36|80387959|Target5/6;80387961 once|
|37|80387959|Target3/5;80387961 twice|
|63|80387965|80387965 four times;target once|
|90|80387961|80387961 five times;937808821 once|
|100|80387959|Target4/6;937808821 once;80387961 once|

Every sector has at least one omitted-event stack whose preferred host differs
from the full stack. Sector63's neighbor preference changes to the target when
event345 is omitted. Sector90 never favors the target in these omission tests.
Individual-event preferences also vary; all winning fitted amplitudes are
positive. The stability plot was visually inspected.

This test demonstrates sensitivity to event selection, not which host is true.
The leave-one-out stacks overlap and are not independent replications. Registration
is kept fixed rather than refitted, so the test deliberately isolates event
contributions within the existing model; it does not propagate registration
uncertainty. Formal diagonal errors, shared instrumental residuals and PRF mismatch
remain limitations. Chi-square differences are not posterior probabilities or
calibrated significance. Independent earlier empirical controls remain relevant
and are not superseded by these diagnostics.

No period or event-time retuning, new sector selection, gate relaxation or planet
promotion was performed. Original evidence remains intact in the prior PRF folder.
A useful next test would examine the influential residual images and compare
event-window background/registration changes with matched off-event controls;
simply choosing the target-favoring omissions would be invalid.
