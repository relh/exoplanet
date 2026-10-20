from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
raw=Path(json.loads((out/'files.json').read_text())[0]['path'])
paths=[Path(f'results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/354475391-peak{k}/frozen.json') for k in [0,1]]
with fits.open(raw) as h:
 t=np.asarray(h[1].data['TIME']);q=np.asarray(h[1].data['QUALITY']);masks=[]
 for p in paths:
  b=json.loads(p.read_text())['best'];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
  masks.append(np.isfinite(t)&(q==0)&(abs(phase)<b['duration']/2))
r={'script_sha256':sha(Path(__file__)),'raw_sha256':sha(raw),'frozen_hashes':{str(p):sha(p) for p in paths},'quality_zero_inside_counts':[int(m.sum()) for m in masks],'shared_inside_exposures':int((masks[0]&masks[1]).sum()),'limits':'Shared same-sector exposures do not independently validate either period.'}
save_json(out/'window-overlap.json',r);print(r)
