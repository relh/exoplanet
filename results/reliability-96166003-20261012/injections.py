"""Four deterministic raw-flux injections; processing sanity checks only."""
from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import read_curve,save_json,sha,now
from exoplanet.search import flatten
from exoplanet.followup import refine_training
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['primary_pre59'];specs=[(300,.2),(300,.65),(600,.2),(600,.65)];assert not (O/'injection-plan.json').exists();save_json(O/'injection-plan.json',dict(created_utc=now(),specs=specs,clock=b,script_sha256=sha(Path(__file__)),policy='Fourdeterministicboxinjections into raw qualityscreenedPDCSAP before samepersectorflatten. Fixedprimaryperiod/duration withtwooffsetepochs,depth300/600ppm. Existingvariability/signalsremain. Reuseidenticallocalfamilymaxstatistic; checksrecovery underexistingbackground, not completeness/nullmodelcalibration. Plannedafteroriginalnulls, notusedtoalterthem.'))
rows=[]
for ppm,phase in specs:
 arrays=[];epoch=b['transit_time']+phase*b['period']
 for sector in p['sectors']:
  t,y,e,_=read_curve(Path(f'data/lightcurves/s{sector:04d}-96166003.fits'));ph=(t-epoch+b['period']/2)%b['period']-b['period']/2;factor=1-ppm*1e-6*(abs(ph)<b['duration']/2);arrays.append(flatten(t,y*factor,e*factor,window=1.5))
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];best,_=refine_training(t,y,e,p['seed'],seed_baseline=p['seed_baseline']);offset=((best['transit_time']-epoch+b['period']/2)%b['period']-b['period']/2);rows.append(dict(depth_ppm=ppm,phase=phase,best=best,epoch_offset_days=float(offset),period_difference_days=best['period']-b['period'],period_epoch_match=bool(abs(best['period']-b['period'])<b['duration']*b['period']/np.ptp(t) and abs(offset)<b['duration'])))
save_json(O/'injections.json',dict(plan_sha256=sha(O/'injection-plan.json'),rows=rows));print(rows)
