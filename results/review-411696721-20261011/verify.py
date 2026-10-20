from pathlib import Path
import json,csv,numpy as np
from exoplanet.pipeline import sha,read_curve,save_json,now
from exoplanet.search import flatten
p=Path(__file__).parent;src=Path('results/solar-radius-ranks4944-5456-20261011/targets/411696721.json');r=json.loads(src.read_text());plan=json.loads((p/'plan.json').read_text());assert sha(src)==sha(p/'discovery.json')==plan['discovery_sha256'];assert sha(p/'morphology.py')==plan['script_sha256'];assert r['screened_peaks'][0]['flags']==[]
for name in ['results.json','identity.json']:
 for q in json.loads((p/name).read_text()):
  assert q['status']=='success' and sha(Path(q['path']))==q['sha256'];assert list(csv.DictReader(Path(q['path']).open()))==q['rows']
ids={x['id'].strip() for x in json.loads((p/'identity.json').read_text())[0]['rows']};vsx=json.loads((p/'results.json').read_text())[0]['rows'];assert {'TIC 411696721','Gaia DR3 3393787504083851136'}<=ids;assert len(vsx)==1 and vsx[0]['Name'].strip() in ids and vsx[0]['Type'].strip()=='ROT';assert vsx[0]['Period'].strip()==''
arr=np.load(p/'photometry.npz');profiles=json.loads((p/'morphology.json').read_text())['profiles'];count=0
for d in r['data']:
 s=d['sector'];assert s in [43,44];raw=Path(f'data/lightcurves/s{s:04d}-411696721.fits');assert sha(raw)==d['source']['sha256'];t,f,e,star=read_curve(raw);assert star['ticid']==411696721 and star['sector']==s
 for w in [1.5,2.5]:
  tt,y,dy=flatten(t,f,e,window=w);np.testing.assert_allclose(arr[f's{s}w{w}'],np.array([tt,y,dy]),rtol=0,atol=0);b=plan['clock'];phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2
  bins=next(x['bins'] for x in profiles if x['sector']==s and x['window']==w)
  for v in bins:
   k=(phase>=v['lo'])&(phase<v['hi']);assert int(k.sum())==v['n'];sw=sum(1/float(z)**2 for z in dy[k]);mean=sum(float(a)/float(z)**2 for a,z in zip(y[k],dy[k]))/sw;np.testing.assert_allclose([v['flux'],v['error']],[mean,sw**-.5],rtol=1e-12);count+=1
for s in [32,71]:assert not Path(f'data/lightcurves/s{s:04d}-411696721.fits').exists()
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),discovery_products=2,processed_series=4,weighted_bins_checked=count,exact_identity_and_rot_match=True,added_and_reserved_unopened=[32,71],limits='Discovery integrity, preprocessing and independently accumulated bin arithmetic; no full search rerun or astrophysical validation.',artifact_sha256={x.name:sha(x) for x in p.iterdir() if x.is_file() and x.name!='verification.json'}))
