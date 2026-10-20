# Code and research workflow

Use [README.md](README.md) for conclusions, [CHECKED-RESULTS.md](CHECKED-RESULTS.md) for evidence, and [GOAL.md](GOAL.md) for completion and resumption state. This document covers implementation, data access and verification.

## Repository layout

| Location | Contents |
|---|---|
| [src/exoplanet/](src/exoplanet/) | Reusable scientific algorithms, archive access and command entrypoints |
| [tests/](tests/) | Algorithm checks, including deterministic synthetic injections |
| [results/](results/) | Experiment plans, reports, measurements, provenance and verifiers |
| [dashboard/](dashboard/) | Local static evidence explorer and saved-result export script |
| `results/<run>/source/` | Historical source snapshots; retain as evidence |
| ignored `data/` | Raw downloads and caches; URLs, retrieval times and hashes belong in committed manifests |

Put reusable code in `src/exoplanet/` and experiment-specific choices in a fresh `results/<run>/`. Do not overwrite completed runs or move historical files: scripts, links and evidence hashes depend on them. Add a superseding report when interpretation changes.

## Entry points

Use Python 3.12 and `uv`. Run `uv sync --locked --python 3.12` to install the recorded environment; the locked `batman-package` dependency has no Python 3.14 wheel. Use `--help` before launching a command; historical result scripts are experiment records, not general-purpose launchers.

| Task | Module or command |
|---|---|
| Inventory and selection | [targeting.py](src/exoplanet/targeting.py): `uv run python -m exoplanet.targeting --help`; [archive.py](src/exoplanet/archive.py) handles MAST access |
| Single-sector search | [pipeline.py](src/exoplanet/pipeline.py): `uv run exoplanet-search --help` |
| Multi-sector search | [campaign.py](src/exoplanet/campaign.py), [qlp_campaign.py](src/exoplanet/qlp_campaign.py): run with `uv run python -m exoplanet.<module> --help` |
| Detection and diagnostics | [search.py](src/exoplanet/search.py), [vetting.py](src/exoplanet/vetting.py), [secondary.py](src/exoplanet/secondary.py), [null_controls.py](src/exoplanet/null_controls.py) |
| Prediction and follow-up | [followup.py](src/exoplanet/followup.py), [qlp_followup.py](src/exoplanet/qlp_followup.py); read the preflight below first |
| Difference images and source models | [pixel_vet.py](src/exoplanet/pixel_vet.py), [prf_fit.py](src/exoplanet/prf_fit.py) |
| Physical models and injections | [transit_model.py](src/exoplanet/transit_model.py), [physical_fit.py](src/exoplanet/physical_fit.py), [injection_grid.py](src/exoplanet/injection_grid.py), [pixel_injection.py](src/exoplanet/pixel_injection.py) |
| Radial velocities | [rv_search.py](src/exoplanet/rv_search.py), [rv_campaign.py](src/exoplanet/rv_campaign.py), [rv_activity.py](src/exoplanet/rv_activity.py) |

## Before opening additional observations

**The generic `exoplanet.followup` command writes a prediction and then automatically loads reserved sectors.** It does not establish that they were unseen or that the parent campaign passed its terminal audit. The caller must check both.

1. Inspect discovery records, previous follow-ups and raw caches. Establish which observations were already opened; file absence alone is insufficient.
2. Check actual live processes, campaign manifests and terminal verification. Do not open a running queue's reserved products while its audit requires them to remain absent. Document any coordinated exception.
3. Freeze training inputs, period, epoch, duration, timing uncertainty, success criteria and intended observations **before** access. Preserve the plan's hash and timestamp.
4. For image cutouts, verify the target and aperture lie on active science pixels before extracting photometry. A sky footprint and a successful TESScut response can include collateral columns. Preserve physical WCS coordinates and the instrument boundary convention; invalid detector pixels are not transit non-detections. See the [80387959 geometry audit](results/new-epochs-80387959-20261012/ASSESSMENT.md).
5. Report the unchanged prediction and all negative results. Label refitted clocks, alternate detrending, enlarged windows and event omissions as exploratory.

Omitted-year tests must exclude that year from training and disclose whether target or period selection originally used it. Retrospective cross-validation does not erase selection history. Different reductions of the same exposures share photons.

## Parallel ownership

- Give each worker a concrete question, exclusive output directory, explicit input paths and an allowlist of observations it may open.
- Give each target/cache path one downloading owner, or use isolated data roots. `pipeline.fetch` uses an unlocked deterministic `.partial` filename; concurrent downloads can race.
- Keep shared docs, aggregate ledgers, commits and pushes under one coordinator. Read-only review of completed evidence can run in parallel.
- Check live processes and resource use before launching compute. A stale progress file, missing handle or timeout does not justify a duplicate queue.
- Do not change shared scientific `src/` while a queue uses it: later batches import the live package. Use a separate checkout for development or wait and document the transition.

## Verification and integration

Run `uv run pytest` for scientific algorithm changes, with deterministic injection tests appropriate to the behavior. For individual experiments, preserve choices and inputs, independently reproduce the relevant arithmetic, and state what verification does **not** establish. A passing verifier is not astrophysical validation.

Before integration, reconcile target/pass/error counts, inspect relevant figures and check links. Keep catalog errors distinct from nonmatches. Preserve failed analyses, recovery records and raw provenance; never execute downloaded shell scripts. Inspect historical verifiers before rerunning them: cache-absence assertions may no longer apply.

Update current summaries without rewriting archived conclusions. An original `followup_priority` flag and a weak-seed local flag use different gates; neither establishes a planet. Keep source identity, planet plausibility and novelty separate. Follow [AGENTS.md](AGENTS.md) for privacy, synchronization and evidence retention. No external submissions or outreach without explicit user authorization.
