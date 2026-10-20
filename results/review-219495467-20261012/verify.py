from pathlib import Path
import json,csv,numpy as np
from exoplanet.pipeline import sha,read_curve,save_json,now
from exoplanet.search import flatten
p=Path(__file__).parent;src=Path('results/solar-radius-ranks6480-6992-20261011/targets/219495467.json');r=json.loads(src.read_text());plan=json.loads((p/'plan.json').read_text());assert sha(src)==sha(p/'discovery.json')==plan['discovery_sha256'];assert sha(p/'morphology.py')==plan['script_sha256'];assert r['screened_peaks'][0]['flags']==[]
for name in ['results.json','identity.json']:
 for q in json.loads((p/name).read_text()):
  assert q['status']=='success' and sha(Path(q['path']))==q['sha256'];assert list(csv.DictReader(Path(q['path']).open()))==q['rows']
ids={x['id'].strip() for x in json.loads((p/'identity.json').read_text())[0]['rows']};vsx=json.loads((p/'results.json').read_text())[0]['rows']
assert ids==set();ti=json.loads((p/'tic-identity.json').read_text());assert ti['status']=='success' and sha(Path(ti['path']))==ti['sha256'];assert str(ti['rows'][0]['GAIA'])=='1382399927901469184';assert vsx[0]['Name'].strip()=='Gaia DR3 1382399927901469184'
arr=np.load(p/'photometry.npz');profiles=json.loads((p/'morphology.json').read_text())['profiles'];count=0
for d in r['data']:
 s=d['sector'];assert s in [24, 25];raw=Path(f'data/lightcurves/s{s:04d}-219495467.fits');assert sha(raw)==d['source']['sha256'];t,f,e,star=read_curve(raw);assert star['ticid']==219495467 and star['sector']==s
 for w in [1.5,2.5]:
  tt,y,dy=flatten(t,f,e,window=w);np.testing.assert_allclose(arr[f's{s}w{w}'],np.array([tt,y,dy]),rtol=0,atol=0);b=plan['clock'];phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2
  bins=next(x['bins'] for x in profiles if x['sector']==s and x['window']==w)
  for v in bins:
   k=(phase>=v['lo'])&(phase<v['hi']);assert int(k.sum())==v['n'];sw=sum(1/float(z)**2 for z in dy[k]);mean=sum(float(a)/float(z)**2 for a,z in zip(y[k],dy[k]))/sw;np.testing.assert_allclose([v['flux'],v['error']],[mean,sw**-.5],rtol=1e-12);count+=1
for s in [50, 51, 52, 77, 78]:assert not Path(f'data/lightcurves/s{s:04d}-219495467.fits').exists()
measure=json.loads((p/'per-sector.json').read_text());assert sha(p/'photometry.npz')==measure['photometry_sha256'];b=measure['clock'];n_measure=0
for case in measure['rows']:
 t,y,e=arr[case['series']];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;event=np.rint((t-b['transit_time'])/b['period']).astype(int);inside=abs(phase)<b['duration']/2;outside=(abs(phase)>b['duration'])&(abs(phase)<min(3*b['duration'],b['period']/2))
 for m,mask in [(case['measurement']['total'],np.ones(len(t),bool))]+[(v,event==v['event']) for v in case['measurement']['events']]:
  im=inside&mask;om=outside&mask;wi=sum(float(v)**-2 for v in e[im]);wo=sum(float(v)**-2 for v in e[om]);mi=sum(float(a)/float(v)**2 for a,v in zip(y[im],e[im]))/wi;mo=sum(float(a)/float(v)**2 for a,v in zip(y[om],e[om]))/wo;depth=mo-mi;error=(1/wi+1/wo)**.5;np.testing.assert_allclose([depth,error,depth/error],[m['depth'],m['error'],m['snr']],rtol=1e-9,atol=1e-12);n_measure+=1
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),discovery_products=2,processed_series=4,weighted_bins_checked=count,independent_fixed_measurements=n_measure,catalog_identity_scope_checked=True,added_and_reserved_unopened=[50, 51, 52, 77, 78],limits='Discovery integrity, preprocessing and independently accumulated bin arithmetic; no full search rerun or astrophysical validation.',artifact_sha256={x.name:sha(x) for x in p.iterdir() if x.is_file() and x.name!='verification.json'}))
