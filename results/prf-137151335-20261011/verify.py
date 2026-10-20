from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text());fits=json.loads((out/'fits.json').read_text());tic=fits['tic']
assert sha(out/'analyze.py')==plan['script_sha256'];assert sha(out/'models.json')==plan['models_sha256'];assert sha(Path(f'results/source-check-{tic}-20261011/frozen.json'))==plan['frozen_sha256'];assert sha(Path(f'results/neighbors-{tic}-20261011/neighbors.json'))==plan['neighbors_sha256']
count=0;winners=[]
def verify(im,error,templates,rows):
 global count
 yy,xx=np.indices(im.shape,dtype=float)
 for r in rows:
  cols=np.stack([templates[r['tic']],np.ones(im.shape),xx-xx.mean(),yy-yy.mean()]);ok=np.isfinite(im)&np.isfinite(error)&(error>0)&np.all(np.isfinite(cols),axis=0);a=(cols[:,ok]/error[ok]).T;y=im[ok]/error[ok];coef,_,_,_=lstsq(a,y,lapack_driver='gelsy');res=y-a@coef
  np.testing.assert_allclose([coef[0],res@res],[r['amplitude'],r['chi2']],rtol=1e-9,atol=1e-8);count+=1
for meta,r in zip(json.loads((out/'models.json').read_text())['sectors'],fits['sectors']):
 assert meta['sector']==r['sector'];assert sha(Path(meta['pixel_path']))==meta['pixel_sha256']
 for m in meta['models']:assert sha(Path(m['path']))==m['source']['sha256']
 z=np.load(out/f"s{r['sector']}-images.npz");templates={h['tic']:z['template_'+h['tic']] for h in r['hypotheses']}
 verify(z['difference'],z['error'],templates,r['hypotheses'])
 for i,event in enumerate(r['events']):verify(z['event_differences'][i],np.sqrt(z['event_variances'][i]),templates,event['hypotheses'])
 for i,entry in enumerate(r['leave_one_out']):
  keep=np.arange(len(r['events']))!=i;v=z['event_variances'][keep];e=z['event_differences'][keep];w=np.divide(1,v,out=np.zeros_like(v),where=v>0);total=w.sum(axis=0);im=np.divide((w*e).sum(axis=0),total,out=np.zeros_like(total),where=total>0);error=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0));verify(im,error,templates,entry['hypotheses'])
 assert not r['alignment_boundary'];np.testing.assert_allclose(r['synthetic_registration_recovered'],[.12,-.08],atol=1e-5)
 winners.append(dict(sector=r['sector'],stack=r['hypotheses'][0],loo_hosts=sorted(set(x['hypotheses'][0]['tic'] for x in r['leave_one_out'])),individual_hosts=sorted(set(x['hypotheses'][0]['tic'] for x in r['events'])),all_stack_and_loo_winning_amplitudes_positive=all(x['amplitude']>0 for x in [r['hypotheses'][0]]+[x['hypotheses'][0] for x in r['leave_one_out']])))
save_json(out/'verification.json',dict(status='passed',independent_QR_linear_fits_checked=count,raw_and_model_hashes_checked=True,synthetic_registration_checked=True,winners=winners,core_source_sha256={p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},limits='QR reconstructions validate saved fits, not physical PRF accuracy or probabilistic source attribution. Registration synthetic check uses identical PRF and Tmag scene.'))
print(count,winners)
