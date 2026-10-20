from pathlib import Path
import json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
n=Path('results/neighbors-207468582-20261010/neighbors.json');rows=json.loads(n.read_text());star=next(r for r in rows if int(r['ID'])==207468583)
f=Path('results/qlp-faint-expanded-followup-20261010/207468582-peak0/frozen.json')
params={'POS':f"CIRCLE {star['ra']} {star['dec']} {45/3600}",'FORMAT':'csv'}
raw=Path('data/catalogs/ztf-207468583-neighborhood-20261010.csv')
save_json(out/'request.json',{'utc':now(),'neighbors_sha256':sha(n),'frozen_sha256':sha(f),'best':json.loads(f.read_text())['best'],'params':params,'policy':'45arcsec cone around suspected neighbor TIC207468583. Fixed original target native TESS ephemeris, no period/phase retuning. Independent ground photometry; retain all OIDs and failures. No catalog match is not evidence of absence.'})
meta=fetch('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves',raw,params);save_json(out/'source.json',meta);print('bytes',meta['bytes'],flush=True)
