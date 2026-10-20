from pathlib import Path
import json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;p=Path('results/tesscut-314649431-s56-20261010/analysis.json');d=json.loads(p.read_text());sky=dict(zip(['ra','dec'],d['difference_sky']))
params={'POS':f"CIRCLE {sky['ra']} {sky['dec']} {15/3600}",'FORMAT':'csv'}
raw=Path('data/catalogs/ztf-314649431-contaminants-20261010.csv')
save_json(out/'request.json',{'utc':now(),'pixel_source_sha256':sha(p),'params':params,'policy':'15arcsec cone around the off-target Sector56 difference centroid; post-hoc TESS period/epoch fixed before downloading ground photometry. Catalog/photometry nonmatches are not proof of absence.'})
meta=fetch('https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves',raw,params);save_json(out/'source.json',meta)
print(raw.read_text()[:500],flush=True);print('bytes',meta['bytes'])
