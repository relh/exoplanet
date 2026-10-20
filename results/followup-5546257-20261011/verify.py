from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());h=json.loads((p/'heldout.json').read_text())[0];assert f['discovery_sha256']==sha(Path('results/review-5546257-20261011/discovery.json'))
raw=Path('data/lightcurves/s0062-5546257.fits');assert sha(raw)==h['source']['sha256'];assert f['frozen_utc']<=h['started_utc']<=h['source']['retrieved_utc']
t,y,e,star=read_curve(raw);assert star['ticid']==5546257 and star['sector']==62;t,y,e=flatten(t,y,e);b=f['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);assert m==h['measurement'];spread=prediction_spread(t,b,f['timing_ranges']);assert spread==h['timing_spread_days'];assert spread>b['duration']/2 and h['conclusion']=='timing_prediction_inconclusive'
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training
discovery=json.loads(Path('results/review-5546257-20261011/discovery.json').read_text());target=discovery['target'];target['training_sectors']=[9,35,36];tt,yy,ee,_=load_training(target,Path('data'));bb,rr=refine_training(tt,yy,ee,f['seed'],seed_baseline=discovery['clean_baseline_days']);assert bb==f['best'] and rr==f['timing_ranges']
rows=[]
for period,epoch in f['timing_ranges']['profile_timing_pairs']:
 epoch+=round((b['transit_time']-epoch)/period)*period
 total=fixed_measure(t,y,e,period,epoch,b['duration'])['total'];rows.append(dict(period=period,epoch=epoch,total=total))
best=max((r for r in rows if r['total'] is not None),key=lambda r:r['total']['snr'])
save_json(p/'profile-check.json',dict(frozen_sha256=sha(p/'frozen.json'),raw_sha256=sha(raw),rows=rows,best=best,limits='Exploratory maximum over saved discovery timing pairs; no epoch-floor offsets or other durations, correlated trials, not confirmation or complete exclusion.'))
save_json(p/'verification.json',dict(status='passed',expanded_training_clock_frozen=True,freeze_precedes_download=True,raw_hash_and_identity_checked=True,nominal_reconstructed=True,timing_spread_days=spread,profile_pairs_checked=len(rows)))
print('Nominal',m['total'],'profile maximum',best)
