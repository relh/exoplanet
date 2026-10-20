from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');r=read(out/'results.json')
assert plan['script_sha256']==sha(out/'run.py')
for p,h in plan['inputs'].items():assert sha(Path(p))==h
assert [x['ratio'] for x in r['rows']]==plan['ratios'] and len(r['controls'])==5
for row,control in zip(r['rows'],r['controls']):
 assert row['ratio']==control['ratio'];np.testing.assert_allclose(control['recovered'],control['truth'],atol=1e-5)
 assert row['winner']==min(row['host_chi2'],key=row['host_chi2'].get)=='611135702'
base=Path('results/prf-429034844-s70-20261011');old=read(base/'fits.json')['sectors'][0];s=read(base/'registration-sensitivity.json')['rows'][8]
assert old['scene_ids']==['429034844','429034846','611135702'] and abs(s['scene_coefficients'][0])<1e-6
assert s['scene_coefficients'][2]>2000
new=r['rows'][2];before=old['hypotheses'][0]['chi2']-old['hypotheses'][1]['chi2'];after=new['host_chi2']['429034844']-new['host_chi2']['611135702'];assert 0<after<before
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in [out/'run.py',out/'plan.json',out/'results.json',out/'ASSESSMENT.md']},'prior_delta_chi2':before,'ratio_constrained_delta_chi2':after,'status':'Input hashes, pre-recorded ratio grid, five numerical recovery controls and original free-scene degeneracy checked. No calibrated host probability.'});print(before,after)
