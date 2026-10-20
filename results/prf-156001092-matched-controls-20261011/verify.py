from pathlib import Path
import json
import itertools
import numpy as np
from exoplanet.pipeline import sha, save_json
out = Path(__file__).parent
read = lambda p: json.loads(p.read_text())
p, r, s, pm = [read(out / name) for name in ['plan.json', 'results.json', 'summary.json', 'plot-manifest.json']]
assert p['script_sha256'] == sha(out / 'run.py')
for group in ['inputs', 'modules']:
    for path, digest in p[group].items():
        assert sha(Path(path)) == digest, path
assert pm['script_sha256'] == sha(out / 'plot.py')
assert pm['plot_sha256'] == sha(out / 'controls.png')
assert s['results_sha256'] == pm['results_sha256'] == sha(out / 'results.json')
rows = r['rows']
assert len(rows) == 36
assert {(x['mapping'], x['dx'], x['dy'], x['width']) for x in rows} == set(itertools.product(range(2), [-.1, 0., .1], [-.1, 0., .1], [0., .4]))
assert len(r['schedule']) == 36
measured = [x for x in r['schedule'] if x['status'] == 'measured']
keys = {x['window_id'] for x in measured}
assert len(measured) == 21 and len(keys) == 14
assert all(x['inside'] < 2 or x['outside'] < 5 for x in r['schedule'] if x['status'] != 'measured')
assert r['max_observed_reproduction_error'] < 1e-8
for row in rows:
    assert len(row['controls']) == 14 and {c['window_id'] for c in row['controls']} == keys
    assert {e['event'] for e in row['events']} == {2, 3}
    for c in row['controls'] + row['events']:
        assert all(np.isfinite(c[k]) for k in ['target_amplitude', 'neighbor090_amplitude', 'chi2'])
        assert c['dof'] == 103
for report in s['events']:
    for key in ['target_amplitude', 'neighbor090_amplitude']:
        gaps, agaps, values = [], [], []
        for row in rows:
            event = next(e[key] for e in row['events'] if e['event'] == report['event'])
            cs = [c[key] for c in row['controls']]
            values.extend(cs)
            gaps.append(event - max(cs))
            agaps.append(event - max(abs(v) for v in cs))
        rs = report[key]
        assert rs['control_range_all_models'] == [min(values), max(values)]
        assert rs['event_minus_same_model_max_control_range'] == [min(gaps), max(gaps)]
        assert rs['models_above_max_control'] == sum(g > 0 for g in gaps)
        assert rs['event_minus_same_model_max_absolute_control_range'] == [min(agaps), max(agaps)]
        assert rs['models_above_absolute_control'] == sum(g > 0 for g in agaps)
save_json(out / 'verification.json', {'script_sha256': sha(Path(__file__)), 'results_sha256': sha(out / 'results.json'), 'summary_sha256': sha(out / 'summary.json'), 'status': '36 models, 504 unique-window fits, 72 reproduced event fits, missing/duplicate windows and provenance verified. Not physical calibration.'})
print('Verified 504 control fits, 72 reproduced event fits and all source hashes.')
