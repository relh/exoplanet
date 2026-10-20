from pathlib import Path
import requests,json,hashlib,datetime
p=Path(__file__).parent;plan=p/'epoch-plan.json';assert plan.exists();out=Path('data/web-402358350-20261012/gaia-epoch.csv');r=dict(requested_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),plan_sha256=hashlib.sha256(plan.read_bytes()).hexdigest())
try:
 q=requests.get('https://gea.esac.esa.int/data-server/data',params={'ID':'4318716236117290496','RELEASE':'Gaia DR3','RETRIEVAL_TYPE':'EPOCH_PHOTOMETRY','FORMAT':'CSV','VALID_DATA':'false'},timeout=45);out.write_bytes(q.content);r.update(url=q.url,http_status=q.status_code,path=str(out),sha256=hashlib.sha256(q.content).hexdigest(),bytes=len(q.content),headers=dict(q.headers));q.raise_for_status();r['status']='downloaded_not_yet_parsed'
except Exception as exc:r.update(status='error',error=repr(exc))
(p/'epoch-source.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r.get('bytes'))
