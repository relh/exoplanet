from pathlib import Path
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path('data/qlp/302382075-s0097.fits');rows=[]
with fits.open(p) as h:
 d=h[1].data
 for name in ['SAP_FLUX','DET_FLUX','DET_FLUX_ERR','SYS_RM_FLUX']:
  x=np.asarray(d[name],float);q=(d['QUALITY']==0)&np.isfinite(x);v=x[q]
  rows.append({'column':name,'finite_quality_zero':len(v),'positive':int(np.sum(v>0)),'quantiles_0_1_50_99_100':np.percentile(v,[0,1,50,99,100]).tolist() if len(v) else None})
save_json(out/'qlp-audit.json',{'script_sha256':sha(Path(__file__)),'raw_sha256':sha(p),'columns':rows,'limits':'Broad excursions already exist in QLP SAP/DET columns; their physical/processing cause is not established. Initial interactive check raised IndexError taking percentiles of the empty finite-error column; this version explicitly retains missing values.'})
