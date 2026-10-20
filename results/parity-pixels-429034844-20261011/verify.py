from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/429034844-peak1/frozen.json');old=read(fp)['best'];plan=read(out/'plan.json');assert sha(fp)==plan['original_frozen_sha256']
p=Path('data/pixels/429034844-s0070.fits');checks=[];families=[]
with fits.open(p) as hd:
 t=np.asarray(hd[1].data['TIME'],float);q=hd[1].data['QUALITY'];valid=np.isfinite(t);t=t[valid];q=q[valid]
 for parity,expected in [(0,21),(1,22)]:
  f=out/f'frozen-{parity}.json';b=read(f)['best'];assert b['period']==old['period']*2/3;assert b['transit_time']==old['transit_time']+parity*old['period']/3;assert b['duration']==old['duration']
  a=read(out/f'parity-{parity}/localization.json');assert sha(p)==a['source']['sha256'];assert sha(f)==a['frozen_sha256'];assert read(out/f'status-{parity}.json')['exit_code']==0
  nums=np.rint((t-b['transit_time'])/b['period']).astype(int);delta=t-(b['transit_time']+nums*b['period']);inside=(q==0)&(abs(delta)<b['duration']/2);baseline=(q==0)&(abs(delta)>b['duration'])&(abs(delta)<3*b['duration']);rows=[]
  for n in np.unique(nums[inside]):
   ni=int(np.sum(inside&(nums==n)));no=int(np.sum(baseline&(nums==n)))
   if ni>=2 and no>=5:rows.append({'event':int(n),'inside':ni,'outside':no})
  assert [r['event'] for r in rows]==a['event_numbers'];assert len(rows)==expected
  assert np.load(out/f'parity-{parity}/images.npz')['event_differences'].shape[0]==expected
  e=read(out/f'parity-{parity}/event-plots.json')
  for name,h in e['inputs'].items():assert sha(out/f'parity-{parity}'/name)==h
  for path,h in e['plots'].items():assert sha(Path(path))==h
  families.append(inside);checks.append({'parity':parity,'events':rows})
 assert not np.any(families[0]&families[1])
paths=[p for p in out.rglob('*') if p.is_file() and p.name!='verification.json']
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in paths},'checks':checks,'status':'Exact unchanged alias clocks, raw/plot/input hashes, independent coverage enumeration and disjoint parity windows verified. No physical host probability.'})
print('Verified 21/22 events and disjoint windows.')
