"""Read-only independent review of preserved SuperWASP metadata responses."""
from pathlib import Path
from math import sin,cos,asin,sqrt,radians,degrees
from urllib.parse import urlparse,parse_qs
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
DIR=ROOT/'results/superwasp-metadata-20261013';RAW=ROOT/'data/superwasp-metadata-20261013'
checks=0;used={}
def read(p):
 used[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return json.loads(p.read_text())
def check(b):
 global checks
 assert b
 checks+=1
p=read(DIR/'plan.json');queries=read(DIR/'queries.json')
manifest=read(DIR/'manifest.json')
for m in manifest:
 q=ROOT/m['path'];check(hashlib.sha256(q.read_bytes()).hexdigest()==m['sha256'])
for q in queries['queries']:check('0.03333333333333333' in q['query'])
for m in read(DIR/'browser-manifest.json')['files']:
 check(hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()==m['sha256'])
for label in ['80387959','402358350','control']:
 entry=next(m for m in manifest if m['name']=='cone-'+label);check(entry['status']==403)
def sep(a,b,c,d):
 a,b,c,d=map(radians,[a,b,c,d]);return degrees(2*asin(sqrt(sin((b-d)/2)**2+cos(b)*cos(d)*sin((a-c)/2)**2)))*3600
ans={}
for label,ra,dec,expected in [('80387959',p['targets'][0]['ra'],p['targets'][0]['dec'],12),('control',99.97608333333334,35.523805555555555,9)]:
 tables=read(RAW/f'ui-{label}-tables.json');rows=[r for table in tables for r in table if len(r)==14 and r[2].startswith('1SWASP')]
 check(len(rows)==expected)
 parsed=[]
 for r in rows:
  z={'sourceid':r[-1],'separation_arcsec':sep(ra,dec,float(r[3]),float(r[4])),'span_minutes':(float(r[6])-float(r[5]))*1440,'npts':int(r[8]),'scatter_mag':float(r[11])}
  check(z['separation_arcsec']<120);check(z['span_minutes']>0);check(z['npts']>0);parsed.append(z)
 ans[label]=sorted(parsed,key=lambda z:z['separation_arcsec'])
check(ans['80387959'][0]['sourceid']=='1SWASP J110114.50-483649.2')
check(all(r['npts'] in [6,7] and 37<r['span_minutes']<38 for r in ans['80387959']))
check(ans['control'][0]['sourceid']=='1SWASP J063954.26+353125.7')
check(ans['control'][0]['npts']==4965)
r=read(RAW/'ui-402358350-network.json')['data'];q=parse_qs(urlparse(r['url']).query)
check(r['status']==200);check(q['radius']==['120']);check(q['locstr']==[f"{p['targets'][1]['ra']} {p['targets'][1]['dec']}"]);check('No data found in this region.' in r['responseBody'])
summary=read(DIR/'summary.json')
for label in ['80387959','control']:
 check(summary[label]['row_count']==len(ans[label]))
 for row in ans[label]:
  z=next(r for r in summary[label]['rows'] if r['sourceid']==row['sourceid'])
  check(abs(z['separation_j2016_arcsec']-row['separation_arcsec'])<1e-7);check(abs(z['span_minutes']-row['span_minutes'])<1e-7);check(z['npts']==row['npts']);check(z['tm_stddevwrtmed']==row['scatter_mag'])
check(summary['402358350']['row_count']==0)
ans.update({'passed':True,'checks':checks,'reviewed_input_sha256':used,'limits':'Metadata and arithmetic only; no flux, precision calibration, physical exclusion, or exhaustive survey coverage.'})
(OUT/'superwasp-review.json').write_text(json.dumps(ans,indent=2)+'\n')
print('checks',checks,'803 nearest',ans['80387959'][0],'control nearest',ans['control'][0])
