from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json
out=Path(__file__).parent

def get(tic):
 d=json.loads(Path(f'results/campaign-qlp-full-pool-20261010/targets/{tic}.json').read_text());s=d['target']['star']
 req={'service':'Mast.Catalogs.Tic.Cone','params':{'ra':s['ra'],'dec':s['dec'],'radius':.06},'format':'json','pagesize':5000,'page':1}
 rows,meta=mast_query(req,Path(f'data/catalogs/qlp-neighbors-{tic}-20261010.json'));save_json(out/f'{tic}-source.json',meta);save_json(out/f'{tic}-neighbors.json',rows)
 target=next(r for r in rows if int(r['ID'])==tic)
 print(tic,'neighbors',len(rows),{k:target.get(k) for k in ['ID','GAIA','HIP','TYC','TWOMASS','plx','d','rad','Teff','pmRA','pmDEC']},flush=True)
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(get,[286607959]))
