"""Describe archived training flux without changing discovery preprocessing."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;f=json.loads((out/'frozen.json').read_text());rows=[]
for ev in f['training_data']:
 s=ev['sector'];p=Path(f'data/qlp/405695928-s{s:04d}.fits');assert sha(p)==ev['source']['sha256']
 with fits.open(p) as h:
  assert h[0].header['TICID']==405695928 and h[0].header['SECTOR']==s
  d=h[1].data;q=np.asarray(d['QUALITY']);cols={}
  for name in ['DET_FLUX','KSPSAP_FLUX','SAP_FLUX']:
   if name not in d.names:continue
   x=np.asarray(d[name],float);good=(q==0)&np.isfinite(x)
   cols[name]={'n_finite_quality0':int(good.sum()),'n_nonpositive_quality0':int(np.sum(x[good]<=0)),'percentiles_1_16_50_84_99':np.percentile(x[good],[1,16,50,84,99]).tolist() if good.any() else None}
  rows.append({'sector':s,'raw_sha256':sha(p),'columns':cols})
save_json(out/'flux_audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'limits':'Descriptive archived flux audit, no new detrending, source identification, or calibrated significance. Negative processed flux can indicate extraction/background problems; this alone does not identify their cause.'})
print(rows)
