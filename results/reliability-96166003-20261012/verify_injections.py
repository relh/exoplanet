import json,numpy as np
from pathlib import Path
from exoplanet.pipeline import read_curve,sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import refine_training
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());plan=json.loads((O/'injection-plan.json').read_text());r=json.loads((O/'injections.json').read_text());assert r['plan_sha256']==sha(O/'injection-plan.json');assert plan['script_sha256']==sha(O/'injections.py');b=plan['clock'];assert b==p['primary_pre59'];assert len(r['rows'])==len(plan['specs'])==4
for row,(depth,shift) in zip(r['rows'],plan['specs']):
 assert (row['depth_ppm'],row['phase'])==(depth,shift);epoch=b['transit_time']+shift*b['period'];arrays=[]
 for sector in p['sectors']:
  path=Path(f'data/lightcurves/s{sector:04d}-96166003.fits');assert sha(path)==p['inputs'][str(path)];t,f,e,_=read_curve(path);cycles=np.floor((t-epoch)/b['period']+.5);mask=np.abs(t-(epoch+cycles*b['period']))<b['duration']/2;factor=np.where(mask,1-depth/1e6,1);arrays.append(flatten(t,f*factor,e*factor,window=1.5))
 t,y,e=[np.concatenate([a[k] for a in arrays]) for k in range(3)];best,_=refine_training(t,y,e,p['seed'],seed_baseline=p['seed_baseline']);assert best==row['best'];offset=best['transit_time']-epoch;offset-=np.floor(offset/b['period']+.5)*b['period'];assert np.isclose(offset,row['epoch_offset_days']);assert row['period_epoch_match']==bool(abs(best['period']-b['period'])<b['duration']*b['period']/np.ptp(t) and abs(offset)<b['duration'])
save_json(O/'injection-verification.json',dict(status='passed',verified_utc=now(),cases_recomputed=4,script_sha256=sha(Path(__file__)),limits='Independent transit mask and full arithmetic reproduction with shared preprocessing and BLS, not injection completeness or null-model validation.'));print('4 injections verified')
