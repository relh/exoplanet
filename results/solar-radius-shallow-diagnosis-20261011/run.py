from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import read_curve,sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
from exoplanet.transit_model import integrated_box
p=Path(__file__).parent;parent=Path('results/solar-radius-shallow-injections-20261011');selected=json.loads((parent/'selected.json').read_text());outcomes=json.loads((parent/'results.json').read_text());save_json(p/'plan.json',dict(created_utc=now(),inputs={str(parent/q):sha(parent/q) for q in ['selected.json','results.json','run.py']},script_sha256=sha(Path(__file__)),policy='Post-outcome diagnostic at injected true clock; same original data, attenuation and1.5-day detrending. Oracle-clock measurement is not blind recovery or planet evidence.'))
rows=[]
for original,outcome in zip(selected,outcomes):
 assert original['tic']==outcome['tic'];curves=[]
 for s in original['target']['training_sectors']:
  raw=Path(f"data/lightcurves/s{s:04d}-{original['tic']}.fits");t,f,e,star=read_curve(raw);curves.append((t,f,e,sha(raw)))
 for probe in outcome['probes']:
  baseline=[];injected=[]
  for t,f,e,digest in curves:
   attenuation=1-probe['depth']*integrated_box(t,probe['period'],probe['epoch'],probe['duration'],float(np.median(np.diff(t))))
   baseline.append(flatten(t,f,e));injected.append(flatten(t,f*attenuation,e*attenuation))
  measurements=[]
  for parts in [baseline,injected]:
   t,y,e=[np.concatenate([a[k] for a in parts]) for k in range(3)];measurements.append(fixed_measure(t,y,e,probe['period'],probe['epoch'],probe['duration'])['total'])
  b,i=measurements
  rows.append(dict(tic=original['tic'],probe=probe,baseline=b,injected=i,incremental_depth=None if b is None or i is None else i['depth']-b['depth'],incremental_depth_fraction=None if b is None or i is None else (i['depth']-b['depth'])/probe['depth'],ideal_depth_over_measured_error=None if i is None else probe['depth']/i['error'],raw_hashes=[c[3] for c in curves]))
save_json(p/'results.json',rows)
for depth in [.0001,.0003]:
 rs=[r for r in rows if r['probe']['depth']==depth];print(depth,[(r['tic'],r['probe']['period'],r['probe']['duration'],round(r['injected']['snr'],2) if r['injected'] else None,round(r['incremental_depth_fraction'],2) if r['incremental_depth_fraction'] is not None else None) for r in rs])
