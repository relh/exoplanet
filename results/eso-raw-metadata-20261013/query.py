"""Bounded anonymous ESO raw observation metadata; never retrieve flux."""
import json,hashlib,datetime,io
from pathlib import Path
import requests
from astropy.io.votable import parse
O=Path(__file__).parent; D=Path('data/eso-raw-metadata-20261013')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
src=Path('results/companion-constraints-shortlist-20261012/summary.json')
targets=[dict(tic=r['tic'],dr3=r['dr3'],ra=float(r['values']['ra']),dec=float(r['values']['dec'])) for r in json.loads(src.read_text())['rows'] if r['tic'] in [80387959,402358350]]
assert not (O/'plan.json').exists()
save(O/'plan.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),identity_source=str(src),identity_sha256=sha(src),targets=targets,radius_arcsec=120,table='dbo.raw',scope='Anonymous metadata only, all instruments/categories/dates at catalog pointing within cone; no spectrum/image/flux downloads. Retrieve schema first then freeze exact selected columns before target query. Maximum 10000 rows each; overflow or errors are failures, not nonmatches. Hits require physical pointing/slit/footprint checks; empty cone is not a footprint archive exclusion. Gaia J2016 centers not propagated; two arcmin cone allows ordinary proper motion.',decision='Inspect any returned metadata for genuinely discriminating spectroscopy or time series. No candidate disposition changes from absence.'))
records=[]
def request(name,url,params=None):
 rec=dict(name=name,started_utc=now()); p=D/(name+'.xml' if params else name+'.html')
 try:
  r=requests.get(url,params=params,timeout=60);p.write_bytes(r.content);rec.update(url=r.url,http_status=r.status_code,path=str(p),sha256=sha(p));r.raise_for_status()
  if params:
   v=parse(io.BytesIO(r.content));status=[i.value for i in v.iter_info() if i.name=='QUERY_STATUS'];assert 'OK' in status and not any(x in status for x in ['ERROR','OVERFLOW']),status;t=v.get_first_table().to_table();rec.update(query=params['QUERY'],query_status=status,columns=t.colnames,rows=[{k:None if str(row[k])=='--' else str(row[k]) for k in t.colnames} for row in t])
  rec['status']='success'
 except Exception as e:rec.update(status='error',error=str(e))
 rec['completed_utc']=now();records.append(rec);save(O/'requests.json',records);return rec
request('official_programmatic','https://archive.eso.org/cms/eso-data/programmatic-access.html')
request('official_examples','https://archive.eso.org/tap_obs/examples')
params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='votable',MAXREC=10000)
s=request('raw_schema','https://archive.eso.org/tap_obs/sync',dict(params,QUERY="SELECT column_name,datatype,unit,ucd,description FROM TAP_SCHEMA.columns WHERE table_name='dbo.raw'"))
assert s['status']=='success'
print(json.dumps(s['rows'],indent=2))
