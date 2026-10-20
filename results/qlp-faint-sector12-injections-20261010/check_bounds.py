"""Reconstruct the unchanged period grid for each completed injected trial."""
from pathlib import Path
import json
from astropy.timeseries import BoxLeastSquares
from exoplanet.campaign import DURATIONS
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
a=json.loads((out/'audit.json').read_text());rows=[]
for r in a['rows']:
    p=Path(r['path']);z=json.loads(p.read_text());b=z['clean_baseline_days']
    grid=BoxLeastSquares([0,b],[1,1]).autoperiod(DURATIONS,minimum_period=.5,maximum_period=min(20,b/2.5),frequency_factor=2)
    rows.append({'tic':r['tic'],'period':r['period'],'radius_earth':r['radius_earth'],'baseline_days':b,'nominal_max_period':min(20,b/2.5),'grid_min':float(min(grid)),'grid_max':float(max(grid)),'in_grid':float(min(grid))<=r['period']<=float(max(grid)),'result_sha256':sha(p)})
existing=json.loads((out/'bounds.json').read_text())
assert existing['audit_sha256']==sha(out/'audit.json') and existing['rows']==rows
print('Verified period bounds for',len(rows),'trials;',sum(r['in_grid'] for r in rows),'in grid')
