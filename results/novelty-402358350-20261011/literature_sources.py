from pathlib import Path
import requests
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;root=Path('data/catalogs/novelty-402358350-20261011');rows=[]
for name,url in [('paper2018','https://arxiv.org/abs/1710.05803'),('paper2019','https://arxiv.org/abs/1910.00542')]:
 r=dict(name=name,url=url,requested_utc=now())
 try:
  a=requests.get(url,timeout=(15,35));f=root/(name+'.html');f.write_bytes(a.content);r.update(url=a.url,http_status=a.status_code,path=str(f),sha256=sha(f),bytes=len(a.content),retrieved_utc=now());a.raise_for_status();r['status']='retrieved'
 except Exception as exc:r.update(status='error',error=repr(exc))
 rows.append(r);save_json(p/'literature-sources.json',rows)
print([(r['name'],r['status']) for r in rows])
