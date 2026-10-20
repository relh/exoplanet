import json
from pathlib import Path
import numpy as np
from exoplanet.pipeline import read_curve,save_json,sha,now
from exoplanet.search import flatten,diagnostics
from exoplanet.followup import refine_training
from exoplanet.vetting import extended_vetting
from exoplanet.injection_grid import integrated_box
out=Path('results/vetting-calibration-20261009');results=[]
for tic in [351654581,238870740]:
 path=Path(f'results/injection-grid-20261009/{tic}/p1.37-d0.12-z0.00075/targets/{tic}.json');r=json.loads(path.read_text());probe=r['target']['injection'];parts=[]
 for s in r['target']['training_sectors']:
  t,f,e,_=read_curve(Path(f'data/lightcurves/s{s:04d}-{tic}.fits'))
  attenuation=1-probe['depth']*integrated_box(t,probe['period'],probe['epoch'],probe['duration'],np.median(np.diff(t)))
  parts.append(flatten(t,f*attenuation,e*attenuation))
 t,y,dy=(np.concatenate([p[k] for p in parts]) for k in range(3));seed=next(p for p in r['screened_peaks'] if abs(p['best']['period']/probe['period']-1)<.005)
 best=seed['best'];refined,_=refine_training(t,y,dy,best);truth={**best,'period':probe['period'],'transit_time':probe['epoch'],'duration':probe['duration']}
 row={'tic':tic,'source_sha256':sha(path),'cases':[]}
 for name,b in [('coarse',best),('refined_box',refined),('true_injection',truth)]:
  diag=diagnostics(t,y,dy,b,shared=seed['diagnostics']);ext=extended_vetting(t,y,dy,b,diag)
  row['cases'].append({'name':name,'best':b,'odd_even_sigma':diag['odd_even_sigma'],'event_consistency':ext['event_consistency']})
 results.append(row);save_json(out/'results.json',results);print(row,flush=True)
save_json(out/'run.json',{'finished_utc':now(),'experiment_sha256':sha(out/'experiment.py'),'note':'Known injected ephemerides used only to diagnose pipeline behavior; never used for real-candidate fits'})
