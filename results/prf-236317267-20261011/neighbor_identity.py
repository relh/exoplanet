from pathlib import Path
import requests,csv,io,json
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;q='select dr2_source_id,dr3_source_id from gaiadr3.dr2_neighbourhood where dr2_source_id=1316214619309621248';record=dict(created_utc=now(),query=q,status='error')
try:
 r=requests.get('https://gea.esac.esa.int/tap-server/tap/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',QUERY=q),timeout=40);r.raise_for_status();p=Path('data/targeting/236317263-dr2-dr3-20261011.csv');p.write_bytes(r.content);record.update(status='complete',url=r.url,path=str(p),sha256=sha(p),rows=list(csv.DictReader(io.StringIO(r.text))))
except Exception as exc:record['error']=repr(exc)
save_json(O/'neighbor-identity.json',record);print(record)
