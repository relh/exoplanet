from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;fp=Path('results/source-check-469309982-20261011/frozen.json');b=json.loads(fp.read_text())['best'];groups=[[9,10],[36,37],[63,64]];paths=[Path(f'data/lightcurves/s{s:04d}-469309982.fits') for g in groups for s in g];assert all(q.exists() for q in paths)
save_json(p/'plan.json',dict(created_utc=now(),clock=b,frozen_sha256=sha(fp),raw_hashes={str(q):sha(q) for q in paths},groups=groups,windows=[1.5,2.5],script_sha256=sha(Path(__file__)),policy='Retrospective fixed original discovery clock; primary and exactly half-phase secondary only, same duration. All data already inspected. No secondary phase search or independent detection claim.'))
rows=[]
for window in [1.5,2.5]:
 for group in groups:
  t,y,e,meta=load_training(dict(tic=469309982,training_sectors=group),Path('data'),window=window)
  for name,shift in [('primary',0),('half_phase',.5)]:
   m=fixed_measure(t,y,e,b['period'],b['transit_time']+shift*b['period'],b['duration']);rows.append(dict(window=window,sectors=group,component=name,measurement=m));print(window,group,name,m['total'])
save_json(p/'results.json',dict(rows=rows))
