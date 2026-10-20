from pathlib import Path
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;raw=Path('data/qlp/408642351-s0071.fits');rows=[]
with fits.open(raw) as h:
 d=h[1].data
 for label,mask in [('all',np.ones(len(d),bool)),('quality_zero',d['QUALITY']==0)]:
  for col in ['SAP_FLUX','DET_FLUX','DET_FLUX_SML','DET_FLUX_LAG','SYS_RM_FLUX']:
   v=np.asarray(d[col],float);v=v[mask&np.isfinite(v)]
   rows.append({'quality':label,'column':col,'n_finite':len(v),'percentiles_0_1_50_99_100':np.percentile(v,[0,1,50,99,100]).tolist()})
save_json(out/'audit.json',{'utc':now(),'raw_path':str(raw),'raw_sha256':sha(raw),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Descriptive raw-product quantiles only, no transit test or cause attribution. Quality flags retained separately.'})
print(rows)
