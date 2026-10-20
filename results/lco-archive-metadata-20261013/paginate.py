"""Correct API estimated counts by explicit bounded offset pagination."""
import pathlib,json,urllib.request,urllib.parse,hashlib,datetime
R=pathlib.Path('results/lco-archive-metadata-20261013');D=pathlib.Path('data/lco-archive-metadata-20261013');m=json.loads((R/'sources.json').read_text()); summary=[]
(R/'pagination-amendment.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'count=1, count_estimated=true and next=null despite100 rows; cannot trust estimated pagination','method':'Explicit offsets100..9900 until empty page. Retain initial55/100 rows. All fourqueries; no newflux.','prior_summary_status_correction':'retry-summary status complete referred only to next=null; superseded by paginated-summary'},indent=2)+'\n')
for tic in [80387959,402358350]:
 for epoch in ['j2016','j2027']:
  original=json.loads((R/f'{tic}-{epoch}-limit100-metadata.json').read_text());rows=original['records'];params=original['params'];pages=[{'offset':0,'n':len(rows)}];status='cap'
  for offset in range(100,10000,100):
   params['offset']=offset;u='https://archive-api.lco.global/frames/?'+urllib.parse.urlencode(params)
   try:
    with urllib.request.urlopen(u,timeout=60) as response:b=response.read();http=response.status
    p=D/f'{tic}-{epoch}-offset{offset}.json';p.write_bytes(b);x=json.loads(b);m.append({'url':u,'path':str(p),'http_status':http,'sha256':hashlib.sha256(b).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});new=x['results'];pages.append({'offset':offset,'n':len(new),'count':x['count'],'count_estimated':x.get('count_estimated'),'next':x.get('next')});rows+=new
    if not new:status='empty_terminal_page';break
   except Exception as e:m.append({'url':u,'error':str(e)});status='error';break
   finally:(R/'sources.json').write_text(json.dumps(m,indent=2)+'\n')
  clean=[{k:v for k,v in row.items() if k not in ['url','version_set']} for row in rows]
  out={'tic':tic,'epoch':epoch,'status':status,'pages':pages,'n_rows':len(rows),'unique_ids':len({x['id'] for x in rows}),'records':clean}
  (R/f'{tic}-{epoch}-paginated.json').write_text(json.dumps(out,indent=2)+'\n');summary.append({k:v for k,v in out.items() if k!='records'});print(summary[-1],flush=True)
(R/'paginated-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
