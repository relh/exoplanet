from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());z=np.load('results/ztf-search-196681132-20261011/processed.npz');t,y,e,g,tr,h=[z[k] for k in ['t','flux','error','oid','training','hmjd']];b=r['clock'];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;cycle=np.rint((t-b['transit_time'])/b['period']).astype(int);primary=abs(phase)<b['duration']/2;design=np.array([primary&(cycle%2==0),primary&(cycle%2==1),abs(abs(phase)-b['period']/2)<b['duration']/2],float).T
for path,digest in r['inputs'].items():assert sha(Path(path))==digest
checks=[(np.ones(len(t),bool),False,r['measurements']['all']),(tr,False,r['measurements']['early']),(~tr,False,r['measurements']['later']),(np.ones(len(t),bool),True,r['measurements']['seasonal'])]+[(g==int(oid),False,row) for oid,row in r['bands'].items()]
for mask,season,expected in checks:
 groups=g[mask].astype(str)
 if season:groups=np.char.add(np.char.add(groups,':'),np.floor((h[mask]-58000)/365.25).astype(int).astype(str))
 w=1/e[mask]**2;yy=y[mask].copy();x=design[mask].copy();assert x.sum(axis=0).astype(int).tolist()==expected['counts']
 for group in np.unique(groups):
  m=groups==group;yy[m]-=np.average(yy[m],weights=w[m]);x[m]-=np.average(x[m],weights=w[m],axis=0)
 info=x.T@(w[:,None]*x)
 if np.linalg.matrix_rank(info)<3:assert expected['status']=='rank_deficient';continue
 cov=np.linalg.inv(info);depth=-cov@(x.T@(w*yy));chi=float(np.sum(w*(yy+x@depth)**2))
 np.testing.assert_allclose(depth,list(expected['depths'].values()),atol=1e-12);np.testing.assert_allclose(cov,expected['covariance_depths'],atol=1e-12);np.testing.assert_allclose(chi,expected['chi2']);deltaerr=np.sqrt(cov[0,0]+cov[1,1]-2*cov[0,1]);np.testing.assert_allclose(deltaerr,expected['difference_formal_error'])
save_json(p/'verification.json',{'status':'Seven multicomponent fits and depth covariance independently reconstructed after projecting out group baselines. Input hashes verified.','artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Numerical verification, not binary classification or calibrated significance.'});print('seven fits verified')
