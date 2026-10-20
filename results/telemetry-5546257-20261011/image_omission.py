from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;q=Path('results/prf-motion-5546257-20261011');r=json.loads((q/'fits.json').read_text());rows=[]
for s in r['sectors']:
 path=q/f"s{s['sector']}-images.npz";z=np.load(path);ns=np.array([e['event'] for e in s['events']]);omit=408 if s['sector']==35 else 424
 keep=ns!=omit;es=z['event_differences'][keep];vs=z['event_variances'][keep];w=np.divide(1,vs,out=np.zeros_like(vs),where=vs>0);total=w.sum(axis=0);im=np.divide((w*es).sum(axis=0),total,out=np.zeros_like(total),where=total>0);error=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0));yy,xx=np.indices(im.shape,dtype=float);hs=[]
 for h in s['hypotheses']:
  cs=np.stack([z['template_'+h['tic']],z['gradx'],z['grady'],np.ones(im.shape),xx-xx.mean(),yy-yy.mean()]);ok=np.isfinite(im)&np.isfinite(error)&(error>0)&np.all(np.isfinite(cs),axis=0);a=(cs[:,ok]/error[ok]).T;y=im[ok]/error[ok];c,_,rank,_=lstsq(a,y,lapack_driver='gelsy');assert rank==6;res=y-a@c;chi=float(res@res);saved=next(x for x in s['leave_one_out'] if x['omitted']==omit);prior=next(x for x in saved['hypotheses'] if x['tic']==h['tic']);np.testing.assert_allclose([c[0],chi],[prior['amplitude'],prior['chi2']],rtol=1e-8,atol=1e-8);hs.append(dict(tic=h['tic'],amplitude=float(c[0]),chi2=chi,dof=int(ok.sum()-rank)))
 hs.sort(key=lambda h:h['chi2']);rows.append(dict(sector=s['sector'],omitted_event=int(omit),npz_sha256=sha(path),hypotheses=hs));print(s['sector'],hs[:2])
save_json(p/'image-omission.json',dict(rows=rows,verification='Independent QR reproduces archived leave-one-out fits',policy='Posthoc omissions chosen from telemetry. All-data original fits retained. No calibrated source probabilities.'))
