"""Exploratory held-out checks across the saved training-only timing profile."""
import json
from pathlib import Path
import numpy as np
from exoplanet.pipeline import read_curve,save_json,sha,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
f=json.loads((out/'frozen.json').read_text());b=f['best'];curves={}
for sector in f['heldout_sectors']:
 t,y,e,_=read_curve(Path(f'data/lightcurves/s{sector:04d}-420359321.fits'))
 curves[sector]=flatten(t,y,e)
rows=[]
for p,epoch in f['timing_ranges']['profile_timing_pairs']:
 row={'period':p,'epoch':epoch,'sectors':{}}
 for s,(t,y,e) in curves.items():
  m=fixed_measure(t,y,e,p,epoch,b['duration'])
  row['sectors'][s]={'total':m['total'],'supported_events':m['supported_events']}
 vals=[v['total'] for v in row['sectors'].values() if v['total'] is not None]
 row['combined_depth']=float(sum(v['depth']/v['error']**2 for v in vals)/sum(1/v['error']**2 for v in vals)) if vals else None
 row['combined_error']=float(sum(1/v['error']**2 for v in vals)**-.5) if vals else None
 row['combined_snr']=row['combined_depth']/row['combined_error'] if vals else None
 rows.append(row)
best=max((r for r in rows if r['combined_snr'] is not None),key=lambda r:r['combined_snr'])
save_json(out/'profile-check.json',{'utc':now(),'frozen_sha256':sha(out/'frozen.json'),'n_training_profile_pairs':len(rows),'best_joint':best,'trials':rows,'interpretation':'Post-hoc exploratory scan of already-opened reserved sectors across saved training profile only. Shared epoch/period across sectors, depth free. Maximum SNR is selected, not calibrated significance. Does not replace original inconclusive frozen check; finite profile grid and fixed duration do not exhaust timing/model uncertainty.'})
print('best',best)
