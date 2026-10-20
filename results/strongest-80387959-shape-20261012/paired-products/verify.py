from pathlib import Path
import json,hashlib,numpy as np
from astropy.io import fits
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();assert sha(O/'plan.json')==r['plan_sha256'];assert sha(O.parent/'plan.json')==p['parent_plan_sha256'];assert sha(O.parent/'results.json')==p['parent_results_sha256'];n=0
for row in r['rows']:
 raw=[]
 for inp in [a for a in p['inputs'] if a['sector']==row['sector']]:
  assert sha(inp['path'])==inp['sha256']==inp['provenance']['sha256']
  with fits.open(inp['path']) as h:
   d=h[1].data;t=np.asarray(d['TIME'],float);y=np.asarray(d[inp['flux']],float);e=np.asarray(d[inp['error']],float);m=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);idx=np.flatnonzero(m);idx=idx[np.argsort(t[idx])];raw.append((t[idx],y[idx],e[idx]))
 z=np.load(O/f's{row["sector"]}-SPOC.npz');ia=z['matched_spoc_indices'];ic=z['matched_qlp_indices'];t1,y1,e1=raw[0];t2,y2,e2=raw[1];assert len(np.unique(ia))==len(np.unique(ic))==row['matched_cadences'];assert np.max(abs(t1[ia]-t2[ic]))<=1e-4;assert abs(np.max(abs(t1[ia]-t2[ic]))*86400-row['max_timestamp_difference_seconds'])<1e-6;ys=[y1[ia]/np.median(y1[ia])-1,y2[ic]/np.median(y2[ic])-1];ts=(t1[ia]+t2[ic])/2;cycles=np.round((ts-p['best']['transit_time'])/p['best']['period']).astype(int);dt=ts-p['best']['transit_time']-cycles*p['best']['period'];m=np.isin(cycles,row['events'])&(abs(dt)<3*p['best']['duration'])
 for case in row['rows']:
  z=np.load(O/f's{row["sector"]}-{case["product"]}.npz');expected=ys[0] if case['product']=='SPOC' else ys[1] if case['product']=='QLP' else ys[0]-ys[1];assert np.allclose(z['t'],ts[m]);assert np.allclose(z['y'],expected[m]);A=z['X']/z['e'][:,None];v=z['y']/z['e'];beta=np.linalg.solve(A.T@A,A.T@v);assert np.allclose(beta,z['beta'],atol=1e-10,rtol=0);assert abs(beta[-1]*1e6-case['depth_ppm'])<1e-5;variance=np.sum((v-A@beta)**2)/(len(v)-A.shape[1]);cov=np.linalg.inv(A.T@A)*(variance if case['product']=='SPOC-minus-QLP' else max(1,variance));assert np.allclose(cov,z['cov'],rtol=1e-8,atol=1e-14)
  for om in case['omissions']:
   mask=z['cycles']!=om['event'];xx=z['X'][mask];xx=xx[:,np.any(abs(xx)>0,axis=0)];aa=xx/z['e'][mask,None];vv=z['y'][mask]/z['e'][mask];bb=np.linalg.solve(aa.T@aa,aa.T@vv);assert abs(bb[-1]*1e6-om['depth_ppm'])<1e-5
  n+=1
(O/'verification.json').write_text(json.dumps(dict(status='passed',models=n,raw_files=4,scope='rawhashes, commoncadence uniqueness/offsets, independentlyreconstructed normalizeddata, normal-equation fit/covariance/omissions; no astrophysical calibration'),indent=2)+'\n');print((O/'verification.json').read_text())
