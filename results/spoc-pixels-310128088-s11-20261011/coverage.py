from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent;p=Path('data/pixels/310128088-s0011.fits')
fp=Path('results/qlp-faint-retrospective-gap-followup-20261011/310128088-peak0/frozen.json');f=json.loads(fp.read_text());b=f['best']
with fits.open(p) as h:
 integrity=verify_hdus(p,h);d=h[1].data;t=np.array(d['TIME']);q=np.array(d['QUALITY']);valid=np.isfinite(t)
 t=t[valid];q=q[valid]
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 event=np.rint((t-b['transit_time'])/b['period']).astype(int)
 rows=[]
 for n in np.unique(event):
  inside=(event==n)&(abs(phase)<b['duration']/2);outside=(event==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration'])
  ni=int(sum(inside&(q==0)));no=int(sum(outside&(q==0)))
  rows.append({'event':int(n),'center':b['transit_time']+int(n)*b['period'],'inside_all':int(sum(inside)),'inside_quality_zero':ni,'outside_all':int(sum(outside)),'outside_quality_zero':no,'usable_image_event':ni>=2 and no>=5,'inside_quality_values':np.unique(q[inside]).tolist()})
save_json(out/'coverage.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pixel_sha256':sha(p),'frozen_sha256':sha(fp),'integrity':integrity,'rows':rows,'n_usable':sum(r['usable_image_event'] for r in rows),'limits':'Unchanged image gates: at least2 in-event and5 local baseline cadences, quality0, at least2events. Missing or flagged cadences not evidence against a planet.'})
print(rows)
