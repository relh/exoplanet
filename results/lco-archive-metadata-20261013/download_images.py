import pathlib,json,urllib.request,hashlib,datetime
R=pathlib.Path('results/lco-archive-metadata-20261013');D=pathlib.Path('data/lco-archive-metadata-20261013');plan=json.loads((R/'image-plan.json').read_text());m=json.loads((R/'sources.json').read_text())
for f in plan['allowlist']:
 p=D/f['filename']
 if p.exists():raise RuntimeError('Retain existing file; do not replace')
 with urllib.request.urlopen(f['url'],timeout=90) as response:
  size=response.headers.get('Content-Length');assert size is None or int(size)<=plan['max_bytes_per_file'];b=response.read(plan['max_bytes_per_file']+1);assert len(b)<=plan['max_bytes_per_file'];status=response.status
 p.write_bytes(b);m.append({'url':f['url'],'http_status':status,'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'image_plan_sha256':hashlib.sha256((R/'image-plan.json').read_bytes()).hexdigest()});(R/'sources.json').write_text(json.dumps(m,indent=2)+'\n');print(f['id'],len(b),flush=True)
