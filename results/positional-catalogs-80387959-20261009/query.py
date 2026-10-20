from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from exoplanet.pipeline import fetch,save_json
out=Path(__file__).parent
circle="CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',165.31041473672,-48.6136321332977,0.02))=1"
jobs=[('simbad','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',{'request':'doQuery','lang':'adql','format':'csv','query':f'select top 30 main_id,ra,dec,otype from basic where {circle}'}),('confirmed','https://exoplanetarchive.ipac.caltech.edu/TAP/sync',{'format':'csv','query':f'select pl_name,tic_id,ra,dec,pl_orbper from pscomppars where {circle}'}),('toi','https://exoplanetarchive.ipac.caltech.edu/TAP/sync',{'format':'csv','query':f'select toi,tid,ra,dec,pl_orbper,tfopwg_disp from toi where {circle}'})]
def query(job):
 name,url,params=job
 try:
  p=Path(f'data/targeting/positional-80387959-{name}.csv');meta=fetch(url,p,params);save_json(out/f'{name}-source.json',meta);(out/f'{name}.csv').write_bytes(p.read_bytes())
 except Exception as exc:save_json(out/f'{name}-error.json',{'params':params,'url':url,'error':repr(exc)})
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(query,jobs))
