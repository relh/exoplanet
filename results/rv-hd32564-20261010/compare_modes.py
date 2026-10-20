"""Follow-up sensitivity tests; all HD32564 RVs already opened."""
import json,csv
from pathlib import Path
import numpy as np
from exoplanet.rv_search import fit,refine,design,scan
from exoplanet.pipeline import save_json,now
p=Path(__file__).parent;d=np.load(p/'nightly.npz');t,y,e,g=(d[k] for k in ['time','rv','error','group']);train=d['train'];held=(~train)&(g==0)
baseperiods=json.loads((p/'frozen-training.json').read_text())['periods'];output=[]
for jitter in [1.,2.,3.]:
 errors=np.sqrt(e*e-4+jitter*jitter)
 for first in [baseperiods[0],1.635]:
  for n in [3,4]:
   periods=[first,*baseperiods[1:n]]
   full=refine(t,y,errors,g,periods,fraction=.001)
   training=refine(t[train],y[train],errors[train],g[train],periods,fraction=.001)
   prediction=design(t[held],g[held],training['periods'],training['epoch'])@training['coefficients']
   output.append(dict(jitter=jitter,n_signals=n,periods=full['periods'].tolist(),amplitudes=full['amplitudes'].tolist(),chi2=full['chi2'],rms=float(np.sqrt(np.mean((y-full['model'])**2))),train_periods=training['periods'].tolist(),held_rms=float(np.sqrt(np.mean((y[held]-prediction)**2)))))
save_json(p/'mode-comparison.json',dict(created_utc=now(),results=output,limitations='Post-hoc sensitivity, periods guided by external report. Fixed white jitter; not a marginal likelihood or activity GP.'))
for r in output:
 if r['jitter']==2:print(r)
# Nightly activity fits at the preferred reported family, using the same raw data
# and absolute epochs; diagnostic amplitudes/powers cannot exclude stellar activity.
raw=list(csv.DictReader(open('data/rv/HD32564.csv')))
periods=next(r['periods'] for r in output if r['jitter']==2 and r['n_signals']==4 and r['periods'][0]>2)
activity=[]
for col in ['Halpha','RHKp','BIS','FWHM_DRS','dLW','CRX']:
 at=np.array([float(r['BJD']) for r in raw]);ay=np.array([float(r[col]) for r in raw]);ag=(at>=2457163).astype(int)
 valid=np.isfinite(ay)&(abs(ay)<1e6);at,ay,ag=at[valid],ay[valid],ag[valid]
 ae=np.ones(len(at))*np.std(ay)
 base=fit(at,ay,ae,ag,[]);full=fit(at,ay,ae,ag,periods)
 drops=[]
 for i,period in enumerate(periods):
  reduced=fit(at,ay,ae,ag,periods[:i]+periods[i+1:])
  drops.append(dict(period=period,delta_chi2=reduced['chi2']-full['chi2']))
 activity.append(dict(column=col,n=len(at),periods=periods,amplitudes=full['amplitudes'].tolist(),drops=drops,scale=float(ae[0])))
save_json(p/'activity-diagnostics.json',dict(results=activity,limitations='Per-exposure indicators with empirical full-series scatter as constant scale. Correlated activity, instrumental steps and multiple testing prevent interpreting delta chi-square as detection significance.'))
