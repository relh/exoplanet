from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());count=0;empty=0
for path,digest in r['inputs'].items():assert sha(Path(path))==digest
for target in r['targets']:
 z=np.load(p/f"{target['tic']}-processed.npz");t,y,e,g,h,band,tdb=[z[k] for k in ['t','flux','error','oid','hmjd','band','t_assume_tdb']];b=target['clock'];allmask=np.ones(len(t),bool)
 tests=[(t,mask,0,target['measurements'][name]) for name,mask in [('all',allmask),('early',h<60000),('later',h>=60000)]]+[(t,band==int(k),0,v) for k,v in target['bands'].items()]+[(tdb,allmask,0,target['assume_tdb'])]+[(t,allmask,x['shift_fraction']*b['period'],x['measurement']) for x in target['shifted_controls']]
 for times,mask,offset,expected in tests:
  tt=times[mask];gg=g[mask];w=1/e[mask]**2;yy=y[mask].copy();inside=(abs((tt-b['transit_time']-offset+b['period']/2)%b['period']-b['period']/2)<b['duration']/2).astype(float);xx=inside.copy()
  assert len(tt)==expected['n'] and int(inside.sum())==expected['n_inside']
  for oid in np.unique(gg):
   m=gg==oid;xx[m]-=np.average(inside[m],weights=w[m]);yy[m]-=np.average(yy[m],weights=w[m])
  info=np.sum(w*xx**2)
  if info==0:assert expected['status'] in ['rank_deficient','no_observations'];empty+=1;continue
  depth=-np.sum(w*xx*yy)/info;err=1/np.sqrt(info);chi=np.sum(w*(yy+depth*xx)**2)
  np.testing.assert_allclose([depth,err,chi],[expected['depth'],expected['formal_error'],expected['chi2']],atol=1e-11);count+=1
save_json(p/'verification.json',{'measured_fits_reconstructed':count,'unidentifiable_contrasts_verified':empty,'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Numerical audit, not calibrated signal significance or timing validation.'});print(count,empty)
