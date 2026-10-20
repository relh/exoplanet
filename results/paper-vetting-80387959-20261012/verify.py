from pathlib import Path
import json,hashlib,numpy as np
from run import maps,fit,split,D
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(O/'plan.json')==r['plan_sha256'];checks=0;max_ref_diff=0
for inp in p['inputs']:
 assert sha(inp['path'])==inp['sha256'];z=np.load(inp['path']);sector=int(Path(inp['path']).name.split('-')[0][1:]);row=next(v for v in r['rows'] if v['sector']==sector)
 for rec in [row['full']]+row['omissions']:
  m=np.ones(len(z['t']),bool) if 'omitted_event' not in rec else z['cycles']!=rec['omitted_event'];t,c,y,e=[z[k][m] for k in ['t','cycles','y','e']];X=z['X'][m];X=X[:,np.any(X!=0,axis=0)];w=1/e**2;C=np.linalg.inv(X.T@(w[:,None]*X));L=C@(X.T*w);b=L@y;res=y-X@b;scale=max(1,np.sqrt(np.sum((res/e)**2)/(len(y)-len(b))));assert np.isclose(b[-1]*1e6,rec['depth_ppm']);assert np.isclose(np.sqrt(C[-1,-1])*scale*1e6,rec['white_error_ppm']);checks+=2
  for (info,bins),v in zip(maps(t,c),rec['scales']):
   for ix in bins:assert len(set(c[ix]))==1 and np.all(np.diff(t[ix])<=1.5*np.median(np.diff(t)[np.diff(c)==0]));checks+=1
   if v['status']!='ok':continue
   rms=np.sqrt(np.mean([np.mean(res[i])**2 for i in bins]));vari=[]
   for ix in bins:
    a=np.zeros(len(t));a[ix]=1/len(ix);q=a-(a@X)@L;vari.append(np.sum((q*e*scale)**2))
   exact=np.sqrt(np.mean(vari))*1e6;diff=abs(v['white_reference_ppm']/exact-1);max_ref_diff=max(max_ref_diff,diff);assert diff<.05;assert np.isclose(rms*1e6,v['rms_ppm']);checks+=2
  assert np.isclose(rec['beta'],max([1]+[v['beta'] for v in rec['scales'] if v['status']=='ok']));checks+=1
 (O/'verification.json').write_text(json.dumps(dict(passed=True,checks=checks,max_white_monte_carlo_relative_difference_from_analytic=max_ref_diff),indent=2))
print(checks,max_ref_diff)
