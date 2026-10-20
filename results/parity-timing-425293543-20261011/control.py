from pathlib import Path
import json
import numpy as np
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text());b=json.loads(Path('results/timing-425293543-20261011/fits.json').read_text())['joint']['best'];target=json.loads(Path('results/qlp-faint-midradius-remaining-two-20261011/targets/425293543.json').read_text())['target'];t,_,e,_=load_qlp(dict(target,training_sectors=[53,54,80,81]),Path('data'),bin_minutes=0)
p=3.94363;epoch=b['transit_time']+.01;y=np.ones(len(t));rng=np.random.default_rng(425293543)
for phase,depth in ((0,.15),(.495,.14)):
 dist=(t-epoch-phase*p+p/2)%p-p/2;y-=depth*np.exp(-.5*(dist/.02)**2)
y+=rng.normal(0,.001,len(t));err=np.full(len(t),.001);cycle=np.rint((t-b['transit_time'])/b['period']).astype(int);rows=[]
for k in (0,1):
 m=cycle%2==k;best,ranges=refine_training(t[m],y[m],err[m],dict(b,period=2*b['period']))
 delta=(best['period']-p)*86400;offset=(best['transit_time']-epoch-k*.495*p+p/2)%p-p/2
 assert abs(delta)<10 and abs(offset)<.005 and not ranges['search_boundary_hit']
 rows.append({'parity':k,'period_error_seconds':delta,'epoch_error_days':offset})
save_json(out/'control.json',{'script_sha256':sha(Path(__file__)),'seed':425293543,'period_days':p,'separation_phase':.495,'rows':rows,'limits':'One deterministic Gaussian-eclipse control on actual cadence verifies parity selection/refinement plumbing only; not physical model validation or uncertainty calibration.'});print(rows)
