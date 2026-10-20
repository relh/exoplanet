import json
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import fit,predict
from exoplanet.pipeline import save_json,now
out=Path(__file__).parent;screen={r['name']:r for r in json.loads(Path('results/rv-coverage-search-20261010/screening.json').read_text())['results']};rows=[]
for name in ['HD95542','HD297396']:
 for col,ecol in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp')]:
  t,y,e,g=nightly(Path('data/rv/coverage-selected')/(name+'.csv'),col,ecol);periods=screen[name]['frozen_solution']['periods'];m=np.floor(t+.5)<=screen[name]['training_last_night']
  split_masks=[('original',~m)]+[(f'block{i}',np.isin(np.arange(len(t)),idx)) for i,idx in enumerate(np.array_split(np.arange(len(t)),3))]
  for label,test in split_masks:
   train=~test;held=test&np.isin(g,np.unique(g[train]))
   if held.sum()<10:continue
   full=fit(t[train],y[train],e[train],g[train],periods);reduced=fit(t[train],y[train],e[train],g[train],periods[1:]);r1=(y[held]-predict(full,t[held],g[held]))/e[held];r0=(y[held]-predict(reduced,t[held],g[held]))/e[held]
   row=dict(name=name,reduction=col,split=label,n_held=int(held.sum()),first_period=periods[0],amplitude=float(full['amplitudes'][0]),held_delta_chi2=float(r0@r0-r1@r1));rows.append(row);print(row,flush=True)
save_json(out/'temporal.json',dict(created_utc=now(),results=rows,limitations='Post-hoc comparisons at fixed original training periods; three chronological blocks overlap original discovery/validation information. No fresh independent validation. Two reductions share spectra. Offsets/trend and other two sinusoids profiled in training.'))
