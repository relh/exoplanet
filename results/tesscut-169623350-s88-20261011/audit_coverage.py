from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/169623350-peak0/frozen.json');b=json.loads(fp.read_text())['best'];p=Path(json.loads((out/'files.json').read_text())[0]['path'])
with fits.open(p) as h:
 assert h[0].header['SECTOR']==88
 t=np.array(h[1].data['TIME']);q=np.array(h[1].data['QUALITY']);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;finite=np.isfinite(t);ev=np.zeros(len(t),int);ev[finite]=np.rint((t[finite]-b['transit_time'])/b['period']).astype(int);rows=[]
 for n in np.unique(ev[finite&(abs(phase)<b['duration']/2)]):
  inside=finite&(ev==n)&(abs(phase)<b['duration']/2);outside=finite&(ev==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration']);v,c=np.unique(q[inside],return_counts=True)
  rows.append({'event':int(n),'inside':int(inside.sum()),'inside_quality_zero':int((inside&(q==0)).sum()),'outside_quality_zero':int((outside&(q==0)).sum()),'quality_counts':{str(int(x)):int(y) for x,y in zip(v,c)}})
save_json(out/'coverage.json',{'script_sha256':sha(Path(__file__)),'raw_sha256':sha(p),'frozen_sha256':sha(fp),'events':rows,'limits':'Coverage audit only; counts each predicted event without altering selection. No event gates relaxed.'});print(rows)
