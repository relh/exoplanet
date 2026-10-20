# Local evidence explorer

A static assessment of TIC 80387959 and TIC 402358350 using saved observations and reports from 13 October 2026. It includes candidate comparisons, measured dips, uncertainty bars, source-contamination limits, model comparisons and follow-up plans. Neither signal is validated.

## Build and preview

Run from the repository root:

```sh
python3 dashboard/build.py
uv run python dashboard/export_transits.py
uv run python dashboard/export_triceratops.py
uv run python dashboard/export_followup.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dashboard/dist
```

Open <http://127.0.0.1:8765/>. The exporters read saved artifacts; they do not download observations or run new scientific analyses. Serve only `dashboard/dist`.

Hosting addresses and machine-specific service instructions are omitted. The [release audit](../docs/RELEASE-AUDIT.md) records the completed publication cleanup. Publish the exported dashboard only with the credited data and its scientific limitations.

## Files and provenance

| File | Role |
|---|---|
| `dist/index.html` | Page structure, assessment text and exported sections |
| `dist/app.js`, `dist/transit.js`, `dist/styles.css` | Interactive charts and presentation |
| `build.py` | Exports reviewed photometric reports, figures and depth/noise summaries |
| `export_transits.py` | Exports 4,045 saved light-curve observations and their clocks |
| `export_triceratops.py` | Exports the 17 completed model runs, controls and review |
| `export_followup.py` | Exports resolved-neighbor checks, timing windows, archive screens and observing plans |
| `dist/*provenance.json` | Source paths, export names and SHA-256 hashes |

Text exports preserve original report links, which may refer to repository files outside the dashboard. Downloadable archives include superseded runs and limitations. Rebuilding an export does not make those contents suitable for public release.

## Interpretation

Observed light curves use saved baseline-subtracted samples within two durations of the retained events, without additional outlier clipping. The browser shows 32 equal-width mean bins. Combined sectors are descriptive because cadence and depth differ. Adjusted depth errors are conditional estimates, not calibrated confidence intervals; previous values remain in `data.json` as `original_error`.

The animated crossing illustrates a central transit of a uniform, undiluted disk. Its radius ratio is the square root of a reference depth; the host, path and surface texture are unmeasured. The locator ring exaggerates visibility. No planet size or validation follows.

TRICERATOPS percentages are conditional scenario weights from one sector per candidate. They omit general instrumental artifacts and stellar variability; numerical convergence is unestablished. The follow-up packet retains 64 nominal events and ten neighbor rows. Its timing envelopes are not calibrated confidence intervals, and no telescope time is booked. The operator inquiry remains unsent.

## Verification

```sh
uv run python dashboard/verify_transits.py
```

This reconstructs all 4,045 exported observations and checks their source hashes, clocks and event counts. It checks presentation fidelity, not planetary origin.

Earlier integration checks covered desktop/mobile layouts, candidate selectors, filters, local links, model values and provenance. [followup-integration-verification.json](followup-integration-verification.json) records their scope. Those are historical results; rerun relevant checks after presentation changes.
