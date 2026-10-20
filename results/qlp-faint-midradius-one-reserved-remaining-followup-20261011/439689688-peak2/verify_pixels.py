from pathlib import Path
import json,zipfile,numpy as np
from exoplanet.pipeline import sha,save_json
case=Path(__file__).parent;raw=Path('results/tesscut-439689688-s81-20261011');nb=Path('results/neighbors-439689688-20261011');sp=Path('results/spoc-pixels-439689688-s81-20261011');g=Path('results/gaia-439689688-scene-20261011');read=lambda p:json.loads(p.read_text())
a=read(raw/'analysis.json');files=read(raw/'files.json');assert len(files)==1
for f in files:assert sha(Path(f['path']))==f['sha256']
assert sha(Path('data/pixels/tesscut-439689688-s81.zip'))==read(raw/'source.json')['sha256']
with zipfile.ZipFile('data/pixels/tesscut-439689688-s81.zip') as z:assert z.read(files[0]['member'])==Path(files[0]['path']).read_bytes()
assert a['fit_sha256']==sha(case/'frozen.json') and a['neighbor_sha256']==sha(nb/'neighbors.json')
assert a['script_sha256']==sha(raw/'analyze.py') and read(raw/'status.json')['exit_code']==0
assert len(a['event_numbers'])==8 and np.load(raw/'images.npz')['event_differences'].shape==(8,11,11)
c=read(raw/'coverage.json');assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(case/'frozen.json')
assert [r['event'] for r in c['events'] if r['inside_quality_zero']>=2 and r['outside_quality_zero']>=5]==a['event_numbers']
assert read(sp/'status.json')['exit_code']==1 and '404 Client Error' in (sp/'stderr.txt').read_text()
e=read(raw/'event-plots.json')
for p,h in e['plots'].items():assert sha(Path(p))==h
for n,h in e['inputs'].items():assert sha(raw/n)==h
assert len(read(nb/'neighbors.json'))==499
if (g/'results.json').exists():
 for p in g.glob('*-source.json'):
  table=p.name.removesuffix('-source.json');assert sha(Path(f'data/catalogs/gaia-439689688-scene-{table}-20261011.csv'))==read(p)['sha256']
 assert read(g/'results.json')['status']=='complete'
else:assert (g/'error.json').exists()
paths=[p for directory in [raw,nb,sp,g] for p in directory.rglob('*') if p.is_file()]
save_json(case/'source_review.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in paths},'status':'Raw evidence,8 maps/coverage,neighbors,processed404 and catalog provenance verified. Images reviewed separately; no calibrated host attribution.'})
print('Verified source artifacts.')
