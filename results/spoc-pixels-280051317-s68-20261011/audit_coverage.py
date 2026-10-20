from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent;raw=Path('data/pixels/280051317-s0068.fits');meta=json.loads(raw.with_suffix('.fits.json').read_text());assert sha(raw)==meta['sha256']
frozen=Path('results/qlp-faint-midradius-remaining-three-followup-20261011/280051317-peak1/frozen.json');b=json.loads(frozen.read_text())['best'];p,e,d=(b[k] for k in ['period','transit_time','duration'])
with fits.open(raw) as h:
 assert h[0].header['TICID']==280051317 and h[0].header['SECTOR']==68
 integrity=verify_hdus(raw,h);a=h[1].data;good=np.isfinite(a['TIME']);t=np.array(a['TIME'][good]);q=np.array(a['QUALITY'][good]);phase=(t-e+p/2)%p-p/2;event=np.rint((t-e)/p).astype(int);rows=[]
 for n in np.unique(event[abs(phase)<d/2]):
  inside=(event==n)&(abs(phase)<d/2);outside=(event==n)&(abs(phase)>d)&(abs(phase)<3*d);values,counts=np.unique(q[inside],return_counts=True)
  rows.append({'event':int(n),'n_inside':int(inside.sum()),'inside_quality_counts':{str(int(v)):int(c) for v,c in zip(values,counts)},'n_inside_quality_zero':int((inside&(q==0)).sum()),'n_outside_quality_zero':int((outside&(q==0)).sum())})
 save_json(out/'coverage.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(frozen),'source':meta,'integrity':integrity,'events':rows,'limits':'Counts at the frozen ephemeris under the existing image-event gate; missing/flagged events are not nondetections.'})
 print(rows)
