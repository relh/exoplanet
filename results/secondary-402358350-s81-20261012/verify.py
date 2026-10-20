from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['clock'];r=json.loads((O/'results.json').read_text());assert r['plan_sha256']==sha(O/'plan.json');assert sha(O/'run.py')==p['script_sha256'];assert sha(Path('results/expanded-402358350-20261011/frozen-for81.json'))==p['frozen_sha256']
for path,h in p['raw_hashes'].items():assert sha(Path(path))==h
count=0
for row in r['rows']:
 t,f,e,star=read_curve(Path('data/lightcurves/s0081-402358350.fits'));assert star['ticid']==402358350 and star['sector']==81;t,y,e=flatten(t,f,e,window=row['window']);epoch=b['transit_time']+(b['period']/2 if row['component']=='half_phase' else 0);ph=(t-epoch+b['period']/2)%b['period']-b['period']/2;inside=abs(ph)<b['duration']/2;outside=(abs(ph)>b['duration'])&(abs(ph)<min(3*b['duration'],b['period']/2));ev=np.rint((t-epoch)/b['period']).astype(int)
 def check(a,c,m):
  global count
  wi=1/e[a]**2;wo=1/e[c]**2;d=y[c]@wo/wo.sum()-y[a]@wi/wi.sum();err=np.sqrt(1/wi.sum()+1/wo.sum());np.testing.assert_allclose([d,err,d/err],[m['depth'],m['error'],m['snr']],atol=1e-10,rtol=1e-8);assert a.sum()==m['n'];count+=1
 check(inside,outside,row['measurement']['total'])
 for m in row['measurement']['events']:a=ev==m['event'];check(inside&a,outside&a,m)
old=Path('results/secondary-sectors-402358350-20261011');op=json.loads((old/'plan.json').read_text());assert op['clock']==b;oldrows=json.loads((old/'results.json').read_text())['rows']
save_json(O/'comparison.json',dict(prior_path=str(old),prior_plan_sha256=sha(old/'plan.json'),prior_results_sha256=sha(old/'results.json'),clock_identical=True,rows=[dict(sector=x['sectors'][0],window=x['window'],component=x['component'],total=x['measurement']['total']) for x in oldrows+r['rows']]))
save_json(O/'verification.json',dict(status='passed',script_sha256=sha(Path(__file__)),independent_total_and_event_measurements=count,raw_hashes_checked=True,prior_clock_identical=True,limits='Raw identity/hash and independent weighted means/errors for81, shared flattening. Prior40/41/54results copied withhashes/identicalclock, not independently reverified here. No calibrated significance.'))
print(count)
