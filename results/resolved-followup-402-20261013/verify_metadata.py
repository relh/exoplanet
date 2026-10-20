from pathlib import Path
import json,csv,hashlib,math
p=Path(__file__).parent;checks=[]
def ck(x,n):
 assert x,n
 checks.append(n)
for name in ['gaia','gaia_scene','simbad','ztf','cloud-metadata']:
 j=json.loads((p/f'{name}.json').read_text());f=Path(j['path']);ck(hashlib.sha256(f.read_bytes()).hexdigest()==j['sha256'],name+' raw hash')
 if j['status']=='success':
  r=json.loads(f.read_text()) if name=='cloud-metadata' else list(csv.DictReader(f.open()));ck(r==j['rows'],name+' reparse')
 else:ck('ORA-12541' in f.read_text(),'IRSA error retained, not a catalog nonmatch')
plan=json.loads((p/'ztf-plan.json').read_text());ck(hashlib.sha256((p/'ztf-plan.json').read_bytes()).hexdigest()==(p/'ztf-plan.sha256').read_text().strip(),'frozen plan hash')
for f,h in plan['source_hashes'].items():ck(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h,'frozen source hash')
g=plan['source_position'];scene=json.loads((p/'gaia_scene.json').read_text())['rows'];associations=[]
for z in json.loads((p/'cloud-metadata.json').read_text())['rows']:
 distances=[]
 for s in scene:
  a,b=map(math.radians,[float(s['dec']),z['objdec']]);dl=math.radians(float(s['ra'])-z['objra']);d=2*math.asin(math.sqrt(math.sin((a-b)/2)**2+math.cos(a)*math.cos(b)*math.sin(dl/2)**2))*180/math.pi*3600;distances.append((d,s['source_id']))
 distances.sort();ck(distances[0][1]==g['source_id'] and distances[0][0]<1 and distances[1][0]>2,'unique nearest Gaia association');associations.append(dict(oid=z['objectid'],nearest_arcsec=distances[0][0],next_arcsec=distances[1][0]))
st=next(r for r in csv.DictReader(open('results/triceratops-20261013/402358350-stars.csv')) if r['ID']=='74037550');depth=json.load(open('results/triceratops-20261013/402358350-input.json'))['depth'];ck(abs(depth/float(st['fluxratio'])-plan['expected_source_eclipse'])<1e-12,'model eclipse arithmetic')
(p/'metadata-verification.json').write_text(json.dumps(dict(status='passed',checks=checks,n_checks=len(checks),associations=associations),indent=2)+'\n');print('PASS',len(checks))
