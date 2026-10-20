import csv,json
from pathlib import Path
import numpy as np
from exoplanet.rv_search import fit,scan,refine
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;downloads=json.loads((out/'downloads.json').read_text());results=[]
for source in downloads:
 if 'error' in source:continue
 rows=list(csv.DictReader(open(source['path'])));t=[];y=[];err=[]
 for row in rows:
  v=np.array([float(row[k]) for k in ['BJD','RV_mlc_nzp','e_RV_mlc_nzp']])
  if np.all(np.isfinite(v)) and float(row['f_RV'])==0 and 0<v[2]<100 and abs(v[1])<1e6:t.append(v[0]);y.append(v[1]);err.append(v[2])
 t,y,err=map(np.array,[t,y,err]);nights=np.floor(t+.5);tt=[];yy=[];ee=[]
 for n in np.unique(nights):
  m=nights==n;w=1/err[m]**2;tt.append(np.average(t[m],weights=w));yy.append(np.average(y[m],weights=w));ee.append(np.hypot(1/np.sqrt(w.sum()),2.))
 t,y,e=map(np.array,[tt,yy,ee]);row=dict(name=source['name'],n_nights=len(t),input_sha256=sha(Path(source['path'])))
 if len(t)<30 or np.ptp(t)<150:
  row['status']='insufficient_for_pilot';results.append(row);continue
 g=(t>=2457163).astype(int);frequencies=np.arange(.01,1/.8,1/(6*np.ptp(t)));known=[];history=[]
 baseline=fit(t,y,e,g,[]);chi=baseline['chi2']
 for step in range(3):
  power=scan(t,y,e,g,frequencies,known);idx=np.nanargmax(power);period=1/frequencies[idx]
  known.append(period);solution=refine(t,y,e,g,known,fraction=.001);known=list(solution['periods'])
  history.append(dict(periods=known,amplitudes=solution['amplitudes'].tolist(),delta_chi2=chi-solution['chi2'],chi2=solution['chi2']));chi=solution['chi2']
 row.update(status='screened_only',span_days=float(np.ptp(t)),history=history,baseline_chi2=baseline['chi2'],rms=float(np.std(y)),final_rms=float(np.sqrt(np.mean((y-solution['model'])**2))))
 np.savez_compressed(out/(source['name']+'-nightly.npz'),time=t,rv=y,error=e,group=g)
 results.append(row);save_json(out/'screening.json',dict(created_utc=now(),results=results,limitations='Exploratory circular period screen; fixed2m/s nightly white jitter, offsets and trend. No formal FAP, activity vetting, aliases or exhaustive literature check.'))
 print(source['name'],len(t),known,solution['amplitudes'],flush=True)
save_json(out/'screening.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),results=results,limitations='Exploratory circular period screen; fixed2m/s nightly white jitter, offsets and trend. No formal FAP, activity vetting, aliases or exhaustive literature check.'))
