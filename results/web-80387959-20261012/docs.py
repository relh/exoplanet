from pathlib import Path
import requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;D=Path('data/web-80387959-20261012');out=[]
for name,url in [('rave-readme','https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/III/283?format=html&tex=true'),('rave-paper','https://arxiv.org/abs/2002.04377'),('galah-release','https://arxiv.org/abs/2409.19858')]:
 rec=dict(name=name,url=url,started_utc=now())
 try:
  r=requests.get(url,timeout=60);p=D/(name+'.html');p.write_bytes(r.content);rec.update(path=str(p),sha256=sha(p),http_status=r.status_code);r.raise_for_status();rec['status']='success'
 except Exception as e:rec.update(status='error',error=repr(e))
 out.append(rec)
save_json(O/'documents.json',out)
