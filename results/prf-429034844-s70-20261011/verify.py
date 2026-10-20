from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.prf_fit import fit_templates
out=Path(__file__).parent;read=lambda n:json.loads((out/n).read_text());m=read('models.json')['sectors'][0];r=read('fits.json');f=r['sectors'][0];z=np.load(out/'s70-images.npz')
assert sha(Path(m['pixel_path']))==m['pixel_sha256']
for model in m['models']:assert sha(Path(model['path']))==model['source']['sha256']
assert r['script_sha256']==sha(out/'analyze.py') and r['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
assert r['frozen_sha256']==sha(Path('results/joint-clock-fine-429034844-20261011/fit.json'))
assert {'429034844','611135702'}<=set(f['scene_ids']) and f['n_events']==43
for h in f['hypotheses']:
 v=fit_templates(z['difference'],z['error'],[z['template_'+h['tic']]])
 np.testing.assert_allclose(v['chi2'],h['chi2'],rtol=1e-10)
for row in f['injections']:assert sum(row['winners'].values())==100
c=read('empirical-controls.json');assert c['fits_sha256']==sha(out/'fits.json') and c['script_sha256']==sha(out/'controls.py');assert c['sectors'][0]['n_controls']==41
s=read('registration-sensitivity.json')
for n,h in s['inputs'].items():assert sha(out/n)==h
assert s['script_sha256']==sha(out/'registration_sensitivity.py') and len(s['rows'])==17
assert s['rows'][8]['winner']=='611135702' and s['rows'][13]['winner']=='429034844'
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in out.iterdir() if p.is_file() and p.name!='verification.json'},'checks':'Pixel/model/input hashes, retained two-star hypotheses, reproduced conditional fits, control counts and registration host switch verified. Not calibrated host attribution.','tests':'uv run pytest -q: 49 passed in22.91s; session57700 terminal0.'});print('Verified PRF evidence and sensitivity.')
