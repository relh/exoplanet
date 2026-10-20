from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,math,datetime
from bs4 import BeautifulSoup
O=Path(__file__).parent;load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plan=load(O/'plan.json');qs=load(O/'queries.json')
assert sha(Path(plan['identity_source']))==plan['identity_sha256'];assert sha(O/'query.py')==plan['script_sha256'];assert len(qs)==3
for q in qs:
 assert sha(Path(q['path']))==q['sha256'];root=ET.parse(q['path']).getroot();nodes=list(root.iter());infos=[v.attrib.get('value') for v in nodes if v.tag.endswith('INFO') and v.attrib.get('name')=='QUERY_STATUS'];assert infos==['OK'];fields=[v.attrib.get('name') for v in nodes if v.tag.endswith('FIELD')];assert fields==q['columns'];assert 's_ra' in fields;assert not [v for v in nodes if v.tag.endswith('TR')];assert q['rows']==[] and q['status']=='success'
doc=load(O/'documentation.json');assert sha(Path(doc['path']))==doc['sha256'] and doc['http_status']==200
r=load(O/'rvbank.json');assert sha(Path(r['raw_path']))==r['raw_sha256'];assert not r['parse_errors'];rows=[]
for a in BeautifulSoup(Path(r['raw_path']).read_text(),'html.parser').find_all('a'):
 h=str(a.get('href',''))
 if not(h.startswith('./Ver_02/') and h.endswith('_HARPS_RVBank_ver02.csv')):continue
 f=[c.get_text(' ',strip=True) for c in a.find_parent('tr').find_all(['th','td'],recursive=False)];hh,mm,ss=map(float,f[1].split(':'));dd,dm,ds=map(float,f[2].split(':'));ra=15*(hh+mm/60+ss/3600);dec=(-1 if f[2].startswith('-') else 1)*(abs(dd)+dm/60+ds/3600);rows.append((f[0],ra,dec))
assert len(rows)==r['n_index_rows']
for t,out in zip(plan['targets'],r['targets']):
 sep=[]
 for name,ra,dec in rows:
  a,b,c,d=map(math.radians,[ra,dec,t['ra'],t['dec']]);v=math.sin((b-d)/2)**2+math.cos(b)*math.cos(d)*math.sin((a-c)/2)**2;sep.append(2*math.asin(math.sqrt(min(1,v)))*180/math.pi*3600)
 i=min(range(len(sep)),key=sep.__getitem__);assert rows[i][0]==out['nearest']['name'];assert abs(sep[i]-out['nearest']['separation_arcsec'])<1e-7;assert all(d>120 for d in sep) and out['matches']==[]
(O/'verification.json').write_text(json.dumps(dict(status='passed',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),script_sha256=sha(Path(__file__)),eso_xml_responses=3,rvbank_rows_checked=len(rows),checks='Raw hashes, XML status/schema/row counts, manual sexagesimal coordinates and haversine nearest distances; shared HTML parser. No orbital or completeness inference.'),indent=2)+'\n');print('passed',len(rows))
