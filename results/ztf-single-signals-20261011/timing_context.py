from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.followup import prediction_spread
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text());rows=[]
for target in plan['targets']:
 p=Path(target['frozen_path']);assert sha(p)==target['frozen_sha256'];f=json.loads(p.read_text());b=f['best'];ranges=f['timing_ranges'];probes=[]
 for days in [30,365,1000,2000]:
  spread=prediction_spread(np.array([b['transit_time']-days]),b,ranges);probes.append({'days_before_reference':days,'conditional_spread_days':spread,'half_duration_days':b['duration']/2,'within_half_duration':spread<b['duration']/2})
 rows.append({'tic':target['tic'],'frozen_sha256':sha(p),'search_boundary_hit':ranges['search_boundary_hit'],'probes':probes})
save_json(out/'timing-context.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Existing conditional box-fit heuristic evaluated at hypothetical lookback times, not actual ZTF epochs or a full timing posterior. Large spread prevents a narrow-window nondetection exclusion; no retiming on external data.'});print(rows)
