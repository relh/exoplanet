from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from astropy.io import fits
from exoplanet.pixel_vet import difference_events,individual_difference_events
from exoplanet.pipeline import sha,save_json
from exoplanet.prf_fit import fit_templates
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'fits.json').read_text());models=json.loads((p/'models.json').read_text());count=0;local=[]
assert sha(p/'analyze.py')==plan['script_sha256'];assert sha(p/'models.json')==plan['models_sha256'];assert sha((p/'frozen.json'))==plan['frozen_sha256'];assert sha(Path('results/neighbors-402358350-20261011/neighbors.json'))==plan['neighbors_sha256']
def qr(im,error,cols):
 yy,xx=np.indices(im.shape,dtype=float);cs=np.stack(cols+[np.ones(im.shape),xx-xx.mean(),yy-yy.mean()]);ok=np.isfinite(im)&np.isfinite(error)&(error>0)&np.all(np.isfinite(cs),axis=0);a=(cs[:,ok]/error[ok]).T;y=im[ok]/error[ok];coef,_,rank,_=lstsq(a,y,lapack_driver='gelsy');assert rank==len(cs);res=y-a@coef;return coef,float(res@res),a
for m,s in zip(models['sectors'],r['sectors']):
 assert sha(Path(m['pixel_path']))==m['pixel_sha256']
 for model in m['models']:assert sha(Path(model['path']))==model['source']['sha256']
 z=np.load(p/f"s{s['sector']}-images.npz");best=json.loads((p/'frozen.json').read_text())['best']
 with fits.open(m['pixel_path']) as hd:
  assert hd[0].header['TICID']==402358350 and hd[0].header['SECTOR']==81
  a=hd[1].data;t=np.asarray(a['TIME'],float);valid=np.isfinite(t);t=t[valid];flux=np.asarray(a['FLUX'][valid],float);err=np.asarray(a['FLUX_ERR'][valid],float);qual=a['QUALITY'][valid]
 diff,sigma,events,numbers=difference_events(t,flux,err,qual,best);evs,vars,nums=individual_difference_events(t,flux,err,qual,best)
 for key,value in [('difference',diff),('error',sigma),('event_differences',evs),('event_variances',vars)]:np.testing.assert_allclose(z[key],value,rtol=0,atol=0)
 assert nums==numbers==[x['event'] for x in s['events']]
 gx,gy=z['gradx'],z['grady'];sets=[(z['difference'],z['error'],s['hypotheses'])]
 sets.extend((z['event_differences'][i],np.sqrt(z['event_variances'][i]),v['hypotheses']) for i,v in enumerate(s['events']))
 for i,loo in enumerate(s['leave_one_out']):
  keep=np.arange(len(s['events']))!=i;vs=z['event_variances'][keep];es=z['event_differences'][keep];w=np.divide(1,vs,out=np.zeros_like(vs),where=vs>0);total=w.sum(axis=0);im=np.divide((w*es).sum(axis=0),total,out=np.zeros_like(total),where=total>0);e=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0));sets.append((im,e,loo['hypotheses']))
 for im,e,hs in sets:
  _,baseline,_=qr(im,e,[gx,gy])
  for h in hs:
   template=z['template_'+h['tic']];c,chi,_=qr(im,e,[template,gx,gy]);cp,chp,_=qr(im,e,[template]);np.testing.assert_allclose([c[0],chi,*c[1:3],cp[0],chp,baseline],[h['amplitude'],h['chi2'],*h['motion_coefficients'],h['without_motion_amplitude'],h['without_motion_chi2'],h['motion_only_chi2']],rtol=1e-8,atol=1e-8);count+=1
 loc=next(x for x in json.loads((p/'local-regions.json').read_text())['sectors'] if x['sector']==s['sector']);yy,xx=np.indices(z['difference'].shape);pos=np.array(s['positions']['402358350'])+s['alignment'];rad=np.hypot(xx-pos[0],yy-pos[1]);target=z['template_402358350']
 for case in loc['cases']:
  error=np.where(rad<=case['radius_pixels'],z['error'],np.inf);_,baseline,_=qr(z['difference'],error,[gx,gy]);np.testing.assert_allclose(baseline,case['motion_only_chi2'])
  for h in case['hypotheses']:
   c,chi,a=qr(z['difference'],error,[z['template_'+h['tic']],gx,gy]);cp,chp,_=qr(z['difference'],error,[z['template_'+h['tic']]]);np.testing.assert_allclose([c[0],chi,cp[0],chp],[h['amplitude'],h['chi2'],h['without_motion_amplitude'],h['without_motion_chi2']],rtol=1e-8,atol=1e-8);count+=1
  c,chi,a=qr(z['difference'],error,[target,gx,gy]);sigma=np.sqrt(np.linalg.inv(a.T@a)[0,0]);injected=z['difference']+5*target;ci,_,_=qr(injected,error,[target,gx,gy]);np.testing.assert_allclose(ci[0]-c[0],5,atol=1e-8)
  fake=5*target+3*gx-2*gy+.1;cf,_,_=qr(fake,error,[target,gx,gy]);np.testing.assert_allclose(cf[:3],[5,3,-2],atol=1e-8)
  local.append(dict(sector=s['sector'],radius_pixels=case['radius_pixels'],target_amplitude=float(c[0]),formal_error=float(sigma),conditional_snr=float(c[0]/sigma),delta_chi2_vs_motion_only=baseline-chi,design_condition_number=float(np.linalg.cond(a)),injected_amplitude_recovered=float(ci[0]-c[0])))
lp=json.loads((p/'local-regions-plan.json').read_text());assert sha(p/'local_regions.py')==lp['script_sha256'];assert sha(p/'fits.json')==lp['fits_sha256']
frozen=json.loads((p/'frozen.json').read_text());held=Path('results/heldout-402358350-s81-20261011');execution=json.loads((held/'execution.json').read_text());pixel=json.loads((p/'pixels/localization.json').read_text());expanded=Path(frozen['source']);exp=json.loads(expanded.read_text());assert sha(expanded)==frozen['source_sha256']==execution['input_sha256'][str(expanded)];assert sha(held/'execution.json')==frozen['heldout_execution_sha256'];assert sha(held/'verification.json')==frozen['heldout_verification_sha256'];assert frozen['best']==next(x['best'] for x in exp['rows'] if x['role']=='primary')
from datetime import datetime
assert datetime.fromisoformat(exp['frozen_utc'])<datetime.fromisoformat(execution['started_utc'])<datetime.fromisoformat(execution['finished_utc'])<datetime.fromisoformat(pixel['source']['retrieved_utc'])
assert datetime.fromisoformat(frozen['created_utc'])<datetime.fromisoformat(pixel['source']['retrieved_utc'])
save_json(p/'verification.json',dict(status='passed',independent_QR_hypothesis_fits_checked=count,local_target_diagnostics=local,raw_and_PRF_hashes_checked=True,pre81_clock_and_source_check_opening_chronology_verified=True,limits='Formal conditional errors ignore pixel correlations and model mismatch. Matched-template injection verifies linear identifiability, not survey completeness or real-PRF accuracy.'))
print(count,local)
