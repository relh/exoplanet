from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.pipeline import sha,save_json,now
from exoplanet.injection_grid import audit
p=Path(__file__).parent;parent=Path('results/solar-radius-pilot-20261011');files=list((parent/'targets').glob('*.json'));rows=sorted([json.loads(f.read_text()) for f in files],key=lambda r:(r['best']['depth_snr'],r['tic']))
selected=[rows[i] for i in [0,7,14]]
assert not (p/'plan.json').exists()
save_json(p/'plan.json',dict(created_utc=now(),selection='Ascending baseline best-peak SNR ranks1,8,15 of16; prior rank16 control retained separately. Deliberate diagnostic strata, not random sampling.',tics=[r['tic'] for r in selected],inputs={str(f):sha(f) for f in files+[Path(__file__),Path('src/exoplanet/injection_grid.py'),Path('src/exoplanet/campaign.py')]},grid=dict(periods=[1.37,4.73,13.13],durations=[.04,.12],depths=[.00025,.00075]),limits='One phase per grid cell, same-sector injection controls only. Reserved sectors remain unopened. No survey completeness claim.'))
with ThreadPoolExecutor(max_workers=3) as pool:result=list(pool.map(lambda r:audit(r,Path('data'),p),selected))
save_json(p/'results.json',result);save_json(p/'run.json',dict(status='complete',finished_utc=now(),counts=[dict(tic=r['tic'],n=len(r['probes']),creditable=sum(q['creditable_recovery'] for q in r['probes']),top3=sum(q['recovered_top3'] for q in r['probes']),errors=sum(q['status']=='error' for q in r['probes'])) for r in result]))
print((p/'run.json').read_text())
