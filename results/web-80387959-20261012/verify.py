from pathlib import Path
import csv,json,hashlib,math
O=Path(__file__).parent
checks=0
for p in O.glob('*.json'):
 obj=json.loads(p.read_text());records=obj if isinstance(obj,list) else [obj]
 for rec in records:
  if 'path' not in rec or 'sha256' not in rec:continue
  path=Path(rec['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==rec['sha256'];checks+=1
  if rec.get('status')=='success' and 'rows' in rec:assert list(csv.DictReader(path.open()))==rec['rows']
def rows(name):return list(csv.DictReader(Path('data/web-80387959-20261012',name+'.csv').open()))
a=rows('identity');r=rows('rave-cone')[0];g=rows('rave-gaia-join')[0];rep=rows('rave-repeats')[0];m=rows('rave-madera')[0]
assert {x['oid'] for x in a}=={'7533309'}
assert {'TIC 80387959','Gaia DR3 5362389543781401216','RAVE J110114.5-483649'} <= {x['id'] for x in a}
assert g['Gaiae3']=='5362389543781401216'
assert r['ObsID'].strip()==g['ObsID'].strip()==rep['ObsID1'].strip()==m['ObsID'].strip()=='20100502_1050m50_094'
assert r['ID']==rep['ID']=='J110114.5-483649' and int(rep['Nr'])==int(r['Nrep'])==1
assert all(not rep[f'ObsID{i}'].strip() for i in range(2,14))
def sep(ra,de,ra2,de2):
 ra,de,ra2,de2=map(math.radians,map(float,[ra,de,ra2,de2]));return math.degrees(2*math.asin(math.sqrt(math.sin((de2-de)/2)**2+math.cos(de)*math.cos(de2)*math.sin((ra2-ra)/2)**2)))*3600
p=Path('data/companion-constraints-shortlist-20261012/source.csv');gaia=next(x for x in csv.DictReader(p.open()) if x['source_id']==g['Gaiae3'])
delta=float(gaia['radial_velocity'])-float(r['HRV']);err=math.hypot(float(gaia['radial_velocity_error']),float(r['e_HRV']))
assert not rows('galah-target');box=rows('galah-box');dist=[sep(x['ra'],x['dec'],a[0]['ra'],a[0]['dec']) for x in box];assert all(x>60 for x in dist)
out=dict(raw_records_verified=checks,identity_join='exact SIMBAD aliases and RAVE release Gaia EDR3 crossmatch + ObsID',rave_position_separation_arcsec=sep(r['RAJ2000'],r['DEJ2000'],a[0]['ra'],a[0]['dec']),rave_rv=float(r['HRV']),rave_error=float(r['e_HRV']),gaia_rv=float(gaia['radial_velocity']),gaia_error=float(gaia['radial_velocity_error']),delta_kms=delta,combined_formal_error_kms=err,formal_sigma=delta/err,galah_box_separations_arcsec=dist,prior_gaia_raw=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
