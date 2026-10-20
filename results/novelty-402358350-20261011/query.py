from pathlib import Path
import requests,json,csv,io
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;root=Path('data/catalogs/novelty-402358350-20261011');root.mkdir(exist_ok=True);records=[]
def get(name,url,params=None,csv_required=None):
 rec=dict(name=name,requested_utc=now(),url=url,params=params)
 try:
  r=requests.get(url,params=params,timeout=(15,60));raw=root/(name+('.csv' if csv_required else '.html'));raw.write_bytes(r.content);rec.update(http_status=r.status_code,url=r.url,path=str(raw),sha256=sha(raw),bytes=len(r.content),retrieved_utc=now());r.raise_for_status()
  if csv_required:
   reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert set(csv_required)<=set(reader.fieldnames or []);rec.update(rows=([x for x in rows if x['TIC ID'].strip()=='402358350'] if name=='current-ctoi' else rows),row_count=len(rows),columns=reader.fieldnames)
  rec['status']='success'
 except Exception as exc:rec.update(status='error',error=repr(exc))
 records.append(rec);save_json(p/'queries.json',records);print(name,rec['status'],len(rec.get('rows',[])),flush=True)
 return rec
get('current-ctoi','https://exofop.ipac.caltech.edu/tess/download_ctoi.php',dict(sort='ctoi',output='csv'),['TIC ID','Period (days)','CTOI'])
get('target-page','https://exofop.ipac.caltech.edu/tess/target.php',dict(id='402358350'))
q="SELECT table_name,column_name FROM TAP_SCHEMA.columns WHERE table_name IN ('has_ref','ref')"
get('simbad-ref-schema','https://simbad.cds.unistra.fr/simbad/sim-tap/sync',dict(request='doQuery',lang='adql',format='csv',query=q),['table_name','column_name'])
