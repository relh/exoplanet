from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path(json.loads((out/'files.json').read_text())[0]['path']);rows=[]
with fits.open(p) as h:
 d=h[1].data;q=d['QUALITY']==0;f=np.array(d['FLUX'][q],float);e=np.array(d['FLUX_ERR'][q],float)
 for col in range(f.shape[2]):
  a=f[:,:,col];rows.append({'column':col,'min':float(np.nanmin(a)),'max':float(np.nanmax(a)),'median':float(np.nanmedian(a)),'zero_fraction':float(np.mean(a==0)),'nonfinite_fraction':float(np.mean(~np.isfinite(a))),'median_error':float(np.nanmedian(e[:,:,col]))})
save_json(out/'column-audit.json',{'script_sha256':sha(Path(__file__)),'raw_sha256':sha(p),'rows':rows,'limits':'Finite raw pixel values, not zero/NaN padding. Abrupt column boundary is present in archived flux. This audit does not determine its physical or processing cause or identify a transit host.'})
print(rows)
