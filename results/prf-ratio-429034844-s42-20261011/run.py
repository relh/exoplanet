"""Posthoc registration sensitivity with a fixed close-pair scene flux ratio."""
from pathlib import Path
import json,numpy as np
from scipy.optimize import least_squares
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;base=Path('results/prf-429034844-s42-20261011');read=lambda p:json.loads(p.read_text());m=read(base/'models.json')['sectors'][0];r=read(base/'fits.json')['sectors'][0];z=np.load(base/'s42-images.npz');prf=TESS_PRF(m['camera'],m['ccd'],42,m['col'],m['row'],localdatadir='data/prf/start_s0004');pos={k:np.array(v) for k,v in r['positions'].items()};third=np.array(r['scene_positions'][r['scene_ids'].index('429034846')]);shape=z['scene'].shape
q0=read(Path('results/close-blend-429034844-20261011/results.json'))['illustrative_neighbor_to_target_flux_ratio'];ratios=[q0/4,q0/2,q0,q0*2,q0*4]
save_json(out/'plan.json',{'inputs':{str(p):sha(p) for p in [base/'models.json',base/'fits.json',base/'s42-images.npz',Path('results/close-blend-429034844-20261011/results.json')]},'script_sha256':sha(Path(__file__)),'ratios':ratios,'policy':'All five predetermined ratio factors retained; posthoc sensitivity, not catalog ratio precision or source validation. Two linked close templates plus independent third star and plane. Fixed observed difference stack and formal errors.'})
def templates(shift,q):return [prf.locate(*(pos['429034844']+shift),shape)+q*prf.locate(*(pos['611135702']+shift),shape),prf.locate(*(third+shift),shape)]
def align(im,q):
 def evaluate(shift):return fit_templates(im,np.ones(shape),templates(shift,q),nonnegative=True)
 fits=[least_squares(lambda x:evaluate(x)['residual'],start,bounds=(-.6,.6),diff_step=1e-4,max_nfev=100) for start in ([0.,0.],[.2,-.2],[-.2,.2])];best=min(fits,key=lambda x:sum(x.fun*x.fun));assert best.success
 return best.x,evaluate(best.x)
rows=[];controls=[]
for q in ratios:
 shift,f=align(z['scene'],q);hs={k:fit_templates(z['difference'],z['error'],[prf.locate(*(v+shift),shape)]) for k,v in pos.items()};chi={k:f['chi2'] for k,f in hs.items()};rows.append({'ratio':q,'factor_from_catalog':q/q0,'shift':shift.tolist(),'scene_sse':f['chi2'],'scene_coefficients':f['coefficients'].tolist(),'host_chi2':chi,'host_amplitudes':{k:float(f['coefficients'][0]) for k,f in hs.items()},'winner':min(chi,key=chi.get)})
 truth=np.array([.13,-.08]);ts=templates(truth,q);yy,xx=np.indices(shape);synthetic=1800*ts[0]+200*ts[1]+3+.2*xx-.1*yy;recovered,_=align(synthetic,q);np.testing.assert_allclose(recovered,truth,atol=1e-5);controls.append({'ratio':q,'truth':truth.tolist(),'recovered':recovered.tolist()})
save_json(out/'results.json',{'rows':rows,'controls':controls,'limits':'Matched-model noiseless alignment controls validate computation only; no PRF mismatch, epoch-dependent catalog flux or registration probability calibration.'});print(rows)
