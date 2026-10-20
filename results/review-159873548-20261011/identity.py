from pathlib import Path
import requests,csv,io
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;records=[]
for tic in [159873548]:
 q=f"SELECT b.main_id,b.ra,b.dec,i.id FROM basic AS b JOIN ident AS i ON i.oidref=b.oid WHERE b.oid IN (SELECT oidref FROM ident WHERE id='TIC {tic}')";record=dict(tic=tic,query=q,retrieved_utc=now())
 try:
  r=requests.get('https://simbad.cds.unistra.fr/simbad/sim-tap/sync',params=dict(request='doQuery',lang='adql',format='csv',query=q),timeout=45);r.raise_for_status();raw=Path(f'data/targeting/tic{tic}-identifiers.csv');raw.write_bytes(r.content);reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert 'id' in reader.fieldnames;record.update(status='success',url=r.url,path=str(raw),sha256=sha(raw),rows=rows)
 except Exception as exc:record.update(status='error',error=repr(exc))
 records.append(record);print(tic,record['status'],[x['id'] for x in record.get('rows',[]) if 'Gaia DR3' in x['id']],flush=True)
save_json(p/'identity.json',records)
