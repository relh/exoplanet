from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.followup import refine_training,fixed_measure
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');fit=read(out/'fit.json');r=read(out/'results.json')
assert plan['script_sha256']==sha(out/'run.py')
for group in ['inputs','source_hashes','raw']:
 for p,h in plan[group].items():assert sha(Path(p))==h
assert sha(out/'folds.png')==r['plot_sha256'];assert [r['sector'] for r in r['rows']]==plan['sectors']
# Deterministic gapped noiseless alternating eclipses, exercise the same joint fitter.
p=.4669;epoch=100.;duration=.032;t=np.concatenate([np.arange(a,a+20,.005) for a in [90,120,850]])
phase=(t-epoch+p/2)%p-p/2;cycle=np.rint((t-epoch)/p).astype(int);e=np.full_like(t,.002);checks=[]
for depths in [[.02,.02],[.025,.015]]:
 y=np.ones_like(t)
 for parity,d in enumerate(depths):y[(cycle%2==parity)&(abs(phase)<duration/2)]-=d
 b,rr=refine_training(t,y,e,{'period':p+.00002,'duration':duration},seed_baseline=20)
 assert abs(b['period']-p)<duration*p/np.ptp(t)
 # Evaluate true centers to test alternating-depth extraction independently of selected fit.
 rec=[fixed_measure(t,y,e,2*p,epoch+i*p,duration)['total']['depth'] for i in [0,1]]
 np.testing.assert_allclose(rec,depths,atol=1e-10)
 checks.append({'injected_period':p,'recovered_period':b['period'],'depths':depths,'recovered_depths':rec})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'fit_sha256':sha(out/'fit.json'),'results_sha256':sha(out/'results.json'),'controls':checks,'status':'Provenance and two gapped synthetic joint-clock controls passed; not calibrated false-positive or cycle-count probability.'});print('Verified two joint-clock controls and provenance.')
