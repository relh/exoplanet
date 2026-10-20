from pathlib import Path
import csv,io,json
from concurrent.futures import ThreadPoolExecutor
from exoplanet.pipeline import fetch,sha,save_json,now
O=Path(__file__).parent
queries={'toi':'select tid,toi,pl_orbper,tfopwg_disp from toi where tid=236317267','confirmed':"select tic_id,pl_name,pl_orbper from ps where tic_id='TIC 236317267'"}
def run(item):
 name,q=item;row=dict(name=name,query=q,started_utc=now())
 try:
  p=Path(f'data/targeting/236317267-{name}-20261011.csv');m=fetch('https://exoplanetarchive.ipac.caltech.edu/TAP/sync',p,dict(query=q,format='csv'));r=csv.DictReader(io.StringIO(p.read_text()));rows=list(r);assert r.fieldnames and ('tid' if name=='toi' else 'tic_id') in r.fieldnames;row.update(status='complete',source=m,path=str(p),rows=rows)
 except Exception as exc:row.update(status='error',error=repr(exc))
 return row
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,queries.items()))
save_json(O/'planet-catalogs.json',dict(script_sha256=sha(Path(__file__)),rows=rows,limits='Exact TIC matches in TOI and confirmed tables only; no exhaustive novelty claim.'))
print([(r['name'],r['status'],len(r.get('rows',[]))) for r in rows])
