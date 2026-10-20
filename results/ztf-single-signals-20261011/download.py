from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
import json,csv
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;plans=[]
for tic in [422626648,241928959,196681132]:
 p=Path(f'results/qlp-faint-midradius-single-remaining-20261011/targets/{tic}.json');r=json.loads(p.read_text());s=r['target']['star'];fp=Path(f'results/qlp-faint-midradius-single-review-20261011/{tic}-peak0/frozen.json');plans.append({'tic':tic,'position':[s['ra'],s['dec']],'discovery_sha256':sha(p),'frozen_path':str(fp),'frozen_sha256':sha(fp),'url':'https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?'+urlencode({'POS':f"CIRCLE {s['ra']} {s['dec']} {3/3600}",'FORMAT':'csv'})})
assert not (out/'plan.json').exists();save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'targets':plans,'policy':'3arcsec position query around TIC coordinates, fixed existing TESS clocks before opening. Object identity, quality, blending, timing conventions and prediction uncertainty require checks before any recovery claim. No retiming or period selection on ZTF at this stage.'})
def query(r):
 p=Path(f'data/targeting/ztf-{r["tic"]}-20261011.csv')
 try:
  source=fetch(r['url'],p);reader=csv.DictReader(p.open());rows=list(reader);return {'tic':r['tic'],'status':'downloaded','path':str(p),'source':source,'columns':reader.fieldnames,'n_rows':len(rows)}
 except Exception as exc:return {'tic':r['tic'],'status':'error','error':repr(exc)}
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(query,plans))
save_json(out/'results.json',results);print(results)
