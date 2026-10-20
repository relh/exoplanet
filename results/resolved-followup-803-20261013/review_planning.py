from pathlib import Path
import json,csv,hashlib,math
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy import units as u
from astropy.utils import iers
iers.conf.auto_download=False
P=Path('results/followup-planning-20261013');F=Path('results/followup-overview-20261013');R=Path(__file__).parent
checks=[]
def ck(name,v): checks.append({'name':name,'pass':bool(v)});assert v,name
p=json.loads((P/'targets.json').read_text());events=list(csv.DictReader((P/'events.csv').open()));f1=json.loads(Path('results/followup-80387959-qlp90-100-20261009/frozen.json').read_text());f2=json.loads(Path('results/expanded-402358350-20261011/frozen-for81.json').read_text());hist=json.loads(Path('results/timing-402358350-discovery-20261011/frozen.json').read_text());orig={80387959:[{'best':f1['best'],'ranges':f1['timing_ranges']}],402358350:f2['rows']};maxround=0
for target in p['targets']:
 tic=target['tic'];rows=orig[tic];ck(str(tic)+' all clock pairs preserved',all(r['ranges']==o['ranges'] and r['best']==o['best'] for r,o in zip(target['clock_profiles'],rows)) and len(rows)==len(target['clock_profiles']))
 if tic==402358350:ck('all historical pairs preserved',all(r['ranges']==o['ranges'] and r['best']==o['best'] for r,o in zip(target['historical_profiles'],hist['rows'])) and len(target['historical_profiles'])==len(hist['rows']))
 coord=target['coordinates'];sky=SkyCoord(coord['linear_ra_j2027_deg']*u.deg,coord['linear_dec_j2027_deg']*u.deg);loc=EarthLocation.from_geocentric(0,0,0,u.m)
 for e in [x for x in events if int(x['tic'])==tic]:
  n=int(e['event']);lo=[];hi=[]
  for row in rows:
   b=row['best'];r=row['ranges'];centers=[ep+(round((b['transit_time']-ep)/period)+n)*period for period,ep in r['profile_timing_pairs']];lo.append(min(centers)-3*r['conditional_epoch_floor_days']);hi.append(max(centers)+3*r['conditional_epoch_floor_days'])
  ck(f'{tic}/{n} envelope no double floor',abs(min(lo)+2457000-float(e['midpoint_earliest_bjd_tdb']))<1e-8 and abs(max(hi)+2457000-float(e['midpoint_latest_bjd_tdb']))<1e-8)
  ck(f'{tic}/{n} full track',abs((max(hi)-min(lo)+max(r['best']['duration'] for r in rows)+2/24)*24-float(e['full_track_hours']))<1e-7)
  ts=Time(e['center_geocentric_utc_approx'],scale='utc',location=loc);bary=ts.tdb+ts.light_travel_time(sky,ephemeris='builtin');err=abs((bary.jd-float(e['center_bjd_tdb']))*86400);maxround=max(maxround,err);ck(f'{tic}/{n} UTC sign/scale',err<.01)
for r in json.loads((F/'field-coordinates.json').read_text()):
 allrows=json.loads((F/'field-coordinates.json').read_text());c=next(x for x in allrows if x['field']==r['field'] and x['tic']==r['field']);a,d,a0,d0=map(math.radians,[r['ra_deg'],r['dec_deg'],c['ra_deg'],c['dec_deg']]);h=math.sin((d-d0)/2)**2+math.cos(d)*math.cos(d0)*math.sin((a-a0)/2)**2;sep=2*math.asin(math.sqrt(h))*180/math.pi*3600;ck(str(r['tic'])+' haversine separation',abs(sep-r['separation_arcsec'])<1e-7);ck(str(r['tic'])+' east sign',(r['east_arcsec']==0 and a==a0) or r['east_arcsec']*(a-a0)>0)
neighbors=list(csv.DictReader((P/'neighbors.csv').open()))
for ident in [80387968,74037550]:
 row=next(x for x in neighbors if int(x['neighbor_tic'])==ident)
 ck(str(ident)+' included with separate model budgets',float(row['optimistic_eclipse_fraction_min'])>0 and float(row['triceratops_nominal_eclipse_fraction'])>0 and 'not a lower bound' in row['triceratops_requirement_note'])
fieldcheck=json.loads((F/'field-verification.json').read_text());ck('chart direct independent verifier',fieldcheck['passed'] and fieldcheck['checks']==26)
res={'status':'passed','checks':checks,'count':len(checks),'utc_roundtrip_max_seconds':maxround,'reviewed_files_sha256':{str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in [P/'build.py',P/'targets.json',P/'events.csv',P/'plan.json',P/'ASSESSMENT.md',P/'neighbors.csv',P/'verification.json',F/'field_chart.py',F/'field-coordinates.json',F/'field-verification.json',F/'fields.png']},'findings':['All saved clock profile pairs retained, historical402profiles explicitly separate.','Three-times heuristic floor applied once per envelope side, matching original prediction_spread policy. Not three sigma.','BJD TDB to geocentric UTC sign and time scale verified through independent forward light_travel_time.','Full track includes widest applicable duration plus one hour baseline each side.','Catalog offsets and east-left field orientation correct. No sky image or host localization inferred.','No observatory schedule claimed. Site visibility and sensitivity explicitly untested.'],'limitations':['Local profiles not complete period aliases or calibrated timing confidence.','Primary timing gate cannot imply futureobservability or astrophysicaltruth.']};(R/'planning-review.json').write_text(json.dumps(res,indent=2)+'\n');print(len(checks),'checks passed; max UTC roundtrip',maxround)
