from pathlib import Path
import requests,csv,json
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;R=Path('data/web-80387959-20261012')
def query(name,url,q):
 rec=dict(query=q,started_utc=now())
 try:
  r=requests.get(url,params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q),timeout=60);p=R/f'{name}.csv';p.write_bytes(r.content);rec.update(url=r.url,path=str(p),sha256=sha(p),http_status=r.status_code);r.raise_for_status();reader=csv.DictReader(p.open());rows=list(reader);assert reader.fieldnames and '<' not in reader.fieldnames[0];rec.update(status='success',columns=reader.fieldnames,rows=rows)
 except Exception as e:rec.update(status='error',error=repr(e))
 save_json(O/f'{name}.json',rec);print(name,rec['status'],len(rec.get('rows',[])),flush=True)
 return rec
if __name__=='__main__':
 query('identity','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',"select b.main_id,b.ra,b.dec,b.otype,b.oid,i.id from basic b join ident i on b.oid=i.oidref where b.oid in (select oidref from ident where id='TIC 80387959')")
 query('galah-tables','https://datacentral.org.au/vo/tap/sync',"select table_name,description from TAP_SCHEMA.tables where table_name like '%galah%'")
 query('rave-tables','https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',"select table_name,description from TAP_SCHEMA.tables where table_name like 'III/283/%'")
