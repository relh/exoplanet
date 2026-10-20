from pathlib import Path
import requests,json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;p=Path('data/ztf/catalog-route-tables.csv');p.parent.mkdir(exist_ok=True,parents=True)
params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':"SELECT table_name,description FROM TAP_SCHEMA.tables WHERE table_name LIKE 'ztf%'"}
url='https://irsa.ipac.caltech.edu/TAP/sync'
save_json(out/'schema-request.json',{'url':url,'params':params,'started':now(),'timeout_seconds':45})
try:
 r=requests.get(url,params=params,timeout=45);r.raise_for_status();p.write_bytes(r.content)
 save_json(out/'schema-result.json',{'url':r.url,'sha256':sha(p),'path':str(p),'bytes':len(r.content),'finished':now()});print(r.text[:5000])
except Exception as e:save_json(out/'schema-result.json',{'error':repr(e),'finished':now()});print(repr(e))
