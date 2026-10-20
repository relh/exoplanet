"""Export the reviewed exploratory run, without exposing raw caches or environments."""
from pathlib import Path
import hashlib
import json
import math
import shutil
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/triceratops-20261013'
REVIEW = ROOT / 'results/triceratops-review-20261013'
OUT = ROOT / 'dashboard/dist'


def percent(value):
    return 'Unavailable' if value is None else f'{100*value:.1f}%'


def render_section(summary, records):
    rows = []
    sensitivity = []
    for target in summary['targets']:
        metric = target['metrics']
        cells = ''.join(f"<td>{percent(metric[key]['value_1m'])}</td>"
                        for key in ['target_planet', 'FPP', 'NFPP'])
        rows.append(f"<tr><th scope='row'>TIC {target['tic']}<small>Sector {target['input']['sector']}</small></th>{cells}</tr>")
        bounds = metric['target_planet']['range_100k']
        if bounds is None:
            sensitivity.append(f"<li>TIC {target['tic']}: repeated-run comparison unavailable; see the retained run errors.</li>")
            continue
        lo, hi = bounds
        sensitivity.append(f"<li><strong>TIC {target['tic']}:</strong> target-planet weights of {percent(lo)}–{percent(hi)} across three 100,000-draw seeds.</li>")
    failed = [str(t['tic']) for t in summary['targets'] if t.get('threshold_comparison', {}).get('original_numerical_validation_thresholds_met') is False]
    threshold_note = ('Neither candidate meets the published numerical validation thresholds: FPP below 1.5% and NFPP below 0.1%.' if len(failed) == 2 else 'The published numerical validation thresholds are FPP below 1.5% and NFPP below 0.1%. Meeting them would still require adequate model and observational constraints.')
    known = [r for r in records if r['tic'] == 137151335 and r.get('status') == 'completed' and not r.get('degenerate', True)]
    known_note = (f"The same restricted setup gives known planet Kepler-93 b a target-planet weight of {percent(known[0]['target_planet'])}. Its published validation used additional evidence that is absent here. A higher weight for our candidates does not establish stronger evidence than for this known planet." if known else 'The known-planet control did not return a usable comparison; see the retained run records.')
    flat = [r for r in records if r['tic'] == 80387959 and r.get('control') == 'flat' and r.get('status') == 'completed' and not r.get('degenerate', True)]
    if flat:
        known_note += f" With every TIC 80387959 flux sample set to unity, removing both the dip and scatter, the constant-flux control receives {percent(flat[0]['target_planet'])} target-planet weight and {percent(flat[0]['any_host_planet'])} for planets across all modeled hosts. The model normalizes its allowed explanations even without a transit."
    control_rows = []
    for r in records:
        if r.get('status') != 'completed':
            continue
        if r['tic'] == 137151335:
            label = 'Kepler-93 b control'
        elif r['control'] != 'none':
            label = f"TIC {r['tic']} · {r['control']} flux"
        elif r['noise'] != 1:
            label = f"TIC {r['tic']} · {r['noise']:g}× noise"
        else:
            continue
        weight = 'Degenerate calculation' if r.get('degenerate', True) else percent(r.get('target_planet'))
        control_rows.append(f"<tr><td>{label}</td><td>{weight}</td><td>{r['draws']:,}</td></tr>")
    controls = '<div class="table-scroll"><table><thead><tr><th scope="col">Diagnostic input</th><th scope="col">Target-planet weight</th><th scope="col">Draws</th></tr></thead><tbody>' + ''.join(control_rows) + '</tbody></table></div>'
    return """<!-- TRICERATOPS:START -->
<section class="article probability-section" id="triceratops" aria-labelledby="triceratops-title">
<div class="eyebrow">Exploratory analysis / 13 October 2026</div>
<h2 id="triceratops-title">TRICERATOPS model comparison</h2>
<p>TRICERATOPS compares planet transits with stellar eclipses and blended sources. The figures below are <strong>conditional weights within that model, not calibrated probabilities that these signals are planets.</strong> This calculation uses one previously inspected sector per candidate, rather than all available observations.</p>
<div class="table-scroll"><table><caption>One million Monte Carlo draws per scenario; one seed per candidate</caption><thead><tr><th scope="col">Candidate</th><th scope="col">Target planet<br>(1 − FPP)</th><th scope="col">Other scenarios<br>(FPP)</th><th scope="col">Nearby source<br>(NFPP)</th></tr></thead><tbody>""" + ''.join(rows) + """</tbody></table></div>
<p class="small">The target-planet and other-scenario columns sum to 100%. Nearby-source weight is part of FPP and includes planets around neighboring stars as well as stellar eclipses. It is not an additional, independent probability.</p>
<p><strong>""" + threshold_note + """</strong></p>
<p><strong>Numerical convergence is not established.</strong> The million-draw calculation has not been repeated with independent seeds. Lower-draw repeats measure sampling variation, but do not account for uncertain stellar properties, contamination, timing, or correlated noise.</p>
<p>Instrumental artifacts and general stellar variability are absent from the scenario comparison. The calculations also do not incorporate our earlier source-localization failures or timing concerns as likelihood terms. Neither candidate is validated by these results.</p>
<details><summary>Numerical repeatability, controls, and noise sensitivity</summary>
<p>""" + known_note + """</p>
<ul>""" + ''.join(sensitivity) + """</ul>
<p>The model uses the original SAP apertures, ten-minute sampling, fixed ephemerides, and a Gaussian approximation to the stellar image. Exact catalog duplicates were removed before the adopted runs. Some neighboring stars are excluded by the assumed flux budget; those exclusions have not been verified by resolved observations. Missing stellar parameters are estimated from photometry.</p>
<img src="triceratops-convergence.png" alt="Conditional target-planet weights by Monte Carlo draw count for the two candidate signals"/>
""" + controls + """
<p>The previously identified neighboring source TIC 1918682563 is included in the TIC 402358350 model. Its low relative weight does not exclude an eclipse: the earlier brightness audit and this model both allow it to supply the observed decrement.</p>
<p>A known-planet control, constant and inverted light curves, and increased-noise calculations test the behavior of this setup. Their full results are retained in the assessment and downloadable run records. These checks do not calibrate the probabilities for a population of unknown signals.</p></details>
<div class="downloads"><a href="triceratops-assessment.txt">Complete TRICERATOPS assessment ↗</a><a href="triceratops-review.txt">Independent numerical review ↗</a><a href="triceratops-results.zip" download>Scenario tables and run records ↓</a><a href="triceratops-provenance.json">Source hashes ↗</a></div>
<p class="small">Method: <a href="https://doi.org/10.3847/1538-3881/abc6af">Giacalone et al. (2021)</a>; <a href="https://github.com/stevengiacalone/triceratops/releases/tag/v1.1.0">TRICERATOPS v1.1.0</a>, <a href="https://ascl.net/2002.004">software citation</a>.</p>
</section>
<!-- TRICERATOPS:END -->"""


def export():
    # Publish only after the bounded experiment has a terminal summary.
    assert (RUN / 'ASSESSMENT.md').exists(), 'Wait for the completed assessment.'
    summary = json.loads((RUN / 'summary.json').read_text())
    assert summary['status'] == 'complete', 'Wait for all planned calculations to complete.'
    review = json.loads((REVIEW / 'output-verification.json').read_text())
    assert review['completed_runs'] == summary['expected_adopted_runs'] == 17, 'Wait for the complete independent review.'
    adopted = set(summary['adopted_run_files'])
    records = []
    for path in sorted(RUN.glob('*-N*.json')):
        record = json.loads(path.read_text())
        if 'draws' in record:
            record['source_file'] = path.name
            record['adopted'] = path.name in adopted
            records.append(record)
    assert records, 'No run records found.'
    manifest = []
    for source, name in [(RUN / 'ASSESSMENT.md', 'triceratops-assessment.txt'),
                         (REVIEW / 'ASSESSMENT.md', 'triceratops-review.txt')]:
        shutil.copyfile(source, OUT / name)
        manifest.append({'source': str(source.relative_to(ROOT)), 'export': name,
                         'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    files = sorted(set(RUN.rglob('*.json')) | set(RUN.rglob('*-scenarios.csv')) |
                   {RUN / 'ASSESSMENT.md', RUN / 'environment.txt'})
    with zipfile.ZipFile(OUT / 'triceratops-results.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            member = str(path.relative_to(RUN))
            archive.write(path, member)
            manifest.append({'source': str(path.relative_to(ROOT)), 'archive_member': member,
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT / 'triceratops-runs.json').write_text(json.dumps(records, indent=2) + '\n')
    (OUT / 'triceratops-provenance.json').write_text(json.dumps(manifest, indent=2) + '\n')

    # Show numerical repeatability separately from model/input uncertainty.
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True, layout='constrained')
    weights = [100*r['target_planet'] for r in records if r['adopted'] and not r.get('degenerate', True)]
    lower = max(0, 5*math.floor((min(weights)-.5)/5))
    upper = min(100, 5*math.ceil((max(weights)+.5)/5))
    for ax, tic in zip(axes, [80387959, 402358350]):
        rows = [r for r in records if r['adopted'] and r['tic'] == tic and r.get('status') == 'completed'
                and not r.get('degenerate', True) and r.get('control') == 'none'
                and r.get('noise') == 1 and r.get('aperture', 'nominal') == 'nominal']
        for r in rows:
            ax.scatter(r['draws'], 100*r['target_planet'], s=35, color='#18785f', alpha=.8)
        ax.set(xscale='log', ylim=(lower, upper), title=f'TIC {tic}', xlabel='Monte Carlo draws per scenario')
        ax.grid(alpha=.2)
    axes[0].set_ylabel('Conditional target-planet weight (%)')
    fig.suptitle('TRICERATOPS numerical repeatability · expanded scale', fontsize=13)
    fig.savefig(OUT / 'triceratops-convergence.png', dpi=160)
    plt.close(fig)
    page = OUT / 'index.html'
    html = page.read_text()
    section = render_section(summary, records)
    if '<!-- TRICERATOPS:START -->' in html:
        before, rest = html.split('<!-- TRICERATOPS:START -->', 1)
        _, after = rest.split('<!-- TRICERATOPS:END -->', 1)
        html = before + section + after
    else:
        html = html.replace('<section id="explore">', section + '\n<section id="explore">')
    html = html.replace('TESS archival photometry / 12 October 2026', 'TESS archival photometry / 13 October 2026')
    html = html.replace('Assessment dated 12 October 2026.', 'Assessment dated 13 October 2026.')
    html = html.replace('Complete technical assessment ↓', 'Photometric vetting report ↓')
    if 'href="#triceratops"' not in html:
        html = html.replace('<a href="#vetting">Vetting</a>', '<a href="#triceratops">Model results</a>')
    html = html.replace('No calibrated probability is available. Source identity and aperture contamination remain insufficiently constrained.', 'TRICERATOPS supplies conditional scenario weights, with convergence and model limitations. No calibrated planet probability is established; source identity and contamination remain unresolved.')
    page.write_text(html)
    print(f'Exported {len(records)} run records and {len(files)} evidence files.')


if __name__ == '__main__':
    export()
