from pathlib import Path
import requests,json,subprocess
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;D=Path('data')/O.name
q={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL,t_min,t_max','filters':[{'paramName':'target_name','values':['80387959']}]},'format':'json','pagesize':50000,'page':1}
rec=dict(utc=now(),request=q)
try:
 r=requests.post('https://mast.stsci.edu/api/v0/invoke',data={'request':json.dumps(q)},timeout=90);f=D/'products.json';f.write_bytes(r.content);rec.update(url=r.url,path=str(f),sha256=sha(f),http_status=r.status_code);r.raise_for_status();j=r.json();assert j['status']=='COMPLETE';rec.update(status='success',rows=j['data'],paging=j['paging'])
except Exception as e:rec.update(status='error',error=repr(e))
save_json(O/'metadata.json',rec)
paths=subprocess.check_output(['rg','-l','80387959','results','--glob','*.json'],text=True).splitlines();hits=[]
def walk(x,where):
 if isinstance(x,dict):
  if str(x.get('sector',x.get('sequence_number',''))) in ['64','99']:hits.append(dict(file=where,record=x))
  for v in x.values():walk(v,where)
 elif isinstance(x,list):
  for v in x:walk(v,where)
for path in paths:
 if str(O) in path:continue
 try:walk(json.loads(Path(path).read_text()),path)
 except Exception:pass
files=subprocess.check_output(['rg','--files','data','--hidden'],text=True).splitlines();matches=[f for f in files if '80387959' in f and any(s in f for s in ['s64','s99','s0064','s0099'])]
save_json(O/'history-audit.json',dict(utc=now(),results_files_scanned=len(paths),sector64_99_records_in_files_mentioning_target=hits,matching_raw_paths=matches,method='JSON sector records from all result JSON containing TIC; mixed-target files can have other-target sector entries. Also searched all raw paths. Existing opened-sector provenance inspected separately. No observations downloaded by this audit.'))
print(rec['status'],[(x['provenance_name'],x['sequence_number']) for x in rec.get('rows',[])], 'historyhits',len(hits),matches)
