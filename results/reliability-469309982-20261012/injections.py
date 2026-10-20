from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import read_curve,sha,save_json,now
from run import evaluate
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());obs=json.loads((O/'observed.json').read_text())['result'];b=obs['windows'][0]['best'];specs=[(150,.2),(150,.65),(300,.2),(300,.65)];assert not (O/'injection-plan.json').exists();save_json(O/'injection-plan.json',dict(created_utc=now(),specs=specs,clock=b,script_sha256=sha(Path(__file__)),policy='Limitedrawfluxboxinjectionsbeforeidenticaltwo-windowweakseedprocessing; existingvariabilityremains; fixed150/300ppm,twooffsetepochs. Notcompletenessorblinddiscovery.'))
rows=[]
for ppm,phase in specs:
 raw=[];epoch=b['transit_time']+phase*b['period']
 for s in p['sectors']:
  t,y,e,_=read_curve(Path(f'data/lightcurves/s{s:04d}-469309982.fits'));ph=(t-epoch+b['period']/2)%b['period']-b['period']/2;f=1-ppm*1e-6*(abs(ph)<b['duration']/2);raw.append((t,y*f,e*f))
 r=evaluate(raw,p['seed'],p['baseline']);r.update(depth_ppm=ppm,phase=phase);r['epoch_matches']=[abs((x['best']['transit_time']-epoch+b['period']/2)%b['period']-b['period']/2)<b['duration'] for x in r['windows']];rows.append(r)
save_json(O/'injections.json',dict(plan_sha256=sha(O/'injection-plan.json'),rows=rows));print([(r['depth_ppm'],r['phase'],r['eligible'],r['epoch_matches']) for r in rows])
