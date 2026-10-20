from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());h=json.loads((p/'heldout.json').read_text())[0];old=json.loads(Path('results/refinement-430216116-20261011/frozen.json').read_text());assert f['best']==old['best'] and f['timing_ranges']==old['timing_ranges'];assert f['discovery_sha256']==sha(Path('results/review-430216116-20261011/discovery.json'))
raw=Path('data/lightcurves/s0071-430216116.fits');assert sha(raw)==h['source']['sha256'];assert old['frozen_utc']<=f['frozen_utc']<=h['started_utc']<=h['source']['retrieved_utc']
t,y,e,star=read_curve(raw);assert star['ticid']==430216116 and star['sector']==71;t,y,e=flatten(t,y,e);b=f['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);assert m==h['measurement'];spread=prediction_spread(t,b,f['timing_ranges']);assert spread==h['timing_spread_days'];assert spread>b['duration']/2 and h['conclusion']=='timing_prediction_inconclusive'
rows=[]
for period,epoch in f['timing_ranges']['profile_timing_pairs']:
 epoch+=round((b['transit_time']-epoch)/period)*period
 total=fixed_measure(t,y,e,period,epoch,b['duration'])['total'];rows.append(dict(period=period,epoch=epoch,total=total))
best=max((r for r in rows if r['total'] is not None),key=lambda r:r['total']['snr'])
save_json(p/'profile-check.json',dict(frozen_sha256=sha(p/'frozen.json'),raw_sha256=sha(raw),rows=rows,best=best,limits='Exploratory maximum over saved discovery timing pairs; no epoch-floor offsets or other durations, correlated trials, not confirmation or complete exclusion.'))
save_json(p/'verification.json',dict(status='passed',original_clock_unchanged=True,freeze_precedes_download=True,raw_hash_and_identity_checked=True,nominal_reconstructed=True,timing_spread_days=spread,profile_pairs_checked=len(rows)))
print('Nominal',m['total'],'profile maximum',best)
