from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');r=read(out/'results.json')
assert plan['script_sha256']==sha(out/'run.py') and plan['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for name,h in plan['inputs'].items():assert sha(Path(name))==h
assert r['plot_sha256']==sha(out/'comparison.png') and r['arrays_sha256']==sha(out/'residuals.npz')
assert len(read(out/'synthetic.json')['checks'])==4
assert all(c['max_absolute_error']<1e-10 for c in read(out/'synthetic.json')['checks'])
assert len(r['rows'])==2
for row in r['rows']:
 assert [f['background_pixels'] for f in row['fits']]==[83,59]
 for f in row['fits']:
  sums={a['tic']:a['sum'] for a in f['aperture_sums']};assert sums[156001092]>0 and sums[156001093]>0 and sums[156001088]<0
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'results_sha256':sha(out/'results.json'),'synthetic_sha256':sha(out/'synthetic.json'),'status':'provenance, controls and recorded sign consistency passed; no astrophysical validation'})
print('Verified provenance and synthetic controls.')
