from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,csv,io,hashlib
out=Path(__file__).parent
positions={241928959:(297.9869341015965,-21.503148391605208),422626648:(232.12945411477833,-19.12425401415114)}
def query(item):
 tic,(ra,dec)=item
 q=f"SELECT TOP 100 b.oid,b.main_id,b.ra,b.dec,b.otype,b.nbref FROM basic AS b WHERE 1=CONTAINS(POINT('ICRS',b.ra,b.dec),CIRCLE('ICRS',{ra},{dec},{60/3600}))"
 params=dict(request='doQuery',lang='adql',format='csv',query=q);url='https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
 result=dict(tic=tic,query=q,endpoint=url,radius_arcsec=60)
 try:
  r=requests.get(url,params=params,timeout=45);r.raise_for_status();p=Path(f'data/targeting/simbad-{tic}-20261011.csv');p.write_bytes(r.content)
  reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert 'main_id' in reader.fieldnames
  result.update(status='success',url=r.url,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),rows=rows)
 except Exception as e: result.update(status='error',error=repr(e))
 return result
with ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(query,positions.items()))
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
