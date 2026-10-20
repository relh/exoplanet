import json,csv
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import fit,predict
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('data/rv/coverage-selected/HD297396.csv');row=next(r for r in json.loads(Path('results/rv-coverage-search-20261010/screening.json').read_text())['results'] if r['name']=='HD297396');periods=row['frozen_solution']['periods'];rows=[]
for col,ecol in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp')]:
 for separate in [False,True]:
  t,y,e,g=nightly(source,col,ecol,separate_masks=separate)
  for include_toi in [False,True]:
   ps=periods+([3.0178746] if include_toi else []);original=np.floor(t+.5)>row['training_last_night']
   masks=[('original',original)]+[(f'block{i}',np.isin(np.arange(len(t)),idx)) for i,idx in enumerate(np.array_split(np.arange(len(t)),3))]
   for label,test in masks:
    train=~test;held=test&np.isin(g,np.unique(g[train]))
    if held.sum()<10:continue
    full=fit(t[train],y[train],e[train],g[train],ps);reduced=fit(t[train],y[train],e[train],g[train],ps[1:]);r1=(y[held]-predict(full,t[held],g[held]))/e[held];r0=(y[held]-predict(reduced,t[held],g[held]))/e[held]
    result=dict(reduction=col,separate_masks=separate,include_toi=include_toi,split=label,n_train=int(train.sum()),n_held=int(held.sum()),amplitudes=full['amplitudes'].tolist(),held_delta_chi2=float(r0@r0-r1@r1),group_counts={str(k):int(np.sum(g==k)) for k in np.unique(g)})
    rows.append(result)
    if label=='original' or (separate and not include_toi):print(col,separate,include_toi,label,round(result['held_delta_chi2'],2),np.round(full['amplitudes'],2).tolist(),flush=True)
save_json(out/'comparison.json',dict(created_utc=now(),input_sha256=sha(source),script_sha256=sha(Path(__file__)),ingestion_sha256=sha(Path('src/exoplanet/rv_campaign.py')),periods=periods,toi_period=3.0178746,results=rows,limitations='Post-hoc sensitivity after inspecting reduction disagreement. G2 singleton offset absorbs that exposure, not an independent correction validated on new data. Original failed comparisons retained. Fixed original RV periods; TOI phase free in RV. 2m/s jitter; no activity GP, no FAP calibration.'))
save_json(out/'mask-exposures.json',[r for r in csv.DictReader(source.open()) if r['MASK']!='K5'])
