"""Bounded public ESO spectrum metadata search; downloads no spectra."""
from pathlib import Path
import json,hashlib,datetime,io
import requests
from astropy.io.votable import parse
O=Path(__file__).parent;D=Path('data/web-spectroscopy-20261012')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
source=Path('results/companion-constraints-shortlist-20261012/summary.json')
targets=[r for r in json.loads(source.read_text())['rows'] if r['tic'] in [80387959,402358350,241928959]]
assert not (O/'plan.json').exists()
save(O/'plan.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),identity_source=str(source),identity_sha256=sha(source),targets=[dict(tic=r['tic'],dr3=r['dr3'],ra=float(r['values']['ra']),dec=float(r['values']['dec'])) for r in targets],radius_arcsec=120,scope='Public ESO ivoa.ObsCore spectrum metadata only; centers Gaia DR3 epoch2016, radius covers proper motion and neighbors; returned rows require association before scientific use. Empty results not complete archival exclusions. No spectra/flux opened.'))
records=[]
for r in targets:
 ra=float(r['values']['ra']);dec=float(r['values']['dec']);tic=r['tic']
 q=f"SELECT target_name,s_ra,s_dec,t_min,t_max,t_exptime,instrument_name,obs_collection,em_res_power,obs_publisher_did,access_url FROM ivoa.ObsCore WHERE dataproduct_type='spectrum' AND 1=CONTAINS(POINT('ICRS',s_ra,s_dec),CIRCLE('ICRS',{ra},{dec},120./3600.))"
 rec=dict(tic=tic,query=q,started_utc=now());p=D/f'{tic}.xml'
 try:
  resp=requests.get('https://archive.eso.org/tap_obs/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='votable',MAXREC=10000,QUERY=q),timeout=50);p.write_bytes(resp.content);rec.update(url=resp.url,path=str(p),sha256=sha(p),http_status=resp.status_code);resp.raise_for_status();v=parse(io.BytesIO(resp.content));statuses=[i.value for i in v.iter_info() if i.name=='QUERY_STATUS'];assert 'ERROR' not in statuses and 'OVERFLOW' not in statuses,statuses;t=v.get_first_table().to_table();assert 's_ra' in t.colnames;rows=[]
  for row in t:
   rows.append({k:None if str(row[k])=='--' else str(row[k]) for k in t.colnames})
  rec.update(status='success',query_status=statuses,columns=t.colnames,rows=rows)
 except Exception as e:rec.update(status='error',error=str(e))
 records.append(rec);save(O/'queries.json',records);print(tic,rec['status'],len(rec.get('rows',[])),flush=True)
u='https://archive.eso.org/tap_obs/examples';resp=requests.get(u,timeout=30);p=D/'examples.html';p.write_bytes(resp.content);save(O/'documentation.json',dict(url=u,retrieved_utc=now(),http_status=resp.status_code,path=str(p),sha256=sha(p)))
