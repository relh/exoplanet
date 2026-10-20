"""Export only reviewed evidence; never expose the repository root."""
from pathlib import Path
import json, hashlib, shutil
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dashboard/dist'
OUT.mkdir(exist_ok=True)
runs = ['strongest-80387959-shape-20261012', 'strongest-402358350-baselines-20261012']
a = json.loads((ROOT/'results'/runs[0]/'results.json').read_text())
b = json.loads((ROOT/'results'/runs[1]/'summary.json').read_text())
noise_a = json.loads((ROOT/'results/paper-vetting-80387959-20261012/results.json').read_text())
noise_b = json.loads((ROOT/'results/paper-vetting-402358350-20261012/results.json').read_text())
noise_sector = {r['sector']:r['full'] for r in noise_a['rows']}
noise_method = {(r['kind'],r['degree'],r['outer']):r for r in noise_b['summary']}
series = []
for row in a['rows']:
    c = next(c for c in row['cases'] if c['name'] == 'primary')
    series.append(dict(label=f"Sector {row['sector']}", depth=c['depths_ppm'][0], error=noise_sector[row['sector']]['adjusted_error_ppm'], original_error=c['errors_ppm'][0], group='QLP' if row['sector'] >= 90 else 'SPOC'))
methods = [dict(label=f"{m['kind']} · {['constant','linear','quadratic'][m['degree']]} · ±{m['outer']}D", depth=m['depth']['depth']*1e6, error=noise_method[(m['kind'],m['degree'],m['outer'])]['inflated_error_fixed_weights']*1e6, original_error=m['depth']['error']*1e6, group=m['kind']) for m in b['methods']]
(OUT/'data.json').write_text(json.dumps({'80387959':series, '402358350':methods},indent=2))
manifest = []
for i,run in enumerate(runs):
    for filename, dest in [('ASSESSMENT.md',f'report-{i}.txt'), ('diagnostic.png' if i==0 else 'event-shapes.png', f'evidence-{i}.png')]:
        src=ROOT/'results'/run/filename
        shutil.copyfile(src,OUT/dest)
        manifest.append({'source':str(src.relative_to(ROOT)),'export':dest,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
for run, name in [(runs[0],'results.json'),(runs[1],'summary.json')]:
    src=ROOT/'results'/run/name
    manifest.append({'source':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
for run, files in [
    ('refereed-vetting-20261012', [('ASSESSMENT.md','full-assessment.md')]),
    ('paper-vetting-80387959-20261012', [('ASSESSMENT.md','noise-80387959.txt'), ('noise-diagnostic.png','noise-80387959.png'), ('results.json',None)]),
    ('paper-vetting-402358350-20261012', [('ASSESSMENT.md','noise-402358350.txt'), ('noise-sensitivity.png','noise-402358350.png'), ('results.json',None)]),
    ('paper-host-vetting-20261012', [('ASSESSMENT.md','neighbor-assessment.txt'), ('required-eclipses.png','neighbor-eclipses.png')])]:
    for filename, dest in files:
        src=ROOT/'results'/run/filename
        if dest: shutil.copyfile(src,OUT/dest)
        manifest.append({'source':str(src.relative_to(ROOT)), 'export':dest, 'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(OUT/'provenance.json').write_text(json.dumps(manifest,indent=2))
