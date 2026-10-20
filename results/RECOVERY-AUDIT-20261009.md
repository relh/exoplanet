# Recovery and noise audit, 2026-10-09

No likely new candidate is claimed. Searches of ranks 1,001–2,000 and
2,001–3,000 are still running; consult their manifests for current counts.

## Real-data injection grid

We selected eight completed batch-two targets with the lowest median point-to-point
scatter floor, then injected 96 box transits **before detrending** into their
actual training photometry. The grid spans 1.37, 4.73 and 13.13 days, durations
0.04/0.12 days, depths 250/750 ppm, and one phase per period. Exact exposure/box
overlap uses the median cadence. All discovery, alternate-window and vetting
steps were run. Existing variability was retained; no reserved sectors were used.

**55/96 injections appeared among the top three screened peaks; 33/96 passed the
full screen.** All runs completed without errors. No credited recovery coincided
with an already significant baseline peak at the injected period.

| Period (days) | Depth (ppm) | Probes | Top-three recovery | Full-screen recovery |
| --- | --- | --- | --- | --- |
| 1.37 | 250 | 16 | 8 | 6 |
| 1.37 | 750 | 16 | 12 | 5 |
| 4.73 | 250 | 16 | 8 | 6 |
| 4.73 | 750 | 16 | 10 | 8 |
| 13.13 | 250 | 16 | 7 | 2 |
| 13.13 | 750 | 16 | 10 | 6 |

Four stars with baseline maximum BLS S/N below 8 recovered 45/48 injected periods
and retained 33/48 through the full screen. The other four, despite their small
point-to-point errors, have strong pre-existing features and recovered only 10/48
periods, with none passing all cuts. This is evidence that the pipeline can miss
planets amid existing variability/systematics, and that its conservative cuts
reject some real injections. It is not an occurrence-rate completeness estimate:
the sample, phases, shapes and depths are highly restricted.

The earlier 38/40 recovery result used a different sample, a single period/duration,
deeper injections and only period recovery; it cannot be compared directly with
this full-screen rate. `injection-grid-20261009/` contains exact source snapshots,
per-injection results, input hashes, aggregate counts and a provisional variability
snapshot. Tests verify exact integration conserves transit area and wraps phases.

## New signals inspected during the running batches

TIC 302366928 has a 3.2353-day, 197-ppm discovery peak with formal S/N 8.08. Its
measured depth nearly doubles with the longer detrending window. QLP fixed-phase
S/N values are 2.96, 0.14 and 1.28 in Sectors 9/10/11. The Sector 10 pixel
difference has adjacent positive/negative residuals rather than a clean positive
source. The apparent difference moment is not a reliable physical localization.

For this star, 48 controls permuted flux/error blocks within contiguous training
segments. Block lengths were 0.5, 1 and 2 days, with 16 realizations each. Each
control repeated the full BLS period search; 1/16, 2/16 and 1/16 respectively
produced a maximum power at least as large as observed. These conditional
controls preserve short correlations but disrupt longer ones, introduce seams
and can retain pieces of astrophysical signals. **4/48 is not a calibrated
survey-wide false-alarm probability**, but further weakens this marginal peak.
The permutation test checks conservation of samples/pairs, gap separation, local
correlations and reproducibility. Evidence is in `null-controls-302366928-20261009/`.

TIC 312812096 has a 12.7975-day formal S/N 8.60 peak and only three supported
training events. QLP Sectors 19/20 give fixed-phase S/N 0.63/3.12, and Sector 19
pixels again show adjacent positive/negative residuals. Its broad dip and strong
detrending sensitivity are additional concerns. Neither star is promoted; no
later validation sectors were opened. These findings do not establish absence
of planets or uniquely identify the instrumental cause.

## Next work

Finish and vet the active batches. Use the injection failures to improve residual
searches and variability handling, preserving injected transits. Inspect near
passes rather than equating a heuristic veto with absence of a planet. Broaden
real-data controls before assigning calibrated significance to any surviving
lead. Twenty-one tests pass. The private repository contains the audit evidence;
no external submissions or messages have been made.
