from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha, save_json
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
p=read(out/'plan.json');r=read(out/'results.json');s=read(out/'synthetic.json')
assert p['script_sha256']==sha(out/'run.py')
assert p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for name,h in p['inputs'].items():assert sha(Path(name))==h
assert r['plot_sha256']==sha(out/'comparison.png') and r['arrays_sha256']==sha(out/'residuals.npz')
assert len(s['checks'])==4 and all(c['max_absolute_error']<1e-10 for c in s['checks'])
z=np.load(out/'residuals.npz');a=read(Path('results/spoc-pixels-149919534-s75-20261011/analysis/localization.json'))
assert [row['event'] for row in r['rows']]==a['event_numbers']==[1,2]
for row in r['rows']:
 assert [f['radius'] for f in row['fits']]==p['radii']
 for f in row['fits']:
  im=z[f"event{row['event']}_radius{f['radius']}"];y,x=np.indices(im.shape);keep=np.isfinite(im)
  for src in p['sources']:keep &= (x-src['x'])**2+(y-src['y'])**2>f['radius']**2
  assert int(keep.sum())==f['background_pixels']
  for ap in f['aperture_sums']:
   src=next(s for s in a['neighbors_by_distance'] if s['tic']==ap['tic']);mask=(x-src['x'])**2+(y-src['y'])**2<=1.5**2
   assert int(mask.sum())==ap['pixels'] and np.isclose(im[mask].sum(),ap['sum'],rtol=0,atol=1e-12)
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'status':'Input hashes, exact-plane controls, masks and aperture arithmetic verified; not host validation.'})
print('Background provenance and arithmetic verified.')
