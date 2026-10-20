from pathlib import Path
import json,hashlib
import numpy as np
O=Path(__file__).parent
p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r['plan_sha256']==sha(O/'plan.json')
for path,h in p['hashes'].items():assert sha(path)==h
for row in r['rows']:
 data=json.loads(Path(row['source']).read_text())
 records=data if isinstance(data,list) else data.get('rows',[data])
 m=records[row['row_index']].get('measurement',records[row['row_index']].get('training_measurement'))
 assert m['events']==row['events'] and m['total']==row['pooled']
 d=np.array([e['depth'] for e in m['events']]);e=np.array([e['error'] for e in m['events']]);A=np.ones((len(d),1))/e[:,None];coef=np.linalg.lstsq(A,d/e,rcond=None)[0][0];cov=np.linalg.inv(A.T@A)[0,0]
 assert np.isclose(coef,row['matched']['depth'],rtol=1e-12,atol=1e-15) and np.isclose(cov**.5,row['matched']['error'],rtol=1e-12)
 for j,loo in enumerate(row['delete_one']):
  B=np.delete(A,j,axis=0);c=np.linalg.lstsq(B,np.delete(d/e,j),rcond=None)[0][0];assert np.isclose(c,loo['depth'],rtol=1e-12,atol=1e-15)
 checks.append({'tic':row['tic'],'row':row['row_index'],'fit_and_all_omissions':'passed'})
# Deliberately unequal sampling + baseline offsets: pooled estimate is biased;
# a shared transit depth with two event intercepts recovers the known injection.
inside=np.array([1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],dtype=bool)
event=np.array([0]*7+[1]*10);flux=np.where(event==0,1.0,1.02)-.001*inside
X=np.column_stack([event==0,event==1,-inside.astype(float)])
fit=np.linalg.lstsq(X,flux,rcond=None)[0]
assert abs(fit[-1]-.001)<1e-12
pooled=float(flux[~inside].mean()-flux[inside].mean());assert abs(pooled-.001)>.001
out={'status':'passed','measurements':len(checks),'checks':checks,'synthetic':{'true_depth':.001,'intercept_fit':float(fit[-1]),'pooled':pooled},'scope':'Independent least-squares verification of saved event summaries and all omissions, plus deterministic baseline-offset example. Does not revalidate original raw reductions, independent-event assumptions or timing predictions.'}
(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(checks))
