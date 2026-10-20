from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json');c=read(out/'synthetic.json')
assert p['script_sha256']==sha(out/'run.py') and p['fit_module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for n,h in p['inputs'].items():assert sha(Path(n))==h
assert r['plot_sha256']==sha(out/'comparison.png') and r['arrays_sha256']==sha(out/'residuals.npz')
assert len(c['controls'])==4
for t in c['controls']:
 if t['amplitude']==0:assert t['max_null_residual']<1e-9
 else:assert .95<t['recovered_fraction']<1.01
for row in r['rows']:
 for f in row['fits']:
  assert f['motion_rss']<=f['plane_rss'] and f['aperture_sums']['156001092']>0 and f['aperture_sums']['156001088']<0
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'results_sha256':sha(out/'results.json'),'synthetic_sha256':sha(out/'synthetic.json'),'status':'provenance and narrow controls passed, not astrophysical validation'})
print('Verified motion diagnostic and controls.')
