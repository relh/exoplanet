from pathlib import Path
import json,zipfile,numpy as np
from exoplanet.pipeline import sha,save_json
case=Path(__file__).parent;raw=Path('results/tesscut-435878345-s57-20261011');nb=Path('results/neighbors-435878345-20261011');sp=Path('results/spoc-pixels-435878345-s57-20261011');g=Path('results/gaia-435878345-scene-20261011');read=lambda p:json.loads(p.read_text())
a=read(raw/'analysis.json');files=read(raw/'files.json');assert len(files)==1
for f in files:assert sha(Path(f['path']))==f['sha256']
assert sha(Path('data/pixels/tesscut-435878345-s57.zip'))==read(raw/'source.json')['sha256']
with zipfile.ZipFile('data/pixels/tesscut-435878345-s57.zip') as z:assert z.read(files[0]['member'])==Path(files[0]['path']).read_bytes()
assert a['fit_sha256']==sha(case/'frozen.json') and a['neighbor_sha256']==sha(nb/'neighbors.json')
assert a['script_sha256']==sha(raw/'analyze.py') and read(raw/'status.json')['exit_code']==0
assert len(a['event_numbers'])==9 and np.load(raw/'images.npz')['event_differences'].shape==(9,11,11)
c=read(raw/'coverage.json');assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(case/'frozen.json')
assert [r['event'] for r in c['events'] if r['inside_quality_zero']>=2 and r['outside_quality_zero']>=5]==a['event_numbers']
assert read(sp/'status.json')['exit_code']==0
from astropy.io import fits
from exoplanet.pixel_vet import difference_events
loc=read(sp/'analysis/localization.json');pp=Path('data/pixels/435878345-s0057.fits')
assert sha(pp)==loc['source']['sha256'] and loc['frozen_sha256']==sha(case/'frozen.json')
with fits.open(pp) as h:
 assert h[0].header['TICID']==435878345 and h[0].header['SECTOR']==57
 assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
 d=h[1].data;ok=np.isfinite(d['TIME']);diff,err,ev,nums=difference_events(np.array(d['TIME'][ok],dtype=float),np.array(d['FLUX'][ok],dtype=float),np.array(d['FLUX_ERR'][ok],dtype=float),d['QUALITY'][ok],read(case/'frozen.json')['best'])
 saved=np.load(sp/'analysis/images.npz');assert nums==loc['event_numbers'] and len(nums)==9
 for arr,key in [(diff,'difference'),(err,'error'),(ev,'event_differences')]:assert np.allclose(arr,saved[key],equal_nan=True)
plots=read(sp/'analysis/event-plots.json')
for path,h in plots['plots'].items():assert sha(Path(path))==h
for name,h in plots['inputs'].items():assert sha(sp/'analysis'/name)==h
e=read(raw/'event-plots.json')
for p,h in e['plots'].items():assert sha(Path(p))==h
for n,h in e['inputs'].items():assert sha(raw/n)==h
assert len(read(nb/'neighbors.json'))==27
if (g/'results.json').exists():
 for p in g.glob('*-source.json'):
  table=p.name.removesuffix('-source.json');assert sha(Path(f'data/catalogs/gaia-435878345-scene-{table}-20261011.csv'))==read(p)['sha256']
 assert read(g/'results.json')['status']=='complete'
else:assert (g/'error.json').exists()
paths=[p for directory in [raw,nb,sp,g] for p in directory.rglob('*') if p.is_file()]
save_json(case/'source_review.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in paths},'status':'Raw evidence,9 raw and9 processed maps/coverage,neighbors,processed pixel and catalog provenance verified. Images reviewed separately; no calibrated host attribution.'})
print('Verified source artifacts.')
