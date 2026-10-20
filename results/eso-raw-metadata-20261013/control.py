"""Metadata-only service control at official SN1987A example coordinates."""
import json,datetime,hashlib,io
from pathlib import Path
import requests
from astropy.io.votable import parse
O=Path(__file__).parent;D=Path('data/eso-raw-metadata-20261013')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
cols=json.loads((O/'target-plan.json').read_text())['expected_columns']
q=f"SELECT TOP 3 {','.join(cols)} FROM dbo.raw WHERE CONTAINS(s_region,CIRCLE('',83.86675,-69.269741666,120./3600.))=1"
assert not (O/'control-plan.json').exists()
save(O/'control-plan.json',dict(created_utc=now(),reason='Post-result service control requested by independent review; not a candidate observation or change in candidate decision gates.',source_url='https://archive.eso.org/tap_obs/examples',source_path=str(D/'official_examples.html'),source_sha256=sha(D/'official_examples.html'),example='SN1987A position in example4; same raw table, selected columns and cone predicate as candidates, TOP3 bounds control size only',query=q,script_sha256=sha(Path(__file__)),flux_access=False))
rq=dict(query=q,started_utc=now());f=D/'control.xml'
try:
 r=requests.get('https://archive.eso.org/tap_obs/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='votable',MAXREC=10000,QUERY=q),timeout=60);f.write_bytes(r.content);rq.update(url=r.url,path=str(f),sha256=sha(f),http_status=r.status_code);r.raise_for_status();v=parse(io.BytesIO(r.content));st=[i.value for i in v.iter_info() if i.name=='QUERY_STATUS'];assert 'OK' in st and not set(st)&{'ERROR','OVERFLOW'};t=v.get_first_table().to_table();assert t.colnames==cols;rq.update(status='success',query_status=st,columns=t.colnames,rows=[{k:None if str(row[k])=='--' else str(row[k]) for k in t.colnames} for row in t])
except Exception as e:rq.update(status='error',error=str(e))
rq['completed_utc']=now();save(O/'control.json',rq);print(rq['status'],len(rq.get('rows',[])))
