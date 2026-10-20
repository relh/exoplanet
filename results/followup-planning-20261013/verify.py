"""Independent decimal clock propagation and Astropy time conversion checks."""
from pathlib import Path
from decimal import Decimal as Q
import csv,json,hashlib,math
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy import units as u
from astropy.utils import iers
iers.conf.auto_download=False
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
checks=0
def check(x):
 global checks
 assert x
 checks+=1
manifest=json.loads((OUT/'provenance.json').read_text())
for p,h in manifest['inputs_sha256'].items():check(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
for p,h in manifest['outputs_sha256'].items():check(hashlib.sha256((OUT/p).read_bytes()).hexdigest()==h)
packet=json.loads((OUT/'targets.json').read_text()); events=list(csv.DictReader((OUT/'events.csv').open()))
loc=EarthLocation.from_geocentric(0,0,0,u.m);max_rt=0
for target in packet['targets']:
 ev=[e for e in events if int(e['tic'])==target['tic']]
 check(len(ev)==target['event_count'])
 coord=target['coordinates']; sky=SkyCoord(coord['linear_ra_j2027_deg']*u.deg,coord['linear_dec_j2027_deg']*u.deg)
 for event in ev:
  n=int(event['event']);expected=Q(str(target['epoch_btjd_tdb']))+n*Q(str(target['period_days']))+Q(2457000)
  check(abs(float(expected)-float(event['center_bjd_tdb']))<1e-8)
  lows=[];highs=[]
  for row in target['clock_profiles']:
   rr=row['ranges']; t0=Q(str(row['best']['transit_time'])); values=[]
   for period,epoch in rr['profile_timing_pairs']:
    pp=Q(str(period)); ee=Q(str(epoch)); k=round((t0-ee)/pp)
    values.append(ee+(n+k)*pp+Q(2457000))
   f=3*Q(str(rr['conditional_epoch_floor_days']));lows.append(min(values)-f);highs.append(max(values)+f)
  lo,hi=float(min(lows)),float(max(highs));check(abs(lo-float(event['midpoint_earliest_bjd_tdb']))<1e-8);check(abs(hi-float(event['midpoint_latest_bjd_tdb']))<1e-8)
  check(abs((hi-lo)*24-float(event['midpoint_envelope_hours']))<3e-8)
  check(abs(float(event['full_track_hours'])-float(event['midpoint_envelope_hours'])-target['duration_hours']-2)<1e-7)
  for a,b in [('center_geocentric_utc_approx','center_bjd_tdb'),('full_track_start_geocentric_utc_approx','full_track_start_bjd_tdb'),('full_track_end_geocentric_utc_approx','full_track_end_bjd_tdb')]:
   ts=Time(event[a],scale='utc',location=loc);bary=ts.tdb+ts.light_travel_time(sky,ephemeris='builtin');err=abs((bary.jd-float(event[b]))*86400);max_rt=max(max_rt,err);check(err<0.01)
 check([int(e['event']) for e in ev]==list(range(int(ev[0]['event']),int(ev[-1]['event'])+1)))
# Gate checks use published formula independently on original rows.
for target in packet['targets']:
 r=target['clock_profiles'][0];p=r['best']['period'];t=r['best']['transit_time'];floor=r['ranges']['conditional_epoch_floor_days']
 for e in [x for x in events if int(x['tic'])==target['tic']]:
  n=int(e['event']);spread=max(abs((ep+round((t-ep)/pp)*pp-t)+n*(pp-p)) for pp,ep in r['ranges']['profile_timing_pairs'])+3*floor
  check(abs(spread*24-float(e['primary_gate_spread_hours']))<1e-7)
  check((spread<r['best']['duration']/2)==(e['primary_gate_pass']=='True'))
# Neighbor summary reproduces source budgets; no probability or physical exclusion checked.
source=json.loads((ROOT/'results/paper-host-vetting-20261012/results.json').read_text())
for t in packet['targets']:
 model=list(csv.DictReader((ROOT/f"results/triceratops-20261013/{t['tic']}-stars.csv").open()))
 for n in t['priority_neighbors']:
  original=next(x for x in model if int(x['ID'])==n['neighbor_tic'])
  check(n['triceratops_nominal_eclipse_fraction']==float(original['tdepth']))
  check(n['triceratops_nominal_aperture_fraction']==float(original['fluxratio']))
  rr=[x for x in source['neighbors'] if x['tic']==t['tic'] and x['neighbor']==n['neighbor_tic']]
  check(len(rr)==4)
  check(n['optimistic_eclipse_fraction_min']==min(x['optimistic_lower_bound'] for x in rr))
  check(math.isclose(n['illustrative_event_depth_precision_fraction']*5,n['optimistic_eclipse_fraction_min'],rel_tol=1e-14))
result={'status':'pass','checks':checks,'utc_roundtrip_max_seconds':max_rt,'independent_methods':['decimal propagation of saved clock pairs','Astropy light_travel_time forward UTC->BJD_TDB at geocenter','hash and neighbor-budget aggregation checks'],'limits':'Arithmetic only; not confidence calibration, alias completeness, visibility, instrument sensitivity or observational evidence.'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
