from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent

def query(tic):
 p=Path(f'results/qlp-faint-midradius-single-remaining-20261011/targets/{tic}.json');target=json.loads(p.read_text())['target'];star=target['star'];dest=out/f'{tic}.json';params={'ra':star['ra'],'dec':star['dec']}
 try:
  source=fetch('https://mast.stsci.edu/tesscut/api/v0.1/sector',dest,params);d=json.loads(dest.read_text());assert isinstance(d['results'],list)
  sectors=sorted({int(r['sector']) for r in d['results']});return {'tic':tic,'status':'complete','discovery_sha256':sha(p),'params':params,'source':source,'sectors':sectors,'additional_sectors':sorted(set(sectors)-set(target['training_sectors'])),'rows':d['results']}
 except Exception as exc:return {'tic':tic,'status':'error','error':repr(exc)}
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(query,[422626648,241928959,196681132]))
save_json(out/'results.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'TESScut metadata at supplied TIC positions. No new photometry opened. No returned additional footprint is not proof of absence in all missions/products or future releases. Proper motion not propagated.'});print(rows)
