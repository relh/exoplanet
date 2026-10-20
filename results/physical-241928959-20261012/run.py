from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.qlp_campaign import load_qlp
from fit_record import fit_circular
O=Path(__file__).parent;F=Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json');D=Path('results/qlp-faint-midradius-single-remaining-20261011/targets/241928959.json');N=Path('results/neighbors-241928959-20261011/neighbors.json');raw=Path('data/qlp/241928959-s0092.fits');f=json.loads(F.read_text());seed=f['best'];target=json.loads(D.read_text())['target'];stars=[s for s in json.loads(N.read_text()) if s['ID'] in [241928959,241928961]];stars.sort(key=lambda s:s['ID']);assert sha(raw)==f['training_data'][0]['source']['sha256']
with fits.open(raw) as h:
 cadence=np.median(np.diff(h[1].data['TIME']));headers={k:h[1].header.get(k,h[0].header.get(k)) for k in ['TIMEDEL','EXPOSURE','FRAMETIM','NUM_FRM','BJDREFI']}
frac=1/(1+10**(.4*(stars[1]['Tmag']-stars[0]['Tmag'])))
axis=lambda s:(6.67430e-11*s['mass']*1.98847e30*(seed['period']*86400)**2/(4*np.pi**2))**(1/3)/(s['rad']*6.957e8)
cases=[dict(name='target_free',host=241928959,fraction=1.,axis=axis(stars[0]),prior=None),dict(name='target_broad',host=241928959,fraction=1.,axis=axis(stars[0]),prior=.25),dict(name='neighbor_diluted_illustration',host=241928961,fraction=frac,axis=axis(stars[1]),prior=.25)]
assert not (O/'plan.json').exists();save_json(O/'plan.json',dict(utc=now(),seed=seed,windows=[1.5,2.5],cases=cases,stellar_inputs=[{k:s.get(k) for k in ['ID','mass','e_mass','rad','e_rad','rho','e_rho','Tmag','Teff']} for s in stars],cadence_days=float(cadence),fits_time_headers=headers,hashes={str(p):sha(p) for p in [F,D,N,raw,Path(__file__),O/'fit_record.py',Path('src/exoplanet/physical_fit.py'),Path('src/exoplanet/qlp_campaign.py'),Path('src/exoplanet/search.py')]},policy='Retrospective sector92 native QLP DET_FLUX only; all events surviving each existing flattening (2.5d previously drops one). Circular dark occultor, fixed LD(.4,.2), local event baselines, three starts max300evals. Logaxis prior.25 =>logdensity.75 illustrative broad, not catalog posterior; target youth uncertain. Neighbor mass/radius errors missing: no inferred errors; fixed two-star equal-throughput flux fraction illustrative only. Companionmass/luminosity ignored, k<=.5 model not a general binary fit. No extra fitting matrix or newdata.'))
rows=[]
for w in [1.5,2.5]:
 t,y,e,data=load_qlp(target,Path('data'),window=w,bin_minutes=0);np.savez_compressed(O/f'w{w}.npz',t=t,y=y,e=e)
 for c in cases:
  yy=1+(y-1)/c['fraction'];ee=e/c['fraction'];ss=dict(seed,depth=seed['depth']/c['fraction']);fit=fit_circular(t,yy,ee,ss,c['axis'],axis_log_prior_sigma=c['prior']);rows.append(dict(window=w,case=c,fit=fit,data=data));save_json(O/'results.json',dict(plan_sha256=sha(O/'plan.json'),rows=rows));print(w,c['name'],fit['best'],fit['conditional_data_chi2'],fit['boundary_hit'],fit['optimization_success'],flush=True)
