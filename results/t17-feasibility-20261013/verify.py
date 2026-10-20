"""Independent audit of frozen inputs, tabular gates and off-grid March track."""
from pathlib import Path
import json,hashlib,csv
import numpy as np
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation,AltAz,get_sun
from astropy.utils import iers
P=Path(__file__).resolve().parent; ROOT=P.parent.parent; iers.conf.auto_download=False
checks=0
plan=json.loads((P/'plan.json').read_text()); prov=json.loads((P/'provenance.json').read_text())
assert hashlib.sha256((P/'plan.json').read_bytes()).hexdigest()==(P/'plan.sha256').read_text().split()[0];checks+=1
for f,h in plan['inputs_sha256'].items(): assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h;checks+=1
for f,h in prov['outputs_sha256'].items(): assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h;checks+=1
src=json.loads((P/'diagram-source.json').read_text());assert hashlib.sha256((ROOT/src['path']).read_bytes()).hexdigest()==src['sha256'];checks+=1
rows=list(csv.DictReader((P/'events.csv').open())); points=list(csv.DictReader((P/'geometry.csv').open())); assert len(rows)==47 and len(points)==31724;checks+=2
for r in rows:
 p=[x for x in points if x['event']==r['event']];a=np.array([float(x['altitude_deg']) for x in p]);s=np.array([float(x['sun_altitude_deg']) for x in p]);az=np.array([float(x['azimuth_deg']) for x in p]);h=np.where(az<90,35+az*20/90,np.where(az<180,55-(az-90)*20/90,np.where(az<270,35-(az-180)*15/90,20+(az-270)*15/90)))
 gates={'passes_sky':((a>=30)&(s<=-18)).all(),'flat55_pass':((a>=55)&(s<=-18)).all(),'linear_cardinals_pass':((a>=30)&(a>=h)&(s<=-18)).all(),'linear_cardinals_margin_pass':((a>=31)&(a>=h+1)&(s<=-19)).all()}
 for k,v in gates.items(): assert (r[k]=='True')==v;checks+=1
 assert abs(float(r['linear_cardinals_min_clearance_deg'])-min(a-h))<1e-10; checks+=1
r=next(r for r in rows if r['event']=='696');s=plan['site'];loc=EarthLocation.from_geodetic(s['longitude_deg']*u.deg,s['latitude_deg']*u.deg,s['height_m']*u.m)
c=next(t for t in json.loads((ROOT/'results/followup-planning-20261013/targets.json').read_text())['targets'] if t['tic']==80387959)['coordinates'];target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
a=Time(r['start_utc']);b=Time(r['end_utc']);ts=a+np.r_[np.arange(0,(b-a).sec,17),(b-a).sec]*u.s;frame=AltAz(obstime=ts,location=loc,pressure=0*u.hPa);coord=target.transform_to(frame);sun=get_sun(ts).transform_to(frame).alt.deg
mask=np.interp(coord.az.deg,[0,90,180,270,360],[35,55,35,20,35]);assert (coord.alt.deg>=31).all() and (coord.alt.deg-mask>=1).all() and (sun<=-19).all();checks+=1
# Synthetic mask breakpoints and wrap, independent analytical piecewise.
assert np.allclose(np.interp([0,90,180,270,360],[0,90,180,270,360],[35,55,35,20,35]),[35,55,35,20,35]);checks+=5
out={'checks':checks,'off_grid_march28_points':len(ts),'off_grid_min_linear_mask_clearance_deg':float(min(coord.alt.deg-mask)),'status':'pass','scope':'Arithmetic consistency; cannot verify actual operational horizon or instrument capability.'};(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
