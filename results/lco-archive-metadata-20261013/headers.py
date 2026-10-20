import urllib.request,json,pathlib,hashlib,datetime
R=pathlib.Path('results/lco-archive-metadata-20261013');D=pathlib.Path('data/lco-archive-metadata-20261013');m=json.loads((R/'sources.json').read_text());out=[]
for fid in [22386855,22379518,57992386]:
 u=f'https://archive-api.lco.global/frames/{fid}/headers/'
 with urllib.request.urlopen(u,timeout=60) as r:b=r.read();s=r.status
 p=D/f'headers-{fid}.json';p.write_bytes(b);m.append({'url':u,'http_status':s,'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});x=json.loads(b);out.append({'id':fid,'headers':x});print(fid,str(x)[:1200])
(R/'sources.json').write_text(json.dumps(m,indent=2)+'\n');(R/'headers-metadata.json').write_text(json.dumps(out,indent=2)+'\n')
