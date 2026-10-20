from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');r=read(out/'results.json');dp=Path('results/qlp-faint-midradius-single-remaining-20261011/targets/196681132.json');fp=Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json');assert sha(dp)==plan['discovery_sha256'] and sha(fp)==plan['frozen_sha256'] and sha(out/'run.py')==plan['script_sha256'];target=read(dp)['target'];b=read(fp)['best'];assert b==plan['clock']
for row in r['rows']:
 t,y,e,data=load_qlp(target,Path('data'),window=row['window'],bin_minutes=0);cycle=np.rint((t-b['transit_time'])/b['period']).astype(int)
 for p,f in enumerate(row['families']):
  mask=cycle%2==p;actual=fixed_measure(t[mask],y[mask],e[mask],2*b['period'],b['transit_time']+p*b['period'],b['duration']);assert actual==f
 x,z=[f['total'] for f in row['families']];assert row['depth_difference']==x['depth']-z['depth'];assert row['formal_error']==float(np.hypot(x['error'],z['error']));assert row['event_scatter_error']==float(np.hypot(*[f['event_scatter_error'] for f in row['families']]))
 for d in row['data']:assert sha(Path(f"data/qlp/196681132-s{d['sector']:04d}.fits"))==d['source']['sha256']
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'comparison.png'),'status':'Input/raw hashes and all four fixed-clock parity measurements reconstructed; descriptive errors recomputed. Not an independent or calibrated binary test.'});print('four parity measurements verified')
