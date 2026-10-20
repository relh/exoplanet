"""Metadata-only six-target availability audit; never fetch flux."""
from pathlib import Path
import json, hashlib, datetime, concurrent.futures
import requests
OUT=Path(__file__).parent
RAW=Path('data')/OUT.name
INPUT=Path('results/companion-constraints-shortlist-20261012/summary.json')
OPENED={80387959:[10,36,37,63,90,100],402358350:[40,41,54,81],241928959:[92],469309982:[9,10,36,37,63,64],96166003:[19,43,44,59],5546257:[9,35,36,62]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def request(name,url,params=None,form=None):
 p=RAW/(name+'.json'); record={'name':name,'url':url,'params':params,'form':form,'started_utc':now()}
 try:
  r=requests.get(url,params=params,timeout=(20,90)) if form is None else requests.post(url,data=form,timeout=(20,90))
  p.write_bytes(r.content);record.update(url=r.url,http_status=r.status_code,path=str(p),sha256=sha(p),finished_utc=now())
  r.raise_for_status();return record,r.json()
 except Exception as exc:record['error']=repr(exc);return record,None
rows=json.loads(INPUT.read_text())['rows']
coords={r['tic']:{'ra':float(r['values']['ra']),'dec':float(r['values']['dec'])} for r in rows if r['tic'] in OPENED}
assert set(coords)==set(OPENED)
save(OUT/'plan.json',{'frozen_utc':now(),'input':str(INPUT),'sha256':sha(INPUT),'opened_sectors':OPENED,'coordinates':coords,'scope':'Current QLP and positional TESScut metadata only, no light curves or image requests. Compare with documented opened sectors. No archive completeness claim; Gaia DR3 coordinates not epoch-propagated.'})
q={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':[str(t) for t in sorted(OPENED)]},{'paramName':'provenance_name','values':['QLP']}]},'format':'json','pagesize':50000,'page':1}
def task(t):return t,request(str(t),'https://mast.stsci.edu/tesscut/api/v0.1/sector',coords[t])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:footprints=list(pool.map(task,OPENED))
manifest=[];results=[]
for t,(rec,d) in footprints:
 manifest.append(rec);v={'tic':t,'opened':OPENED[t],'status':'error'}
 if d is not None and isinstance(d.get('results'),list):
  sectors=sorted(set(int(x['sector']) for x in d['results']));v.update(status='complete',footprint_sectors=sectors,not_documented_opened=sorted(set(sectors)-set(OPENED[t])))
 else:v['error']=rec.get('error','unexpected schema')
 results.append(v)
rec,d=request('qlp','https://mast.stsci.edu/api/v0/invoke',form={'request':json.dumps(q)});manifest.append(rec)
if d is not None and d.get('status')=='COMPLETE' and len(d['data'])==d['paging']['rowsFiltered']:
 for v in results:
  sectors=sorted(set(int(x['sequence_number']) for x in d['data'] if str(x['target_name'])==str(v['tic'])));v.update(qlp_status='complete',qlp_sectors=sectors,qlp_not_documented_opened=sorted(set(sectors)-set(v['opened'])))
else:
 for v in results:v.update(qlp_status='error',qlp_error=rec.get('error',str(d)[:300]))
save(OUT/'manifest.json',manifest);save(OUT/'results.json',{'created_utc':now(),'script_sha256':sha(Path(__file__)),'rows':results});print(json.dumps(results,indent=2))
