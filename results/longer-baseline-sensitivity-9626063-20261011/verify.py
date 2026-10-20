from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
from exoplanet.transit_model import integrated_box
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());assert sha(p/'run.py')==plan['script_sha256'];assert sha(Path(plan['original']))==plan['original_sha256'];inputs=json.loads((p/'inputs.json').read_text());results=json.loads((p/'results.json').read_text());assert len(results)==12;assert not Path('data/lightcurves/s0079-9626063.fits').exists();counts=[]
for d in inputs:
 assert sha(Path(f"data/lightcurves/s{d['sector']:04d}-9626063.fits"))==d['source']['sha256']
 if d['sector'] in [52,53]:assert plan['created_utc']<=d['source']['retrieved_utc']
for row in results:
 q=row['probe'];parts=[];coverage=[]
 for s in plan['target']['training_sectors']:
  t,f,e,star=read_curve(Path(f'data/lightcurves/s{s:04d}-9626063.fits'));assert star['ticid']==9626063 and star['sector']==s;overlap=integrated_box(t,q['period'],q['epoch'],q['duration'],float(np.median(np.diff(t))));part=flatten(t,f*(1-q['depth']*overlap),e*(1-q['depth']*overlap));parts.append(part);phase=(part[0]-q['epoch']+q['period']/2)%q['period']-q['period']/2;coverage.append(dict(sector=s,n_in=int((abs(phase)<q['duration']/2).sum())))
 t,y,e=[np.concatenate([a[k] for a in parts]) for k in range(3)];assert fixed_measure(t,y,e,q['period'],q['epoch'],q['duration'])==row['measurement'];counts.append(dict(depth=q['depth'],period=q['period'],duration=q['duration'],coverage=coverage))
save_json(p/'verification.json',dict(status='passed',raw_reconstructions=12,hashes_and_identity_checked=True,plan_precedes_new_downloads=True,reserved79_unopened=True,coverage=counts,limits='Reconstruction at known synthetic times, not a blind recovery or complete sensitivity model.'))
print('12 measurements reconstructed')
