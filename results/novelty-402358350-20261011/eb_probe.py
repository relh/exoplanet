from pathlib import Path
import requests
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;url='https://tessebs.villanova.edu/402358350';raw=Path('data/catalogs/novelty-402358350-20261011/eb-target.html');rec=dict(url=url,started_utc=now())
try:
 r=requests.get(url,timeout=(15,35));raw.write_bytes(r.content);rec.update(url=r.url,http_status=r.status_code,path=str(raw),sha256=sha(raw),bytes=len(r.content),retrieved_utc=now());r.raise_for_status();rec['status']='retrieved_requires_semantic_review'
except Exception as e:rec.update(status='error',error=repr(e))
save_json(p/'eb-probe.json',rec);print(rec)
