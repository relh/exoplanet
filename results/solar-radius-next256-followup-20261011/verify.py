from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;summary=[]
for tic in [396160833,34576133]:
 f=json.loads((p/str(tic)/'frozen.json').read_text());h=json.loads((p/str(tic)/'heldout.json').read_text())[0];assert f['discovery_sha256']==sha(Path(f'results/solar-radius-next256-20261011/targets/{tic}.json'))
 raw=Path(f"data/lightcurves/s{h['sector']:04d}-{tic}.fits");assert sha(raw)==h['source']['sha256'];assert f['frozen_utc']<=h['started_utc']<=h['source']['retrieved_utc']
 t,y,e,star=read_curve(raw);assert int(star['ticid'])==tic and int(star['sector'])==h['sector'];t,y,e=flatten(t,y,e);b=f['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);assert m==h['measurement'];spread=prediction_spread(t,b,f['timing_ranges']);np.testing.assert_allclose(spread,h['timing_spread_days']);assert spread>b['duration']/2 and h['conclusion']=='timing_prediction_inconclusive'
 summary.append(dict(tic=tic,sector=h['sector'],timing_spread_days=spread,duration_days=b['duration'],depth=m['total']['depth'],formal_snr=m['total']['snr']))
save_json(p/'verification.json',dict(status='passed',measurements=summary,freeze_precedes_download=True,limits='Reconstructs fixed predictions; profile range is conditional and not a physical timing posterior.'))
print(summary)
