from pathlib import Path
import json,zipfile,requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;D=Path('data')/O.name;p=json.loads((O/'plan.json').read_text());meta=json.loads((O/'metadata.json').read_text());assert meta['status']=='success';assert all(int(x['sequence_number']) not in [64,99] for x in meta['rows'] if x.get('sequence_number') is not None)
for sector in p['sectors']:
 params=dict(ra=p['ra'],dec=p['dec'],x=15,y=15,units='px',sector=sector);rec=dict(started_utc=now(),plan_sha256=sha(O/'plan.json'),params=params,metadata_sha256=sha(O/'metadata.json'),history_audit_sha256=sha(O/'history-audit.json'));dest=D/f's{sector}.zip'
 try:
  r=requests.get(p['request']['endpoint'],params=params,timeout=(30,180));dest.write_bytes(r.content);rec.update(url=r.url,http_status=r.status_code,path=str(dest),sha256=sha(dest),bytes=len(r.content));r.raise_for_status();files=[]
  with zipfile.ZipFile(dest) as z:
   for name in z.namelist():
    if not name.endswith('.fits'):continue
    path=D/Path(name).name;assert not path.exists();path.write_bytes(z.read(name));files.append(dict(member=name,path=str(path),sha256=sha(path)))
  rec.update(status='downloaded',files=files)
 except Exception as e:rec.update(status='error',error=repr(e))
 rec['finished_utc']=now();save_json(O/f'source-s{sector}.json',rec);print(sector,rec['status'],rec.get('bytes'),flush=True)
