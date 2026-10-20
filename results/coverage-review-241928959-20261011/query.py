"""Metadata only: no epoch-flux or light-curve request."""
from pathlib import Path
import json,csv,io
import requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;D=Path('data/coverage-review-241928959-20261011');D.mkdir(parents=True,exist_ok=True)
q='select source_id,ra,dec,has_epoch_photometry,phot_variable_flag,phot_g_mean_mag,pmra,pmdec from gaiadr3.gaia_source where source_id=6865254022910168320'
rows=[]
for name,url,params in [('gaia','https://gea.esac.esa.int/tap-server/tap/sync',dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q)),('asassn-http-schema','http://asassn-lb01.ifa.hawaii.edu:9006/get_schema',None),('asassn-https-schema','https://asassn-lb01.ifa.hawaii.edu:9006/get_schema',None)]:
 row=dict(name=name,url=url,params=params,started_utc=now())
 try:
  r=requests.get(url,params=params,timeout=(10,25));p=D/f'{name}.response';p.write_bytes(r.content);row.update(http_status=r.status_code,source=dict(url=r.url,path=str(p),sha256=sha(p),bytes=len(r.content),retrieved_utc=now()));r.raise_for_status()
  if name=='gaia':row['rows']=list(csv.DictReader(io.StringIO(r.text)));assert len(row['rows'])==1 and row['rows'][0]['source_id']=='6865254022910168320'
  else:row['schema']=r.json()
  row['status']='complete'
 except Exception as exc:row.update(status='error',error=f'{type(exc).__name__}: {exc}')
 rows.append(row);save_json(O/'metadata.json',dict(script_sha256=sha(Path(__file__)),rows=rows,policy='Metadata only; ASAS-SN schema reachability is not target coverage. Errors are not nonmatches.'))
 print(name,row['status'],row.get('rows',row.get('error')),flush=True)
