from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.transit_model import exposure_times
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['seed'];rows=[]
for w in p['windows']:
 z=np.load(O/f'w{w}.npz');t=z['t'];epoch=b['transit_time']+round((np.median(t)-b['transit_time'])/b['period'])*b['period'];ev=np.rint((t-epoch)/b['period']).astype(int);dt=t-(epoch+ev*b['period']);a=abs(dt)<4*b['duration'];u,c=np.unique(ev[a],return_counts=True);selected=u[c>=8];events=[dict(event=int(n),center=float(epoch+n*b['period']),n_window=int(((ev==n)&a).sum()),n_in_original_box=int(((ev==n)&(abs(dt)<b['duration']/2)).sum())) for n in selected];rows.append(dict(window=w,events=events,exposure_inferred_days=np.unique(np.round(exposure_times(t),6)).tolist()))
save_json(O/'cadence-events.json',dict(script_sha256=sha(Path(__file__)),plan_sha256=sha(O/'plan.json'),rows=rows))
