from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;fp=Path('results/expanded-402358350-20261011/frozen-for81.json');b=json.loads(fp.read_text())['rows'][0]['best'];groups=[[81]];paths=[Path(f'data/lightcurves/s{s:04d}-402358350.fits') for g in groups for s in g];assert all(q.exists() for q in paths)
assert not (p/'plan.json').exists()
save_json(p/'plan.json',dict(created_utc=now(),clock=b,frozen_sha256=sha(fp),raw_hashes={str(q):sha(q) for q in paths},groups=groups,windows=[1.5,2.5],script_sha256=sha(Path(__file__)),policy='Retrospective fixed expanded40/41/54 primary clock; primary and exactly half-phase secondary only, same duration. All data already inspected. No secondary phase search or independent detection claim.'))
rows=[]
for window in [1.5,2.5]:
 for group in groups:
  t,y,e,meta=load_training(dict(tic=402358350,training_sectors=group),Path('data'),window=window)
  for name,shift in [('primary',0),('half_phase',.5)]:
   m=fixed_measure(t,y,e,b['period'],b['transit_time']+shift*b['period'],b['duration']);rows.append(dict(window=window,sectors=group,component=name,measurement=m));print(window,group,name,m['total'])
save_json(p/'results.json',dict(plan_sha256=sha(p/'plan.json'),rows=rows))
