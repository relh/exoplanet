"""Conditional post-upgrade shape check; fit only an unknown constant offset."""
import json
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import fit,predict
from exoplanet.pipeline import save_json,now,sha
out=Path(__file__).parent;row=next(r for r in json.loads(Path('results/rv-coverage-search-20261010/screening.json').read_text())['results'] if r['name']=='HD297396');p=row['frozen_solution']['periods'];results=[]
for col,ecol in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp')]:
 t,y,e,g=nightly(Path('data/rv/coverage-selected/HD297396.csv'),col,ecol,separate_masks=True);train=np.floor(t+.5)<=row['training_last_night'];held=(~train)&(g=='post:K5');mapped=np.full(held.sum(),'pre:K5')
 for include_toi in [False,True]:
  periods=p+([3.0178746] if include_toi else []);full=fit(t[train],y[train],e[train],g[train],periods);reduced=fit(t[train],y[train],e[train],g[train],periods[1:])
  errors=[];offsets=[]
  for model in [full,reduced]:
   residual=y[held]-predict(model,t[held],mapped);offset=float(np.average(residual,weights=1/e[held]**2));residual-=offset;errors.append(float(np.sum((residual/e[held])**2)));offsets.append(offset)
  result=dict(reduction=col,include_toi=include_toi,n_test=int(held.sum()),chi2_full=errors[0],chi2_without_4d=errors[1],delta_chi2=errors[1]-errors[0],fitted_offsets=offsets);results.append(result);print(result,flush=True)
save_json(out/'postupgrade.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),results=results,limitations='Post-hoc check on already-opened data. Only test-set constant zero point fitted separately under each model; periods, phases, amplitudes and trend from original earliest75percent training data. No independent blind prediction; no significance calibration. Tests temporal shape despite unknown post-upgrade offset.'))
