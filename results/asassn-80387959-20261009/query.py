from pathlib import Path
import requests
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
url='http://asassn-lb01.ifa.hawaii.edu:9006/lookup_cone/radius0.01_ra165.31041473672_dec-48.6136321332977'
body={'catalog':'master_list','cols':['asas_sn_id','ra_deg','dec_deg','catalog_sources'],'format':'arrow','download':False}
save_json(out/'request.json',{'url':url,'body':body,'utc':now(),'docs':'https://github.com/asas-sn/skypatrol/blob/master/pyasassn/client.py','note':'Public metadata cone query only. HTTP is the official SDK endpoint; transport lacks HTTPS integrity.'})
try:
 r=requests.post(url,json=body,timeout=(15,60));r.raise_for_status();p=Path('data/targeting/asassn-80387959-cone.arrow');p.write_bytes(r.content);save_json(out/'source.json',{'url':r.url,'sha256':sha(p),'bytes':len(r.content),'content_type':r.headers.get('content-type'),'utc':now()});print(r.content[:100])
except Exception as exc:save_json(out/'error.json',{'error':repr(exc),'utc':now()});print(repr(exc))
