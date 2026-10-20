"""Preserve baseline failures and freeze shorter-window recovery plans from time coverage."""
from pathlib import Path
import json
import numpy as np
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;rows=[];recovery=[]
for summary in json.loads((out/'results.json').read_text()):
 if summary['status']!='error':continue
 p=out/'targets'/f"{summary['tic']}.json";r=json.loads(p.read_text());t=r['target']
 assert r['error']=='ValueError: Training baseline exceeds configured dense-search limit' and r['clean_baseline_days']>120
 raw=[]
 for ev in r['data']:
  path=Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits");assert sha(path)==ev['source']['sha256'];raw.append({'path':str(path),'sha256':sha(path)})
 options=[];chosen=None
 for n in [3,2]:
  target=dict(t,training_sectors=t['training_sectors'][-n:])
  try:
   x,y,e,ev=load_qlp(target,Path('data'));baseline=float(np.ptp(x));options.append({'training_sectors':target['training_sectors'],'clean_baseline_days':baseline,'n_clean':len(x)})
  except Exception as exc:options.append({'training_sectors':target['training_sectors'],'error':repr(exc)});continue
  if baseline<=120:
   chosen=target;break
 assert chosen is not None and not set(chosen['training_sectors'])&set(t['heldout_sectors'])
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['heldout_sectors'])
 rows.append({'tic':r['tic'],'original_path':str(p),'original_sha256':sha(p),'original_baseline_days':r['clean_baseline_days'],'raw':raw,'options':options,'status':'original_baseline_unusable','recovery_training':chosen['training_sectors']})
 recovery.append(chosen)
assert len(rows)==5
save_json(out/'failure_check.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'policy':'Original failures retained, not nondetections. Recovery chooses longest latest suffix of originally opened training sectors fitting120days, from time coverage only; no reserved sectors consumed. Recovery searches have not yet run.'})
dest=Path('results/qlp-faint-midradius-recovery-20261011');dest.mkdir(exist_ok=True)
assert not (dest/'selected.json').exists()
save_json(dest/'selected.json',recovery)
save_json(dest/'selection.json',{'utc':now(),'selected_sha256':sha(dest/'selected.json'),'failure_check_sha256':sha(out/'failure_check.json'),'n':len(recovery),'policy':'Separate reduced-window discovery attempts, not repair of original four-sector searches. Original ephemerides absent because baseline guard failed before search. Reserved sector lists unchanged.'})
print([(r['tic'],r['original_baseline_days'],r['recovery_training']) for r in rows])
