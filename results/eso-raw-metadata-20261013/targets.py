"""Execute previously frozen metadata-only raw archive cones."""
import json,hashlib,datetime,io
from pathlib import Path
import requests
from astropy.io.votable import parse
O=Path(__file__).parent;D=Path('data/eso-raw-metadata-20261013')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
p=json.loads((O/'plan.json').read_text());s=json.loads((O/'requests.json').read_text())[-1]
cols='dp_id,target,object,ra,dec,ra_pnt,dec_pnt,s_region,date_obs,mjd_obs,exposure,release_date,instrument,telescope,dp_cat,dp_tech,dp_type,ins_mode,slit_path,filter_path,prog_id,prog_title,ob_id,ob_name,tpl_nexp,tpl_expno'.split(',')
assert set(cols)<=set(r['column_name'] for r in s['rows'])
queries=[dict(tic=r['tic'],query=f"SELECT {','.join(cols)} FROM dbo.raw WHERE CONTAINS(s_region,CIRCLE('',{r['ra']},{r['dec']},120./3600.))=1") for r in p['targets']]
assert not (O/'target-plan.json').exists()
save(O/'target-plan.json',dict(created_utc=now(),parent_plan_sha256=sha(O/'plan.json'),schema_sha256=s['sha256'],script_sha256=sha(Path(__file__)),queries=queries,expected_columns=cols,maxrec=10000))
records=[]
for item in queries:
 rec=dict(item,started_utc=now());f=D/f"{item['tic']}.xml"
 try:
  r=requests.get('https://archive.eso.org/tap_obs/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='votable',MAXREC=10000,QUERY=item['query']),timeout=60);f.write_bytes(r.content);rec.update(url=r.url,path=str(f),sha256=sha(f),http_status=r.status_code);r.raise_for_status();v=parse(io.BytesIO(r.content));st=[i.value for i in v.iter_info() if i.name=='QUERY_STATUS'];assert 'OK' in st and not any(x in st for x in ['ERROR','OVERFLOW']),st;t=v.get_first_table().to_table();assert t.colnames==cols;rec.update(status='success',query_status=st,columns=t.colnames,rows=[{k:None if str(row[k])=='--' else str(row[k]) for k in t.colnames} for row in t])
 except Exception as e:rec.update(status='error',error=str(e))
 rec['completed_utc']=now();records.append(rec);save(O/'targets.json',records);print(item['tic'],rec['status'],len(rec.get('rows',[])),flush=True)
