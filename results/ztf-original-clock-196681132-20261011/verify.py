from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());z=np.load('results/ztf-search-196681132-20261011/processed.npz');t,y,e,g,tr,h=[z[k] for k in ['t','flux','error','oid','training','hmjd']];b=r['clock'];events=np.rint((t-b['transit_time'])/b['period']).astype(int);allmask=np.ones(len(t),bool)
for path,digest in r['inputs'].items():assert sha(Path(path))==digest
def direct(mask,epoch,season=False,times=t,flux=y):
 tt=times[mask];gg=g[mask].astype(str);yy=flux[mask];w=1/e[mask]**2
 if season:gg=np.char.add(np.char.add(gg,':'),np.floor((h[mask]-58000)/365.25).astype(int).astype(str))
 inside=(abs((tt-epoch+b['period']/2)%b['period']-b['period']/2)<b['duration']/2).astype(float);xx=inside.copy();res=yy.copy()
 for oid in np.unique(gg):
  m=gg==oid;xx[m]-=np.average(inside[m],weights=w[m]);res[m]-=np.average(yy[m],weights=w[m])
 information=np.sum(w*xx**2);depth=-np.sum(w*xx*res)/information;err=1/np.sqrt(information);chi=np.sum(w*(res+depth*xx)**2)
 return {'depth':float(depth),'formal_error':float(err),'chi2':float(chi),'n_inside':int(inside.sum())}
checks=[]
for name,mask in [('all',allmask),('early',tr),('later',~tr)]:checks.append((direct(mask,b['transit_time']),r['measurements'][name]))
for oid,row in r['bands'].items():checks.append((direct(g==int(oid),b['transit_time']),row))
checks.append((direct(allmask,b['transit_time'],True),r['object_season_intercepts']))
for row in r['leave_one_event_out']:checks.append((direct(events!=row['excluded_event'],b['transit_time']),row['measurement']))
for row in r['shifted_controls']:checks.append((direct(allmask,b['transit_time']+row['phase_shift']*b['period']),row['measurement']))
for actual,expected in checks:
 for key,value in actual.items():np.testing.assert_allclose(value,expected[key],atol=1e-11)
# Noiseless synthetic depth with unequal per-object offsets checks sign and baseline removal.
inside=abs((t-b['transit_time']+b['period']/2)%b['period']-b['period']/2)<b['duration']/2
synthetic=1+np.searchsorted(np.unique(g),g)*.1-.02*inside
np.testing.assert_allclose(direct(allmask,b['transit_time'],flux=synthetic)['depth'],.02,atol=1e-12)
tdb=np.concatenate([np.load(f'results/ztf-timing-20261011/{oid}-timing.npz')['btjd_assume_tdb'] for oid in [373107100003951,373207100006067,373307100008379]])
sensitivity={name:direct(mask,b['transit_time'],times=tdb) for name,mask in [('all',allmask),('early',tr),('later',~tr)]}
save_json(p/'verification.json',{'verified_measurements':len(checks),'synthetic_group_offset_depth_recovered':.02,'assume_tdb_sensitivity':sensitivity,'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Conditional numerical checks. Timestamp-scale sensitivity does not establish true scale; no calibrated detection probability.'});print('verified',len(checks));print(sensitivity)
