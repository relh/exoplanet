from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha, save_json
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
p=read(out/'plan.json');r=read(out/'results.json');s=read(out/'synthetic.json')
assert p['script_sha256']==sha(out/'run.py')
assert p['fit_module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for name,h in p['inputs'].items():assert sha(Path(name))==h
assert r['plot_sha256']==sha(out/'comparison.png') and r['arrays_sha256']==sha(out/'residuals.npz')
assert len(s['controls'])==4
for c in s['controls']:
 if c['amplitude']==0:assert c['max_null_residual']<1e-9
 else:assert .5<c['recovered_fraction']<1.5
z=np.load(out/'residuals.npz');a=read(Path('results/spoc-pixels-149919534-s75-20261011/analysis/localization.json'))
assert [row['event'] for row in r['rows']]==a['event_numbers']==[1,2]
for row in r['rows']:
 assert [f['radius'] for f in row['fits']]==p['radii']
 for f in row['fits']:
  assert f['motion_rss']<=f['plane_rss']+1e-10
  im=z[f"event{row['event']}_radius{f['radius']}"];y,x=np.indices(im.shape);tx,ty=a['header_target_xy']
  assert int((np.isfinite(im)&((x-tx)**2+(y-ty)**2>f['radius']**2)).sum())==f['fit_pixels']
  for tic,value in f['aperture_sums'].items():
   src=next(s for s in a['neighbors_by_distance'] if s['tic']==int(tic));mask=(x-src['x'])**2+(y-src['y'])**2<=1.5**2
   assert np.isclose(im[mask].sum(),value,rtol=0,atol=1e-12)
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'status':'Input hashes, synthetic controls, masks, nested fits and aperture arithmetic verified; not motion exclusion or host validation.'})
print('Motion provenance and arithmetic verified.')
