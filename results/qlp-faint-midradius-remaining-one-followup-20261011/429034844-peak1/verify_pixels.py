from pathlib import Path
import json,zipfile,numpy as np
from exoplanet.pipeline import sha,save_json
case=Path(__file__).parent;raw=Path('results/tesscut-429034844-s70-20261011');nb=Path('results/neighbors-429034844-20261011');sp=Path('results/spoc-pixels-429034844-s70-20261011');g=Path('results/gaia-429034844-scene-20261011');read=lambda p:json.loads(p.read_text())
a=read(raw/'analysis.json');files=read(raw/'files.json');assert len(files)==1
for f in files:assert sha(Path(f['path']))==f['sha256']
assert sha(Path('data/pixels/tesscut-429034844-s70.zip'))==read(raw/'source.json')['sha256']
with zipfile.ZipFile('data/pixels/tesscut-429034844-s70.zip') as z:assert z.read(files[0]['member'])==Path(files[0]['path']).read_bytes()
assert a['fit_sha256']==sha(case/'frozen.json') and a['neighbor_sha256']==sha(nb/'neighbors.json')
assert a['script_sha256']==sha(raw/'analyze.py') and read(raw/'status.json')['exit_code']==0
assert len(a['event_numbers'])==16 and np.load(raw/'images.npz')['event_differences'].shape==(16,11,11)
c=read(raw/'coverage.json');assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(case/'frozen.json')
assert [r['event'] for r in c['events'] if r['inside_quality_zero']>=2 and r['outside_quality_zero']>=5]==a['event_numbers']
assert read(sp/'status.json')['exit_code']==0
sa=read(sp/'analysis/localization.json');sc=read(sp/'coverage.json')
assert sha(Path('data/pixels/429034844-s0070.fits'))==sa['source']['sha256']==sc['raw_sha256']
assert sa['frozen_sha256']==sha(case/'frozen.json')==sc['frozen_sha256']
assert [r['event'] for r in sc['events'] if r['inside_quality_zero']>=2 and r['outside_quality_zero']>=5]==sa['event_numbers']
assert len(sa['event_numbers'])==14 and np.load(sp/'analysis/images.npz')['event_differences'].shape[0]==14
se=read(sp/'analysis/event-plots.json')
for p,h in se['plots'].items():assert sha(Path(p))==h
for n,h in se['inputs'].items():assert sha(sp/'analysis'/n)==h
e=read(raw/'event-plots.json')
for p,h in e['plots'].items():assert sha(Path(p))==h
for n,h in e['inputs'].items():assert sha(raw/n)==h
assert len(read(nb/'neighbors.json'))==20
if (g/'results.json').exists():
 for p in g.glob('*-source.json'):
  table=p.name.removesuffix('-source.json');assert sha(Path(f'data/catalogs/gaia-429034844-scene-{table}-20261011.csv'))==read(p)['sha256']
 assert read(g/'results.json')['status']=='complete'
else:assert (g/'error.json').exists()
paths=[p for directory in [raw,nb,sp,g] for p in directory.rglob('*') if p.is_file()]
save_json(case/'source_review.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in paths},'status':'Raw/processed evidence,16/14 maps and coverage,neighbors and catalog provenance verified. Images reviewed separately; no calibrated host attribution.'})
print('Verified source artifacts.')
