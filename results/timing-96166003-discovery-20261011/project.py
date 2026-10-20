from pathlib import Path
import json
import numpy as np
from astropy.time import Time
from exoplanet.pipeline import fetch,sha,save_json,now
from exoplanet.followup import prediction_spread
O=Path(__file__).parent;f=json.loads((O/'frozen.json').read_text());rows=[];sources=[]
for sector,start,end in [(19,'2019-11-28','2019-12-23'),(59,'2022-11-26','2022-12-23')]:
 p=Path(f'data/catalogs/timing-96166003-sector{sector}-summary-20261011.html');url=f'https://heasarc.gsfc.nasa.gov/docs/tess/sector{sector}_summary.html';src=fetch(url,p);sources.append(dict(sector=sector,raw=str(p),source=src,dates_utc=[start,end]));times=Time([start,end],scale='utc').jd-2457000
 for row in f['rows']:
  b=row['best'];r=row['ranges'];spread=prediction_spread(times,b,r);cycles=np.rint((times-b['transit_time'])/b['period']);offsets=[]
  for pp,ep in r['profile_timing_pairs']:
   ep+=round((b['transit_time']-ep)/pp)*pp;offsets.extend(abs(ep-b['transit_time']+cycles*(pp-b['period'])))
  manual=max(offsets)+3*r['conditional_epoch_floor_days'];np.testing.assert_allclose(spread,manual);rows.append(dict(sector=sector,window=row['window'],approx_jd_minus2457000=times.tolist(),spread_days=spread,half_duration=b['duration']/2,heuristic_timing_precise=spread<b['duration']/2 and not r['search_boundary_hit']))
save_json(O/'sector-projections.json',dict(created_utc=now(),frozen_sha256=sha(O/'frozen.json'),script_sha256=sha(Path(__file__)),sources=sources,rows=rows,limitation='Calendar-sector endpoints converted from UTC to JD-2457000 only; not barycentric timestamps or actual target coverage. No flux or target observation read. Approximate prediction-envelope illustration only; actual cleaned times must determine future gate. Independent period/epoch propagation arithmetic checked.'))
print(rows)
