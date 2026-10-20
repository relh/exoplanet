from pathlib import Path
import requests,json
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;q={'service':'Mast.Catalogs.Filtered.Tic','params':{'columns':'*','filters':[{'paramName':'ID','values':['219495467']}]},'format':'json','pagesize':10,'page':1};r={'requested_utc':now(),'request':q}
try:
 a=requests.post('https://mast.stsci.edu/api/v0/invoke',data={'request':json.dumps(q)},timeout=45);raw=Path('data/targeting/review219495467-tic-20261012.json');raw.write_bytes(a.content);r.update(url=a.url,path=str(raw),sha256=sha(raw),retrieved_utc=now());a.raise_for_status();o=a.json();assert o['status']=='COMPLETE';assert len(o['data'])==1 and int(o['data'][0]['ID'])==219495467;r.update(status='success',rows=o['data'])
except Exception as e:r.update(status='error',error=repr(e))
save_json(p/'tic-identity.json',r);print(r['status'],[{k:x.get(k) for k in ['ID','GAIA','ra','dec']} for x in r.get('rows',[])])
