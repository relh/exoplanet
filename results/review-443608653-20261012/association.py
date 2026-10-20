from pathlib import Path
import requests,json,csv,io
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;rows=[]
for name,query in [('asassn',"SELECT b.main_id,b.ra,b.dec,i.id FROM basic AS b JOIN ident AS i ON i.oidref=b.oid WHERE b.oid IN (SELECT oidref FROM ident WHERE id='ASASSN-V J111352.58-040620.5')")]:
 rec=dict(name=name,query=query,created_utc=now())
 try:
  r=requests.get('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',params=dict(request='doQuery',lang='adql',format='csv',query=query),timeout=45);r.raise_for_status();p=Path('data/targeting/443608653-asassn-20261012.csv');p.write_bytes(r.content);rec.update(status='complete',url=r.url,path=str(p),sha256=sha(p),rows=list(csv.DictReader(io.StringIO(r.text))))
 except Exception as e:rec.update(status='error',error=repr(e))
 rows.append(rec)
q={'service':'Mast.Catalogs.Filtered.Tic.Rows','params':{'columns':'ID,ra,dec,GAIA,TWOMASS','filters':[{'paramName':'ID','values':['443608653']}]},'format':'json','pagesize':100,'page':1};rec=dict(name='tic',query=q,created_utc=now())
try:
 r=requests.post('https://mast.stsci.edu/api/v0/invoke',data={'request':json.dumps(q)},timeout=45);r.raise_for_status();p=Path('data/targeting/443608653-tic-20261012.json');p.write_bytes(r.content);rec.update(status='complete',url=r.url,path=str(p),sha256=sha(p),response=r.json());assert r.json()['status']=='COMPLETE'
except Exception as e:rec.update(status='error',error=repr(e))
rows.append(rec);save_json(O/'association.json',rows);print(rows)
