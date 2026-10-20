from pathlib import Path
import json,numpy as np
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;r=json.loads((p/'discovery.json').read_text());b=next(x['best'] for x in r['screened_peaks'] if not x['flags']);z=np.load(p/'photometry.npz');rows=[]
for key in z.files:
 t,y,e=z[key];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);rows.append(dict(series=key,measurement=m))
save_json(p/'per-sector.json',dict(utc=now(),clock=b,photometry_sha256=sha(p/'photometry.npz'),rows=rows))
print([(x['series'],x['measurement']['total']) for x in rows])
