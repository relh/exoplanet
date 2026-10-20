from pathlib import Path
import requests,json,csv,io,hashlib
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).parent
queries={'confirmed':"select pl_name,hostname,tic_id,pl_orbper from pscomppars where tic_id='TIC 430216116'",'toi':"select toi,tid,tfopwg_disp,pl_orbper from toi where tid=430216116"}
def run(item):
 name,query=item;rec=dict(catalog=name,query=query)
 try:
  r=requests.get('https://exoplanetarchive.ipac.caltech.edu/TAP/sync',params=dict(query=query,format='csv'),timeout=45);r.raise_for_status();path=Path(f'data/catalogs/430216116-{name}-20261011.csv');path.write_bytes(r.content);reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert ('tic_id' if name=='confirmed' else 'tid') in reader.fieldnames;rec.update(status='success',url=r.url,path=str(path),sha256=hashlib.sha256(r.content).hexdigest(),rows=rows)
 except Exception as exc:rec.update(status='error',error=repr(exc))
 return rec
with ThreadPoolExecutor(2) as pool:rows=list(pool.map(run,queries.items()))
(p/'current_catalogs.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
