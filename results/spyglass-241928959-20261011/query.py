from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,hashlib,csv,io
out=Path(__file__).parent
queries={f'table{i}':f'''SELECT TOP 100 * FROM "J/ApJ/917/23/table{i}" WHERE 1=CONTAINS(POINT('ICRS',"RA_ICRS","DE_ICRS"),CIRCLE('ICRS',297.987022155552,-21.5031691342776,0.0166666666666667))''' for i in (1,2)}
def get(item):
 name,q=item;rec=dict(name=name,query=q)
 try:
  r=requests.get('https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q),timeout=45);r.raise_for_status();p=Path(f'data/targeting/spyglass-241928959-{name}.csv');p.write_bytes(r.content)
  rec.update(url=r.url,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),rows=list(csv.DictReader(io.StringIO(r.text))),status='success')
 except Exception as e:rec.update(status='error',error=repr(e))
 return rec
with ThreadPoolExecutor(max_workers=2) as pool:rs=list(pool.map(get,queries.items()))
(out/'results.json').write_text(json.dumps(rs,indent=2)+'\n');print(json.dumps(rs,indent=2))
