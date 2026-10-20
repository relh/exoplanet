"""Frozen T17 geometry; modeled horizons are explicitly sensitivity cases."""
from pathlib import Path
import csv,json,hashlib,math,warnings
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord,EarthLocation,AltAz,CIRS,get_sun
from astropy.time import Time
from astropy.utils import iers
P=Path(__file__).resolve().parent; ROOT=P.parent.parent
iers.conf.auto_download=False
plan=json.loads((P/'plan.json').read_text())
for f,h in plan['inputs_sha256'].items(): assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
site=plan['site']; loc=EarthLocation.from_geodetic(site['longitude_deg']*u.deg,site['latitude_deg']*u.deg,site['height_m']*u.m)
c=next(t for t in json.loads((ROOT/'results/followup-planning-20261013/targets.json').read_text())['targets'] if t['tic']==80387959)['coordinates']
target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
events=[e for e in csv.DictReader((ROOT/'results/followup-planning-20261013/events.csv').open()) if e['tic']=='80387959']; assert len(events)==47
rows=[]; points=[]; errors=[]
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always')
 for e in events:
  a=Time(e['full_track_start_geocentric_utc_approx'],scale='utc'); b=Time(e['full_track_end_geocentric_utc_approx'],scale='utc'); sec=(b-a).to_value(u.s)
  ts=a+np.linspace(0,sec,math.ceil(sec/plan['grid_seconds'])+1)*u.s
  f=AltAz(obstime=ts,location=loc,pressure=0*u.hPa); sky=target.transform_to(f); alt=sky.alt.deg; az=sky.az.deg; sun=get_sun(ts).transform_to(f).alt.deg
  interp=np.interp(az,[0,90,180,270,360],[35,55,35,20,35]); dark=sun<=-18; base=(alt>=30)&dark
  cirs=target.transform_to(CIRS(obstime=ts,location=loc)); ha=(ts.earth_rotation_angle(longitude=loc.lon)-cirs.ra).rad
  de=cirs.dec.rad; la=loc.lat.rad
  analytical=np.rad2deg(np.arcsin(np.sin(la)*np.sin(de)+np.cos(la)*np.cos(de)*np.cos(ha)))
  # Independent spherical azimuth: north through east.
  anaaz=np.rad2deg(np.arctan2(-np.sin(ha)*np.cos(de),np.sin(de)*np.cos(la)-np.cos(de)*np.sin(la)*np.cos(ha)))%360
  ae=float(np.max(np.abs(analytical-alt))); ze=float(np.max(np.abs((anaaz-az+180)%360-180))); assert ae<.01 and ze<.01
  errors.append((ae,ze))
  row={'event':int(e['event']),'start_utc':a.isot,'end_utc':b.isot,'track_hours':sec/3600,'grid_points':len(ts),'altitude_min_deg':float(alt.min()),'altitude_max_deg':float(alt.max()),'azimuth_min_deg':float(az.min()),'azimuth_max_deg':float(az.max()),'start_altitude_deg':float(alt[0]),'end_altitude_deg':float(alt[-1]),'start_azimuth_deg':float(az[0]),'end_azimuth_deg':float(az[-1]),'sun_max_deg':float(sun.max()),'passes_sky':bool(base.all()),'sky_fraction':float(base.mean()),'flat55_pass':bool(((alt>=55)&dark).all()),'linear_cardinals_pass':bool((base&(alt>=interp)).all()),'linear_cardinals_margin_pass':bool(((alt>=31)&(sun<=-19)&(alt>=interp+1)).all()),'linear_cardinals_min_clearance_deg':float((alt-interp).min())}
  rows.append(row)
  points.extend({'event':row['event'],'utc':t,'altitude_deg':float(al),'azimuth_deg':float(azv),'sun_altitude_deg':float(s),'linear_cardinals_horizon_deg':float(h)} for t,al,azv,s,h in zip(ts.isot,alt,az,sun,interp))
for name,data in [('events.csv',rows),('geometry.csv',points)]:
 with (P/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
summary={'event_count':len(rows),'point_count':len(points),'sky_pass':[r['event'] for r in rows if r['passes_sky']],'flat55_pass':[r['event'] for r in rows if r['flat55_pass']],'linear_cardinals_pass':[r['event'] for r in rows if r['linear_cardinals_pass']],'linear_cardinals_margin_pass':[r['event'] for r in rows if r['linear_cardinals_margin_pass']],'max_independent_altitude_error_deg':max(x[0] for x in errors),'max_independent_azimuth_error_deg':max(x[1] for x in errors),'warnings':sorted(set(str(w.message) for w in caught)),'march28':[r for r in rows if r['start_utc'].startswith('2027-03-28')],'interpretation':'Sensitivity cases, not an authoritative mask or booking feasibility.'}
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'input_plan_sha256':hashlib.sha256((P/'plan.json').read_bytes()).hexdigest(),'outputs_sha256':{x:hashlib.sha256((P/x).read_bytes()).hexdigest() for x in ['build.py','events.csv','geometry.csv','summary.json']}},indent=2)+'\n')
print(json.dumps(summary,indent=2))
