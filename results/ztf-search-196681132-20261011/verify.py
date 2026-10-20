from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;read=lambda q:json.loads(q.read_text());plan=read(p/'plan.json');r=read(p/'results.json');f=read(p/'frozen.json');z=np.load(p/'processed.npz');t,y,e,g,tr=[z[n] for n in ['t','flux','error','oid','training']]
assert sha(p/'run.py')==plan['script_sha256'];assert sha(p/'plan.json')==f['plan_sha256'];assert f['best']==r['best']
for name,digest in plan['inputs'].items():assert sha(Path(name))==digest
assert np.array_equal(tr,z['hmjd']<plan['split_hmjd'])
def direct(mask,clock,flux,record):
 tt=t[mask];gg=g[mask];w=1/e[mask]**2;yy=flux[mask];inside=(abs((tt-clock['transit_time']+clock['period']/2)%clock['period']-clock['period']/2)<clock['duration']/2).astype(float)
 assert int(inside.sum())==record['n_inside']
 zz=inside.copy();res=yy.copy()
 for oid in np.unique(gg):
  m=gg==oid;zz[m]-=np.average(inside[m],weights=w[m]);res[m]-=np.average(yy[m],weights=w[m])
 information=np.sum(w*zz**2)
 if information==0:assert record['status']=='rank_deficient';return
 depth=-np.sum(w*zz*res)/information;error=1/np.sqrt(information)
 np.testing.assert_allclose([depth,error],[record['depth'],record['formal_error']],atol=1e-12)
 residual=res+depth*zz;np.testing.assert_allclose(np.sum(w*residual**2),record['chi2'])
for mask,name in [(tr,'training'),(~tr,'reserved')]:direct(mask,r['best'],y,r[name])
for oid,record in r['reserved_by_oid'].items():direct((~tr)&(g==int(oid)),r['best'],y,record)
b=read(Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json'))['best'];inside=abs((t-b['transit_time']+b['period']/2)%b['period']-b['period']/2)<b['duration']/2
for control in r['injections']:direct(~tr,control['best'],y-control['depth']*inside,control['reserved'])
save_json(p/'verification.json',{'status':'8 group-intercept measurements independently checked with weighted within-group centering; input hashes, split and frozen clock verified.','artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Numerical verification, not independent source validation or calibrated search significance.'});print('verified8 measurements')
