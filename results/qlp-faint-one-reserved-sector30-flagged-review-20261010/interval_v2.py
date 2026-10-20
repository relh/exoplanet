"""Post-selection concentration of extreme flux deficits, not a false-alarm test."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;parent=Path('results/qlp-faint-one-reserved-sector30-pilot-20261010')
files=[p for p in sorted((parent/'targets').glob('*.json')) if max((x['depth_snr'] for x in json.loads(p.read_text()).get('peaks',[])),default=0)>=100]
save_json(out/'interval-v2-plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'sources':{str(p):sha(p) for p in files},'interval_btjd':[2121,2126],'normalized_flux_cut':.9,'selection':'Corrects an initial visually misread interval [2112,2116] which contained zero samples; its plan/results retained. This interval uses observed timestamps, hence explicitly post-selection. All discovery top-three peaks with formal SNR >=100, chosen after visual inspection of two examples. Native training-only flux. No period refit, new reserved epochs, or calibrated false-alarm probability.'})
rows=[]
for p in files:
 d=json.loads(p.read_text());t,y,e,ev=load_qlp(d['target'],Path('data'),bin_minutes=0)
 low=y<.9;inside=(t>=2121)&(t<=2126)
 with fits.open(Path('data/qlp')/f"{d['tic']}-s0030.fits") as h:
  detector={k:h[0].header.get(k) for k in ['CAMERA','CCD']}
 r={'tic':d['tic'],'ra':d['target']['star']['ra'],'dec':d['target']['star']['dec'],'detector':detector,'n_total':len(t),'n_interval':int(inside.sum()),'n_low':int(low.sum()),'n_low_in_interval':int((low&inside).sum()),'n_low_outside_interval':int((low&~inside).sum()),'minimum_flux':float(y.min()),'minimum_time_btjd':float(t[y.argmin()]),'data':ev}
 rows.append(r);print({k:v for k,v in r.items() if k!='data'})
save_json(out/'interval-v2-results.json',rows)
