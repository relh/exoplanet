from pathlib import Path
import json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;p=Path('results/pixels-378761120-s52-20261010/localization.json');d=json.loads(p.read_text());sky=d['difference_sky']
params={'POS':f"CIRCLE {sky['ra']} {sky['dec']} {15/3600}",'FORMAT':'csv'}
raw=Path('data/catalogs/ztf-378761120-contaminants-20261010.csv')
save_json(out/'request.json',{'utc':now(),'pixel_source_sha256':sha(p),'params':params,'policy':'15arcsec cone around the off-target Sector52 difference centroid; observed TESS period/epoch frozen before downloading ground photometry. Catalog/photometry nonmatches are not proof of absence.'})
meta=fetch('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves',raw,params);save_json(out/'source.json',meta)
print(raw.read_text()[:500],flush=True);print('bytes',meta['bytes'])
