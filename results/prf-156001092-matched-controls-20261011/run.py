"""Reuse the frozen sensitivity grid and off-event schedule without optimization."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.ndimage import gaussian_filter
from astropy.io import fits
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pixel_vet import individual_difference_events
from exoplanet.pipeline import sha, save_json

out = Path(__file__).parent
read = lambda p: json.loads(p.read_text())
base = Path('results/prf-156001092-astrometry-20261011')
prior = Path('results/prf-156001092-sensitivity-20261011')
mp = Path('results/prf-156001092-20261011/models.json')
ap = Path('results/gaia-156001092-scene-20261011/astrometry-audit.json')
fp = Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/frozen.json')
cp = Path('results/prf-156001092-edge-20261011/broader-controls.json')
r = read(base / 'fits.json')
m = read(mp)['sectors'][0]
b = read(fp)['best']
a = next(x for x in read(ap)['rows'] if x['tic'] == 156001088)
ids = r['scene_ids']
positions = np.array(r['input_positions'])
registration = np.array(r['alignment'])
z = np.load(base / 'images.npz')
scene = z['scene']
shape = scene.shape
models = read(prior / 'results.json')['rows']
schedule = read(cp)['rows']
inputs = [base / 'fits.json', base / 'images.npz', prior / 'results.json', mp, ap, fp, cp, Path(m['pixel_path'])]
assert not (out / 'plan.json').exists()
save_json(out / 'plan.json', {
    'script_sha256': sha(Path(__file__)),
    'modules': {str(p): sha(p) for p in [Path('src/exoplanet/prf_fit.py'), Path('src/exoplanet/pixel_vet.py')]},
    'inputs': {str(p): sha(p) for p in inputs},
    'policy': 'Reuse all 36 archived sensitivity variants and all 36 archived off-event attempts; no outcome selection. Verify observed-event fits match their archived coefficients. Identify duplicate controls by exact inside/outside exposure masks. Compare each model with its own controls. No independent-sample or false-alarm interpretation; control cadence and baseline coverage vary.'
})
with fits.open(m['pixel_path']) as h:
    d = h[1].data
    t = np.asarray(d['TIME'], float)
    ok = np.isfinite(t)
    t = t[ok]
    flux = np.asarray(d['FLUX'][ok], float)
    err = np.asarray(d['FLUX_ERR'][ok], float)
    q = d['QUALITY'][ok]
maps, variances, numbers = individual_difference_events(t, flux, err, q, b)
phase = (t - b['transit_time'] + b['period'] / 2) % b['period'] - b['period'] / 2
valid = (q == 0) & (abs(phase) > b['duration'])
controls = []
unique = {}
for old in schedule:
    center = b['transit_time'] + (old['event'] + old['fraction']) * b['period']
    dt = abs(t - center)
    inside = valid & (dt < b['duration'] / 2)
    outside = valid & (dt > b['duration']) & (dt < 3 * b['duration'])
    ni, no = int(inside.sum()), int(outside.sum())
    assert (ni, no) == (old['inside'], old['outside'])
    row = {k: old[k] for k in ['event', 'fraction', 'status']}
    row.update(center_btjd=center, inside=ni, outside=no)
    if ni < 2 or no < 5:
        assert row['status'] == 'insufficient_coverage'
    else:
        assert row['status'] == 'measured'
        key = hashlib.sha256(inside.tobytes() + outside.tobytes()).hexdigest()
        row['window_id'] = key
        if key not in unique:
            im = np.nanmean(flux[outside], axis=0) - np.nanmean(flux[inside], axis=0)
            se = np.sqrt(np.nansum(err[outside] ** 2, axis=0) / no ** 2 + np.nansum(err[inside] ** 2, axis=0) / ni ** 2)
            unique[key] = (im, se)
    controls.append(row)
assert len(controls) == 36 and len(unique) == 14
prf = TESS_PRF(m['camera'], m['ccd'], 69, m['col'], m['row'], localdatadir='data/prf/start_s0004')
rows = []
max_reproduction_error = 0.
for old in models:
    pos = positions.copy()
    pos[ids.index('156001088')] = a['mappings'][old['mapping']]['propagated_xy']
    templates = []
    for p in pos:
        tpl = prf.locate(*(p + registration + [old['dx'], old['dy']]), shape)
        if old['width']:
            tpl = gaussian_filter(tpl, old['width'], mode='constant', cval=0.)
        templates.append(tpl)
    sf = fit_templates(scene, np.ones(shape), templates, nonnegative=True)
    gy, gx = np.gradient(sf['model'])
    def fit(im, se):
        f = fit_templates(im, se, templates + [gx, gy])
        return {'target_amplitude': float(f['coefficients'][ids.index('156001092')]),
                'neighbor090_amplitude': float(f['coefficients'][ids.index('156001090')]),
                'chi2': f['chi2'], 'dof': f['dof']}
    row = {k: old[k] for k in ['mapping', 'dx', 'dy', 'width']}
    row['events'] = []
    for n, im, v in zip(numbers, maps, variances):
        f = fit(im, np.sqrt(v))
        reference = next(e for e in old['events'] if e['event'] == n)
        for key in ['target_amplitude', 'neighbor090_amplitude', 'chi2']:
            delta = abs(f[key] - reference[key])
            max_reproduction_error = max(max_reproduction_error, delta)
            assert delta < 1e-8
        row['events'].append(dict(event=n, **f))
    row['controls'] = [dict(window_id=key, **fit(im, se)) for key, (im, se) in unique.items()]
    rows.append(row)
save_json(out / 'results.json', {'schedule': controls, 'rows': rows,
    'max_observed_reproduction_error': max_reproduction_error,
    'limits': '14 distinct exposure-mask windows, not 21 independent controls. Selected schedule from one sector, uneven coverage, correlated pixels, and conditional models: no calibrated false-alarm rate, depth or host probability.'})
summary = {'results_sha256': sha(out / 'results.json'), 'models': len(rows), 'attempted_windows': len(controls),
           'measured_rows': sum(c['status'] == 'measured' for c in controls), 'unique_measured_windows': len(unique),
           'insufficient_rows': sum(c['status'] != 'measured' for c in controls), 'events': []}
for n in numbers:
    report = {'event': n}
    for source in ['target_amplitude', 'neighbor090_amplitude']:
        gaps, absolute_gaps, all_controls = [], [], []
        for row in rows:
            event = next(e[source] for e in row['events'] if e['event'] == n)
            cs = [c[source] for c in row['controls']]
            gaps.append(event - max(cs))
            absolute_gaps.append(event - max(abs(x) for x in cs))
            all_controls.extend(cs)
        report[source] = {'control_range_all_models': [min(all_controls), max(all_controls)],
                          'event_minus_same_model_max_control_range': [min(gaps), max(gaps)],
                          'models_above_max_control': sum(g > 0 for g in gaps),
                          'event_minus_same_model_max_absolute_control_range': [min(absolute_gaps), max(absolute_gaps)],
                          'models_above_absolute_control': sum(g > 0 for g in absolute_gaps)}
    summary['events'].append(report)
save_json(out / 'summary.json', summary)
print(json.dumps(summary, indent=2))
