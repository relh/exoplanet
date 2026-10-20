"""Bounded anonymous LCO metadata search. Never follows product URLs."""
import datetime, hashlib, json, pathlib, urllib.request, urllib.parse
R=pathlib.Path('results/lco-archive-metadata-20261013'); D=pathlib.Path('data/lco-archive-metadata-20261013')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
targetpath=pathlib.Path('results/followup-planning-20261013/targets.json')
targets=json.loads(targetpath.read_text())['targets']
plan={'created_utc':now,'scope':'metadata only; no flux, thumbnails, images or spectra','start':'1900-01-01T00:00:00','end':now[:19],'targets':[{k:t[k] for k in ['tic','coordinates']} for t in targets],'target_input_sha256':hashlib.sha256(targetpath.read_bytes()).hexdigest(),'query':'covers POINT at J2016 and linear J2027 positions, public=true, all instruments/types/reduction levels','max_pages_per_query':100,'page_limit':100,'limits':'No claim for proprietary records, missing/incorrect footprints, or nearby-source-only coverage. Any useful metadata requires separate frozen experiment before flux access.'}
(R/'retry-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
manifest=json.loads((R/'sources.json').read_text());summary=[]
def get(url,name):
 p=D/name
 try:
  with urllib.request.urlopen(url,timeout=60) as r: body=r.read(); status=r.status; final=r.url
  p.write_bytes(body); rec={'url':url,'final_url':final,'http_status':status,'path':str(p),'sha256':hashlib.sha256(body).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}; manifest.append(rec); return body
 except Exception as e:
  manifest.append({'url':url,'error':str(e),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}); return None
 finally: (R/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Documentation already retained. Retry follows explicit anonymous limit error.
for t in targets:
 for label,rakey,deckey in [('j2016','ra_j2016_deg','dec_j2016_deg'),('j2027','linear_ra_j2027_deg','linear_dec_j2027_deg')]:
  c=t['coordinates'];params={'covers':f"POINT({c[rakey]} {c[deckey]})",'public':'true','start':plan['start'],'end':plan['end'],'limit':100}
  url='https://archive-api.lco.global/frames/?'+urllib.parse.urlencode(params); rows=[]; counts=[]; status='page_limit'
  for page in range(100):
   body=get(url,f'{t["tic"]}-{label}-limit100-page{page:02d}.json')
   if body is None:status='error';break
   try:x=json.loads(body);counts.append(x['count']);rows+=x['results'];url=x.get('next')
   except Exception as e:status='invalid_response:'+str(e);break
   if not url:status='complete';break
   if urllib.parse.urlparse(url).netloc!='archive-api.lco.global':status='unexpected_next_host';break
  out={'tic':t['tic'],'coordinate_epoch':label,'params':params,'status':status,'page_counts':counts,'retrieved_rows':len(rows),'unique_ids':len({r['id'] for r in rows}),'records':rows}
  (R/f'{t["tic"]}-{label}-limit100-metadata.json').write_text(json.dumps(out,indent=2)+'\n');summary.append({k:v for k,v in out.items() if k!='records'});print(summary[-1],flush=True)
(R/'retry-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
