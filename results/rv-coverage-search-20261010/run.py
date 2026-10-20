import json
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import scan,refine,fit
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;selection=Path('results/rv-coverage-20261010/selection.json');targets=json.loads(selection.read_text())['targets']
save_json(out/'configuration.json',dict(created_utc=now(),selection_sha256=sha(selection),script_sha256=sha(Path(__file__)),module_sha256=sha(Path('src/exoplanet/rv_search.py')),ingestion_sha256=sha(Path('src/exoplanet/rv_campaign.py')),period_min=.8,period_max='min(1000, training span/3)',samples_per_peak=8,max_components=3,jitter=2.,policy='Only earliest75percent nights used for search. Later nights reserved from fitting and rankings. All targets retained regardless result. HD85512 known false-positive/activity case, not new-candidate eligible.'))
rows=[]
for target in targets:
 name=target['name'];p=Path('data/rv/coverage-selected')/(name+'.csv')
 t,y,e,g=nightly(p);training=np.floor(t+.5)<=target['train_last_night'];ntest=int((~training).sum());t,y,e,g=[a[training] for a in [t,y,e,g]]
 row=dict(name=name,n_train=len(t),n_reserved=ntest,input_sha256=sha(p),training_last_night=target['train_last_night'])
 try:
  maximum=min(1000,np.ptp(t)/3);f=np.arange(1/maximum,1/.8,1/(8*np.ptp(t)));periods=[];steps=[];previous=fit(t,y,e,g,[])['chi2']
  for step in range(3):
   power=scan(t,y,e,g,f,periods);indices=np.argsort(np.nan_to_num(power,nan=-np.inf))[::-1];peaks=[]
   for idx in indices:
    if all(abs(f[idx]-1/r['period'])>3/np.ptp(t) for r in peaks):peaks.append(dict(period=float(1/f[idx]),delta_chi2=float(power[idx])))
    if len(peaks)==5:break
   periods.append(peaks[0]['period']);solution=refine(t,y,e,g,periods,fraction=.001);periods=list(solution['periods']);steps.append(dict(periods=periods,amplitudes=solution['amplitudes'].tolist(),chi2=solution['chi2'],delta_chi2=previous-solution['chi2'],top_peaks=peaks));previous=solution['chi2']
  row.update(status='screened',steps=steps,train_rms=float(np.std(y)),residual_rms=float(np.std(y-solution['model'])),frozen_solution={k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in solution.items() if k not in ['model','residual']})
  print(name,len(t),np.round(periods,4).tolist(),np.round(solution['amplitudes'],2).tolist(),flush=True)
 except Exception as exc:row.update(status='error',error=f'{type(exc).__name__}: {exc}');print(name,row['error'],flush=True)
 rows.append(row);save_json(out/'screening.json',dict(created_utc=now(),results=rows))
