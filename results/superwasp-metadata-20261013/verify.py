import json,pathlib,hashlib,math
R=pathlib.Path(__file__).parent;D=pathlib.Path('data')/R.name
checks=0
def ck(b):
 global checks
 assert b
 checks+=1
for n in ['plan','queries']:
 ck(hashlib.sha256((R/(n+'.json')).read_bytes()).hexdigest()==(R/(n+'.sha256')).read_text().split()[0])
for m in [json.loads((R/'manifest.json').read_text()),json.loads((R/'browser-manifest.json').read_text())['files']]:
 for x in m:
  if 'path'in x:ck(hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()==x['sha256'])
s=json.loads((R/'summary.json').read_text());ck(s['80387959']['row_count']==12);ck(s['control']['row_count']==9);ck(s['402358350']['row_count']==0)
for t in ['80387959','control']:
 for row in s[t]['rows']:ck(row['separation_j2016_arcsec']<=120);ck(row['npts']>0)
for row in s['80387959']['rows']:ck(row['npts']in[6,7]);ck(37.4<row['span_minutes']<37.5)
ck(s['80387959']['nearest']['sourceid']=='1SWASP J110114.50-483649.2');ck(s['control']['nearest']['sourceid']=='1SWASP J063954.26+353125.7');ck(s['control']['nearest']['npts']==4965)
n=json.loads((D/'ui-402358350-network.json').read_text())['data'];ck(n['status']==200);ck('No data found in this region' in n['responseBody']);ck('radius=120' in n['url'])
for x in json.loads((R/'manifest.json').read_text()):
 if x['name'].startswith('cone-'):ck(x['status']==403)
(R/'verification.json').write_text(json.dumps({'checks_passed':checks,'scope':'Local metadata/provenance checks; not survey completeness, photometric sensitivity or planet validation'},indent=2)+'\n');print(checks)
