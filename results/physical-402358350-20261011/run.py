from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.physical_fit import fit_circular
O=Path(__file__).parent
E=Path('results/expanded-402358350-20261011/frozen-for81.json');N=Path('results/neighbors-402358350-20261011/neighbors.json');expanded=json.loads(E.read_text());seed=expanded['rows'][0]['best'];star=next(r for r in json.loads(N.read_text()) if r['ID']==402358350)
axis=(6.67430e-11*star['mass']*1.98847e30*(seed['period']*86400)**2/(4*np.pi**2))**(1/3)/(star['rad']*6.957e8)
paths=[E,N,Path(__file__),*[Path('src/exoplanet')/s for s in ['physical_fit.py','transit_model.py','search.py','campaign.py']]]
raw={str(p):sha(p) for p in [Path(f'data/lightcurves/s{s:04d}-402358350.fits') for s in [40,41,54,81]]}
assert not (O/'plan.json').exists()
save_json(O/'plan.json',dict(created_utc=now(),seed=seed,sectors=[40,41,54,81],windows=[1.5,2.5],limb=[.4,.2],axis_log_prior_sigmas=[None,.15],axis_guess=axis,star={k:star[k] for k in ['ID','mass','e_mass','rad','e_rad','rho','e_rho','Tmag']},input_sha256={str(p):sha(p) for p in paths},raw_sha256=raw,policy='Retrospective all-opened data. Circular orbit, target host, no dilution, fixed quadratic limb darkening. Broad log-axis sigma0.15 corresponds to log-density sigma0.45 at fixed period, wider than nominal catalog errors. Three built-in impact starts, max300 evaluations each; no MCMC, no probability. Same expanded primaryseed for both detrendings.'))
rows=[]
for w in [1.5,2.5]:
 t,y,e,data=load_training({'tic':402358350,'training_sectors':[40,41,54,81]},Path('data'),window=w);np.savez_compressed(O/f'w{w}.npz',t=t,y=y,e=e)
 for prior in [None,.15]:
  r=fit_circular(t,y,e,seed,axis,axis_log_prior_sigma=prior);rows.append(dict(window=w,prior=prior,fit=r,data=data));save_json(O/'results.json',dict(plan_sha256=sha(O/'plan.json'),rows=rows));print(w,prior,r['best'],r['conditional_data_chi2'],r['optimization_success'],r['boundary_hit'],flush=True)
