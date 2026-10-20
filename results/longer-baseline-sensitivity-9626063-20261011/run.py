from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.campaign import load_training
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
from exoplanet.transit_model import integrated_box
p=Path(__file__).parent;original=Path('results/solar-radius-next512-20261011/targets/9626063.json');row=json.loads(original.read_text());target={**row['target'],'training_sectors':[25,26,52,53]};assert target['heldout_sectors']==[79];assert not Path('data/lightcurves/s0079-9626063.fits').exists()
assert all(not Path(f'data/lightcurves/s{s:04d}-9626063.fits').exists() for s in [52,53])
save_json(p/'plan.json',dict(created_utc=now(),original=str(original),original_sha256=sha(original),target=target,script_sha256=sha(Path(__file__)),policy='Predesign known-injection-clock sensitivity pilot adding previously unused early sectors52/53 to25/26. Keep reserved79 unopened. Same12 probes and epoch as previous shallow injection trial; no blind-search claim.'))
t,y,e,evidence=load_training(target,Path('data'));save_json(p/'inputs.json',evidence)
probes=json.loads(Path('results/solar-radius-shallow-injections-20261011/9626063/summary.json').read_text())['probes'];results=[]
for q in probes:
 arrays=[]
 for s in target['training_sectors']:
  t,f,e,star=read_curve(Path(f'data/lightcurves/s{s:04d}-9626063.fits'));attenuation=1-q['depth']*integrated_box(t,q['period'],q['epoch'],q['duration'],float(np.median(np.diff(t))));arrays.append(flatten(t,f*attenuation,e*attenuation))
 t,y,e=[np.concatenate([a[k] for a in arrays]) for k in range(3)];m=fixed_measure(t,y,e,q['period'],q['epoch'],q['duration']);results.append(dict(probe=q,measurement=m,baseline_days=float(np.ptp(t))))
save_json(p/'results.json',results);print([(r['probe']['depth'],r['probe']['period'],r['probe']['duration'],round(r['measurement']['total']['snr'],2)) for r in results])
