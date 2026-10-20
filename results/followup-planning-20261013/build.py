"""Reproducible metadata-only packet. No network or photometry access."""
from pathlib import Path
import json,csv,math,hashlib
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,get_body_barycentric
from astropy import units as u
from astropy.constants import c
from astropy.utils import iers
iers.conf.auto_download=False
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
used={}
def read(p):
 q=ROOT/p;used[p]=hashlib.sha256(q.read_bytes()).hexdigest();return json.loads(q.read_text())
def csvread(p):
 q=ROOT/p;used[p]=hashlib.sha256(q.read_bytes()).hexdigest();return list(csv.DictReader(q.open()))
def save(p,x): (OUT/p).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
a=read('results/followup-80387959-qlp90-100-20261009/frozen.json')
b=read('results/expanded-402358350-20261011/frozen-for81.json')
old=read('results/timing-402358350-discovery-20261011/frozen.json')
budget=read('results/paper-host-vetting-20261012/results.json')
gaias=[csvread('results/gaia-80387959-20261009/gaia_source.csv'),read('results/gaia-402358350-scene-20261011/gaia_source.json')]
catalogs=[read('results/neighbors-80387959-20261009/tic-neighbors.json'),read('results/neighbors-402358350-20261011/neighbors.json')]
model_catalogs=[csvread(f'results/triceratops-20261013/{tic}-stars.csv') for tic in [80387959,402358350]]
configs=[(80387959,[{'best':a['best'],'ranges':a['timing_ranges'],'role':'frozen'}],[],[80387965,80387968,80387961,937808821],'5362389543781401216'),(402358350,b['rows'],old['rows'],[1918682563,74037550,402358383,1918682446,1918682448,402358249],'4318715445843296256')]
def bounds(row,n):
 best,r=row['best'],row['ranges'];t0=best['transit_time'];center=t0+n*best['period'];floor=3*r['conditional_epoch_floor_days']
 pts=[ep+round((t0-ep)/p)*p+n*p for p,ep in r['profile_timing_pairs']]
 return min(pts)-floor,max(pts)+floor,max(abs(x-center) for x in pts)+floor

def utc_approx(bjd,coord):
 # Vector dot product uses builtin ephemeris only, no observatory position.
 arrival=Time(bjd,format='jd',scale='tdb')
 unit=coord.cartesian.xyz.value
 for _ in range(4):
  earth=get_body_barycentric('earth',arrival,ephemeris='builtin')
  delay=(np.dot(earth.xyz.to_value(u.m),unit)/c.to_value(u.m/u.s))/86400
  arrival=Time(bjd-delay,format='jd',scale='tdb')
 return arrival.utc.isot
start=Time('2026-10-13',scale='tdb').jd-2457000
end=Time('2027-05-01',scale='tdb').jd-2457000
pack=[];events=[];neighbors=[]
for i,(tic,rows,historical,ids,gid) in enumerate(configs):
 g=next(x for x in gaias[i] if str(x['source_id'])==gid)
 ra,dec=float(g['ra']),float(g['dec']);dt=2027-float(g['ref_epoch'])
 ra27=ra+float(g['pmra'])*dt/(3600000*math.cos(math.radians(dec)))
 de27=dec+float(g['pmdec'])*dt/3600000
 coord=SkyCoord(ra27*u.deg,de27*u.deg)
 best=rows[0]['best'];P=best['period'];t0=best['transit_time'];D=max(r['best']['duration'] for r in rows)
 selected=[]
 for n in range(math.ceil((start-t0)/P),math.ceil((end-t0)/P)):
  center=t0+n*P;bb=[bounds(r,n) for r in rows];lo=min(v[0] for v in bb);hi=max(v[1] for v in bb)
  h=[bounds(r,n) for r in historical]
  full_lo=lo-D/2-1/24;full_hi=hi+D/2+1/24
  e={'tic':tic,'event':n,'center_bjd_tdb':center+2457000,'midpoint_earliest_bjd_tdb':lo+2457000,'midpoint_latest_bjd_tdb':hi+2457000,'midpoint_envelope_hours':(hi-lo)*24,'primary_gate_spread_hours':bb[0][2]*24,'primary_gate_pass':bb[0][2]<best['duration']/2,'full_track_start_bjd_tdb':full_lo+2457000,'full_track_end_bjd_tdb':full_hi+2457000,'full_track_hours':(full_hi-full_lo)*24,'center_geocentric_utc_approx':utc_approx(center+2457000,coord),'full_track_start_geocentric_utc_approx':utc_approx(full_lo+2457000,coord),'full_track_end_geocentric_utc_approx':utc_approx(full_hi+2457000,coord),'historical_discovery_envelope_hours':(max(z[1] for z in h)-min(z[0] for z in h))*24 if h else None}
  events.append(e);selected.append(e)
 nt=[]
 for nid in ids:
  cat=next(x for x in catalogs[i] if int(x['ID'])==nid)
  rr=[x for x in budget['neighbors'] if x['tic']==tic and x['neighbor']==nid]
  z={'target_tic':tic,'neighbor_tic':nid,'catalog_ra_deg':cat['ra'],'catalog_dec_deg':cat['dec'],'catalog_pmra_masyr':cat.get('pmRA'),'catalog_pmdec_masyr':cat.get('pmDEC'),'position_flag':cat.get('POSflag'),'catalog_position_epoch':'not established in this packet; do not label J2016.0','gaia_dr2_id':str(cat.get('GAIA')),'Tmag':cat['Tmag'],'separation_catalog_arcsec':rr[0]['separation_arcsec'],'nominal_min_eclipse_fraction_min':min(x['minimum_eclipse_fraction'] for x in rr),'nominal_min_eclipse_fraction_max':max(x['minimum_eclipse_fraction'] for x in rr),'optimistic_eclipse_fraction_min':min(x['optimistic_lower_bound'] for x in rr)}
  z['illustrative_event_depth_precision_fraction']=z['optimistic_eclipse_fraction_min']/5
  model=next(x for x in model_catalogs[i] if int(x['ID'])==nid)
  z['triceratops_sector']=36 if tic==80387959 else 54
  z['triceratops_nominal_aperture_fraction']=float(model['fluxratio'])
  z['triceratops_nominal_eclipse_fraction']=float(model['tdepth'])
  z['triceratops_requirement_note']='Single-sector Gaussian-response model; not a lower bound, observed eclipse, or the earlier optimistic flux-budget requirement'
  neighbors.append(z);nt.append(z)
 pack.append({'tic':tic,'gaia_dr3_id':gid,'coordinates':{'ra_j2016_deg':ra,'dec_j2016_deg':dec,'pmra_cosdec_masyr':float(g['pmra']),'pmdec_masyr':float(g['pmdec']),'linear_ra_j2027_deg':ra27,'linear_dec_j2027_deg':de27,'method':'linear proper motion; no perspective acceleration or parallax, adequate finder coordinates, not a new astrometric measurement'},'Tmag':next(x['Tmag'] for x in catalogs[i] if int(x['ID'])==tic),'period_days':P,'epoch_btjd_tdb':t0,'duration_hours':best['duration']*24,'event_count':len(selected),'first_event':selected[0],'last_event':selected[-1],'midpoint_envelope_hours_range':[min(e['midpoint_envelope_hours'] for e in selected),max(e['midpoint_envelope_hours'] for e in selected)],'full_track_hours_range':[min(e['full_track_hours'] for e in selected),max(e['full_track_hours'] for e in selected)],'all_pass_original_gate':all(e['primary_gate_pass'] for e in selected),'historical_discovery_envelope_hours_range':[min(e['historical_discovery_envelope_hours'] for e in selected),max(e['historical_discovery_envelope_hours'] for e in selected)] if historical else None,'clock_profiles':rows,'historical_profiles':historical,'priority_neighbors':nt,'classification':'unchanged APC; planning does not add observational evidence'})
# Strip repeated large training datasets; profiles alone sufficient for independent propagation.
for t in pack:
 for key in ['clock_profiles','historical_profiles']:
  t[key]=[{k:r[k] for k in ['best','ranges','role'] if k in r} for r in t[key]]
save('targets.json',{'time_convention':'BJD_TDB = BTJD +2457000; UTC columns approximate geocentric arrival, not site-specific','calibration':'selected-profile envelopes plus heuristic floor, not confidence intervals','targets':pack})
for name,rr in [('events.csv',events),('neighbors.csv',neighbors)]:
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
used['results/followup-planning-20261013/plan.json']=hashlib.sha256((OUT/'plan.json').read_bytes()).hexdigest()
used['results/followup-planning-20261013/build.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
save('provenance.json',{'inputs_sha256':used,'outputs_sha256':{p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ['targets.json','events.csv','neighbors.csv']},'network_access':'none; no new flux or catalog download'})
for t in pack:print(t['tic'],t['event_count'],t['midpoint_envelope_hours_range'],t['full_track_hours_range'],t['all_pass_original_gate'],t['historical_discovery_envelope_hours_range'])
