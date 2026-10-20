"""Apply saved models to reserved nights without period/phase refitting."""
import json
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import fit,predict,refine
from exoplanet.pipeline import save_json,now,sha
out=Path(__file__).parent;screen=out/'screening.json';results=[]
for row in json.loads(screen.read_text())['results']:
 if row['status']!='screened':continue
 name=row['name'];t,y,e,g=nightly(Path('data/rv/coverage-selected')/(name+'.csv'));train=np.floor(t+.5)<=row['training_last_night'];model=row['frozen_solution'];held=(~train)&np.isin(g,model['group_levels']);n=int(held.sum())
 result=dict(name=name,n_test=n,n_unknown_offset=int(np.sum((~train)&(~np.isin(g,model['group_levels'])))))
 if n<10:result['status']='insufficient_same_instrument';results.append(result);continue
 pred=predict(model,t[held],g[held]);null=fit(t[train],y[train],e[train],g[train],[]);nullpred=predict(null,t[held],g[held]);chi=float(np.sum(((y[held]-pred)/e[held])**2));basechi=float(np.sum(((y[held]-nullpred)/e[held])**2));drops=[]
 for i,period in enumerate(model['periods']):
  other=model['periods'][:i]+model['periods'][i+1:]
  reduced=refine(t[train],y[train],e[train],g[train],other,fraction=.001)
  rpred=predict(reduced,t[held],g[held]);drops.append(dict(period=period,delta_chi2=float(np.sum(((y[held]-rpred)/e[held])**2))-chi))
 result.update(status='tested',delta_chi2=basechi-chi,rms_model=float(np.sqrt(np.mean((y[held]-pred)**2))),rms_baseline=float(np.sqrt(np.mean((y[held]-nullpred)**2))),components=drops)
 results.append(result);print(name,n,round(basechi-chi,2),[(round(r['period'],3),round(r['delta_chi2'],2)) for r in drops],flush=True)
save_json(out/'heldout.json',dict(created_utc=now(),screen_sha256=sha(screen),script_sha256=sha(Path(__file__)),results=results,limitations='Saved full-model predictions, no held-period/phase/amplitude refit. Drop-component comparisons re-optimize only training data. Unknown instrumental offsets are excluded rather than estimated from held RVs. Fixed white jitter, no red-noise null calibration; chi-square improvements are descriptive, not significance. Stars or components selected after this check require fresh validation.'))
