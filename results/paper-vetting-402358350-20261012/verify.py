"""Independent saved-bin reconstruction and direct normal-equation baseline solution."""
from pathlib import Path
import hashlib,json
import numpy as np
p=Path(__file__).parent;b=Path('results/strongest-402358350-baselines-20261012');plan=json.loads((p/'plan.json').read_text());out=json.loads((p/'results.json').read_text());checks=0
for f,h in plan['inputs'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h;checks+=1
assert out['plan_sha256']==hashlib.sha256((p/'plan.json').read_bytes()).hexdigest()
for row in out['rows']:
 if row['status']!='measured':continue
 a=np.load(b/(row['key']+'.npz'));x,y,e,X,o,i=[a[k]for k in ['x','y','e','X','outside','inside']];w=1/e**2;coef=np.linalg.solve(X[o].T@(w[o,None]*X[o]),X[o].T@(w[o]*y[o]));res=y-X@coef
 assert abs(-np.sum(res[i]*w[i])/w[i].sum()-row['depth'])<2e-12;checks+=1
 expected_segments=[];part=[];cad=np.median(np.diff(x))
 for j in range(len(x)):
  if not o[j]:
   if part:expected_segments.append(part);part=[]
   continue
  if part and (j!=part[-1]+1 or x[j]-x[part[-1]]>1.5*cad):expected_segments.append(part);part=[]
  part.append(j)
 if part:expected_segments.append(part)
 assert expected_segments==row['diagnostic']['segments'];checks+=1
 betas=[1.]
 for t in row['diagnostic']['trials']:
  n=max(2,round(t['duration']/cad));assert n==t['n']
  chunks=[]
  for seg in expected_segments:
   for start in range(t['offset'],len(seg)-n+1,n):chunks.append(seg[start:start+n])
  assert chunks==t['chunks'] and len(chunks)==t['m'];checks+=1
  means=[sum(res[k]for k in chunk)/n for chunk in chunks];assert np.allclose(means,t['means'],atol=2e-12,rtol=0)
  if len(means)<4:assert t['status']=='insufficient_bins';continue
  sigma=np.sqrt(sum((res[o]-np.mean(res[o]))**2)/sum(o));m=len(means);sb=np.sqrt(sum((np.array(means)-np.mean(means))**2)/m);beta=sb/(sigma*np.sqrt(m/(n*(m-1))));assert abs(beta-t['beta'])<2e-7;betas.append(beta);checks+=1
 assert abs(max(betas)-row['diagnostic']['beta'])<2e-7;checks+=1
for s in out['summary']:
 rr=[r for r in out['rows']if r['status']=='measured'and all(r[k]==s[k]for k in ['kind','degree','outer'])];w=np.array([r['original_error']**-2 for r in rr]);w/=sum(w);depth=sum(v*r['depth']for v,r in zip(w,rr));err=np.sqrt(sum((v*r['inflated_error'])**2 for v,r in zip(w,rr)));assert abs(depth-s['depth'])<1e-15 and abs(err-s['inflated_error_fixed_weights'])<1e-15;checks+=2
assert len([r for r in out['rows']if r['status']=='measured'])==96
assert len([r for r in out['rows']if r['status']!='measured'])==12
(p/'verification.json').write_text(json.dumps(dict(status='passed',checks=checks,scope='Input hashes, independent normal equations, segment boundaries, every saved bin/beta, all fixed-weight aggregates; no raw FITS reread or astrophysical validation.'),indent=2)+'\n');print(checks,'checks passed')
