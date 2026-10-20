from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path(json.loads((out/'files.json').read_text())[0]['path'])
with fits.open(p) as h:
 d=h[1].data;f=np.asarray(d['FLUX']);q=d['QUALITY']==0;rows=[]
 for x in range(f.shape[2]):
  v=f[q,:,x];rows.append({'column':x,'finite_fraction':float(np.isfinite(v).mean()),'zero_fraction':float((v==0).mean()),'median':float(np.nanmedian(v))})
save_json(out/'column-audit.json',{'raw_sha256':sha(p),'script_sha256':sha(Path(__file__)),'quality_zero_rows':int(q.sum()),'columns':rows,'limits':'Descriptive quality-zero raw flux values. Near-zero columns are finite, not NaNs or exactly-zero padding; physical detector cause not established.'})
