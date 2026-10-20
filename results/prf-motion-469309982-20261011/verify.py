from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from exoplanet.pipeline import sha,save_json
from exoplanet.prf_fit import fit_templates
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'fits.json').read_text());models=json.loads((p/'models.json').read_text());count=0;local=[]
assert sha(p/'analyze.py')==plan['script_sha256'];assert sha(p/'models.json')==plan['models_sha256'];assert sha(Path('results/source-check-469309982-20261011/frozen.json'))==plan['frozen_sha256'];assert sha(Path('results/neighbors-469309982-20261011/neighbors.json'))==plan['neighbors_sha256']
def qr(im,error,cols):
 yy,xx=np.indices(im.shape,dtype=float);cs=np.stack(cols+[np.ones(im.shape),xx-xx.mean(),yy-yy.mean()]);ok=np.isfinite(im)&np.isfinite(error)&(error>0)&np.all(np.isfinite(cs),axis=0);a=(cs[:,ok]/error[ok]).T;y=im[ok]/error[ok];coef,_,rank,_=lstsq(a,y,lapack_driver='gelsy');assert rank==len(cs);res=y-a@coef;return coef,float(res@res),a
for m,s in zip(models['sectors'],r['sectors']):
 assert sha(Path(m['pixel_path']))==m['pixel_sha256']
 for model in m['models']:assert sha(Path(model['path']))==model['source']['sha256']
 z=np.load(p/f"s{s['sector']}-images.npz");gx,gy=z['gradx'],z['grady'];sets=[(z['difference'],z['error'],s['hypotheses'])]
 sets.extend((z['event_differences'][i],np.sqrt(z['event_variances'][i]),v['hypotheses']) for i,v in enumerate(s['events']))
 for i,loo in enumerate(s['leave_one_out']):
  keep=np.arange(len(s['events']))!=i;vs=z['event_variances'][keep];es=z['event_differences'][keep];w=np.divide(1,vs,out=np.zeros_like(vs),where=vs>0);total=w.sum(axis=0);im=np.divide((w*es).sum(axis=0),total,out=np.zeros_like(total),where=total>0);e=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0));sets.append((im,e,loo['hypotheses']))
 for im,e,hs in sets:
  _,baseline,_=qr(im,e,[gx,gy])
  for h in hs:
   template=z['template_'+h['tic']];c,chi,_=qr(im,e,[template,gx,gy]);cp,chp,_=qr(im,e,[template]);np.testing.assert_allclose([c[0],chi,*c[1:3],cp[0],chp,baseline],[h['amplitude'],h['chi2'],*h['motion_coefficients'],h['without_motion_amplitude'],h['without_motion_chi2'],h['motion_only_chi2']],rtol=1e-8,atol=1e-8);count+=1
 loc=next(x for x in json.loads((p/'local-regions.json').read_text())['sectors'] if x['sector']==s['sector']);yy,xx=np.indices(z['difference'].shape);pos=np.array(s['positions']['469309982'])+s['alignment'];rad=np.hypot(xx-pos[0],yy-pos[1]);target=z['template_469309982']
 for case in loc['cases']:
  error=np.where(rad<=case['radius_pixels'],z['error'],np.inf);_,baseline,_=qr(z['difference'],error,[gx,gy]);np.testing.assert_allclose(baseline,case['motion_only_chi2'])
  for h in case['hypotheses']:
   c,chi,a=qr(z['difference'],error,[z['template_'+h['tic']],gx,gy]);cp,chp,_=qr(z['difference'],error,[z['template_'+h['tic']]]);np.testing.assert_allclose([c[0],chi,cp[0],chp],[h['amplitude'],h['chi2'],h['without_motion_amplitude'],h['without_motion_chi2']],rtol=1e-8,atol=1e-8);count+=1
  c,chi,a=qr(z['difference'],error,[target,gx,gy]);sigma=np.sqrt(np.linalg.inv(a.T@a)[0,0]);injected=z['difference']+5*target;ci,_,_=qr(injected,error,[target,gx,gy]);np.testing.assert_allclose(ci[0]-c[0],5,atol=1e-8)
  fake=5*target+3*gx-2*gy+.1;cf,_,_=qr(fake,error,[target,gx,gy]);np.testing.assert_allclose(cf[:3],[5,3,-2],atol=1e-8)
  local.append(dict(sector=s['sector'],radius_pixels=case['radius_pixels'],target_amplitude=float(c[0]),formal_error=float(sigma),conditional_snr=float(c[0]/sigma),delta_chi2_vs_motion_only=baseline-chi,design_condition_number=float(np.linalg.cond(a)),injected_amplitude_recovered=float(ci[0]-c[0])))
save_json(p/'verification.json',dict(status='passed',independent_QR_hypothesis_fits_checked=count,local_target_diagnostics=local,raw_and_PRF_hashes_checked=True,limits='Formal conditional errors ignore pixel correlations and model mismatch. Matched-template injection verifies linear identifiability, not survey completeness or real-PRF accuracy.'))
print(count,local)
