from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,csv,io,hashlib
out=Path(__file__).parent
positions={147673716: (188.336510365983, 60.2815668024246), 193389056: (305.656057019948, 43.7315392624833), 10270202: (267.032379584732, 29.930821535502)}
def get(item):
 tic,(ra,dec)=item
 q=f'''SELECT TOP 100 * FROM "B/vsx/vsx" WHERE 1=CONTAINS(POINT('ICRS',"RAJ2000","DEJ2000"),CIRCLE('ICRS',{ra},{dec},{60/3600}))'''
 rec=dict(tic=tic,query=q,radius_arcsec=60)
 try:
  r=requests.get('https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q),timeout=45);r.raise_for_status();p=Path(f'data/targeting/vsx-solar-{tic}-20261011.csv');p.write_bytes(r.content)
  reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert {'Period','Type','Name'}<=set(reader.fieldnames or [])
  rec.update(status='success',url=r.url,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),rows=rows,columns=reader.fieldnames)
 except Exception as e:rec.update(status='error',error=repr(e))
 return rec
with ThreadPoolExecutor(max_workers=2) as pool:rs=list(pool.map(get,positions.items()))
(out/'results.json').write_text(json.dumps(rs,indent=2)+'\n');print(json.dumps(rs,indent=2))
