from pathlib import Path
import csv,json
import numpy as np
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.search import flatten
O=Path(__file__).parent;src=Path('results/solar-radius-ranks6480-6992-20261011/targets/43676101.json');assert sha(src)==sha(O/'discovery.json');r=json.loads(src.read_text());plan=json.loads((O/'plan.json').read_text());m=json.loads((O/'morphology.json').read_text());assert m['plan_sha256']==sha(O/'plan.json');assert r['screened_peaks'][0]['flags']==[]
for p,h in plan['source_hashes'].items():assert sha(Path(p))==h
for filename in ['results.json','identity.json']:
 for row in json.loads((O/filename).read_text()):
  assert row['status']=='success';assert sha(Path(row['path']))==row['sha256'];assert list(csv.DictReader(Path(row['path']).open()))==row['rows']
ids={x['id'] for x in json.loads((O/'identity.json').read_text())[0]['rows']};assert {'TIC 43676101','Gaia DR3 4548837457047295232'}<=ids
for row in json.loads((O/'planet-catalogs.json').read_text())['rows']:
 assert row['status']=='complete' and sha(Path(row['path']))==row['source']['sha256'];assert list(csv.DictReader(Path(row['path']).open()))==row['rows']
b=plan['clock'];counts=[]
for row in m['rows']:
 arrays=[]
 for data in r['data']:
  p=Path(f"data/lightcurves/s{data['sector']:04d}-43676101.fits");assert sha(p)==data['source']['sha256'];t,f,e,star=read_curve(p);assert star['ticid']==43676101 and star['sector']==data['sector'];arrays.append(flatten(t,f,e,window=row['window']))
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];order=np.argsort(t);t,y,e=t[order],y[order],e[order];z=np.load(O/f"w{row['window']}.npz")
 for key,a in dict(t=t,y=y,e=e).items():np.testing.assert_array_equal(a,z[key])
 ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;ev=np.rint((t-b['transit_time'])/b['period']).astype(int);inside=abs(ph)<b['duration']/2;outside=(abs(ph)>b['duration'])&(abs(ph)<min(3*b['duration'],b['period']/2))
 def check(a,c,saved):
  wi=1/e[a]**2;wo=1/e[c]**2;depth=float(y[c]@wo/wo.sum()-y[a]@wi/wi.sum());err=float(np.sqrt(1/wi.sum()+1/wo.sum()));np.testing.assert_allclose([depth,err,depth/err],[saved['depth'],saved['error'],saved['snr']],atol=1e-10,rtol=1e-8);assert int(a.sum())==saved['n']
 check(inside,outside,row['measurement']['total'])
 for event in row['measurement']['events']:a=ev==event['event'];check(inside&a,outside&a,event)
 counts.append(len(row['measurement']['events']))
for s in [26, 79, 80]:assert not Path(f'data/lightcurves/s{s:04d}-43676101.fits').exists()
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),discovery_products=2,windows=2,event_measurements=counts,additional_and_reserved_caches_absent=[26, 79, 80],scope='Discovery-record/raw/hash/catalog parse/exact identity checks, two raw preprocessing reconstructions, independent precision-sum total and event measurements. No global search rerun, planet probability, source validation or exhaustive novelty claim.'))
print('passed',counts)
