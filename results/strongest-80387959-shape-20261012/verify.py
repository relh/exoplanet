from pathlib import Path
import json,hashlib,numpy as np
from astropy.io import fits
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());b=p['best'];sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();assert sha(O/'plan.json')==r['plan_sha256'];assert sha(p['seed_path'])==p['seed_sha256'];checks=0;mx=0
for row,inp in zip(r['rows'],p['inputs']):
 assert sha(inp['path'])==inp['sha256']==inp['provenance']['sha256']
 with fits.open(inp['path']) as h:
  assert h[0].header['TICID']==80387959 and h[0].header['SECTOR']==row['sector'];d=h[1].data;t=np.asarray(d['TIME'],float);y=np.asarray(d[inp['flux_column']],float);e=np.asarray(d[inp['error_column']],float);sel=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);t,y,e=t[sel],y[sel],e[sel];order=np.argsort(t);t,y,e=t[order],y[order],e[order];med=np.median(y);y=y/med-1;e=e/med
 for case in row['cases']:
  z=np.load(O/f's{row["sector"]}-{case["name"]}.npz');offset=.5 if case['name']=='secondary' else 0;cycles=np.round((t-b['transit_time'])/b['period']-offset).astype(int);dt=t-b['transit_time']-(cycles+offset)*b['period'];sel=np.isin(cycles,case['events'])&(abs(dt)<3*b['duration']);assert np.allclose(t[sel],z['t']);assert np.allclose(y[sel],z['y']);assert np.allclose(e[sel],z['e']);X=z['X'];n=len(case['depths_ppm']);cad=np.median(np.diff(t));dd=dt[sel];edges=p['profile_edges'] if case['name']=='profile' else [-.5,.5];H=[]
  for lo,hi in zip(edges[:-1],edges[1:]):H.append(np.clip(np.minimum(dd+cad/2,hi*b['duration'])-np.maximum(dd-cad/2,lo*b['duration']),0,None)/cad)
  S=np.column_stack(H)
  if case['name']=='parity':S=np.column_stack([S[:,0]*(cycles[sel]%2==0),S[:,0]*(cycles[sel]%2==1)])
  assert np.allclose(-X[:,-n:],S,rtol=0,atol=1e-9);A=X/z['e'][:,None];v=z['y']/z['e'];beta=np.linalg.solve(A.T@A,A.T@v);delta=float(np.max(abs(beta-z['beta'])));mx=max(mx,delta);assert delta<1e-10;cov=np.linalg.inv(A.T@A);chi=np.sum((v-A@beta)**2);scale=max(1,chi/(len(v)-X.shape[1]));cov*=scale;assert np.allclose(cov,z['cov'],rtol=1e-8,atol=1e-14);assert np.allclose(beta[-n:]*1e6,case['depths_ppm'],atol=1e-5)
  for om in case['omission']:
   mask=z['cycles']!=om['event'];xx=X[mask];cols=np.any(abs(xx)>0,axis=0);a=xx[:,cols]/z['e'][mask,None];yy=z['y'][mask]/z['e'][mask];bb=np.linalg.solve(a.T@a,a.T@yy);assert np.allclose(bb[-n:]*1e6,om['depths_ppm'],atol=1e-5)
  if case['name']=='primary':
   assert abs(case['joint_injection_recovered_ppm']-1000)<1e-6;B=X[:,:-1];W=1/z['e']**2;box=-X[:,-1];projection=B@np.linalg.solve((B.T*W)@B,(B.T*W)@box);transfer=1000*np.sum(box*(box-projection)*W)/np.sum(box**2*W);assert abs(transfer-case['unmasked_injection_recovered_ppm'])<1e-6
  checks+=1
summary=[]
for selected in [[10,36,37,63],[90,100]]:
 data=[next(c for c in row['cases'] if c['name']=='primary') for row in r['rows'] if row['sector'] in selected];dep=np.array([a['depths_ppm'][0] for a in data]);err=np.array([a['errors_ppm'][0] for a in data]);w=1/err**2;summary.append(dict(sectors=selected,weighted_depth_ppm=float(np.sum(w*dep)/w.sum()),conditional_error_ppm=float(1/np.sqrt(w.sum()))))
(O/'verification.json').write_text(json.dumps(dict(status='passed',models=checks,max_normal_equation_difference=mx,descriptive_group_depths=summary,scope='Sixrawhashes/identity, rawselection, independentboxoverlaps, normal-equationfits/covariances/omissions, analyticunmaskedprojectiontransfer. Conditionalerrors do not model correlatednoise or productdifferences.'),indent=2)+'\n');print((O/'verification.json').read_text())
