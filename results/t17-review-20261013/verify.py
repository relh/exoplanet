"""Read-only independent audit; no new flux or network access."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord,EarthLocation,TETE
from astropy.time import Time
from astropy.utils import iers
iers.conf.auto_download=False
P=Path(__file__).resolve().parent; R=P.parent.parent; D=R/'results/t17-feasibility-20261013'
checks=0
def check(x):
 global checks
 assert x
 checks+=1
plan=json.loads((D/'plan.json').read_text())
for name,sha in plan['inputs_sha256'].items(): check(hashlib.sha256((R/name).read_bytes()).hexdigest()==sha)
check((D/'plan.sha256').read_text().split()[0]==hashlib.sha256((D/'plan.json').read_bytes()).hexdigest())
old={int(x['event']):x for x in csv.DictReader((R/'results/followup-planning-20261013/events.csv').open()) if x['tic']=='80387959'}
rows=list(csv.DictReader((D/'events.csv').open())); geo=list(csv.DictReader((D/'geometry.csv').open()))
check(len(rows)==47); check(set(old)=={int(r['event']) for r in rows}); check(len(geo)==31724)
passes={k:[] for k in ('passes_sky','flat55_pass','linear_cardinals_pass','linear_cardinals_margin_pass')}
for r in rows:
 e=int(r['event']); o=old[e]
 check(r['start_utc']==o['full_track_start_geocentric_utc_approx']);check(r['end_utc']==o['full_track_end_geocentric_utc_approx'])
 g=[x for x in geo if int(x['event'])==e]
 a=np.array([float(x['altitude_deg']) for x in g]); z=np.array([float(x['azimuth_deg']) for x in g]); s=np.array([float(x['sun_altitude_deg']) for x in g]); h=np.interp(z,[0,90,180,270,360],[35,55,35,20,35])
 check(len(g)==int(r['grid_points']));check(np.max(np.diff(Time([x['utc'] for x in g]).jd))*86400<30.01)
 gates={'passes_sky':np.all((a>=30)&(s<=-18)), 'flat55_pass':np.all((a>=55)&(s<=-18)), 'linear_cardinals_pass':np.all((a>=30)&(s<=-18)&(a>=h)), 'linear_cardinals_margin_pass':np.all((a>=31)&(s<=-19)&(a>=h+1))}
 for k,v in gates.items():
  check(v==(r[k]=='True'))
  if v: passes[k].append(e)
check(passes=={'passes_sky':[696],'flat55_pass':[],'linear_cardinals_pass':[696],'linear_cardinals_margin_pass':[696]})
g=[x for x in geo if int(x['event'])==696]; t=Time([x['utc'] for x in g],scale='utc'); site=plan['site'];loc=EarthLocation.from_geodetic(site['longitude_deg']*u.deg,site['latitude_deg']*u.deg,site['height_m']*u.m)
c=json.loads((R/'results/followup-planning-20261013/targets.json').read_text())['targets'][0]['coordinates'];sky=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
# Alternative equinox-based frame + apparent sidereal time; author uses CIO-based CIRS + Earth rotation angle.
eq=sky.transform_to(TETE(obstime=t,location=loc)); ha=(t.sidereal_time('apparent',longitude=loc.lon)-eq.ra).rad; dec=eq.dec.rad; lat=loc.lat.rad
alt=np.rad2deg(np.arcsin(np.sin(lat)*np.sin(dec)+np.cos(lat)*np.cos(dec)*np.cos(ha)))
az=np.rad2deg(np.arctan2(-np.cos(dec)*np.sin(ha),np.cos(lat)*np.sin(dec)-np.sin(lat)*np.cos(dec)*np.cos(ha)))%360
alt_err=np.abs(alt-np.array([float(x['altitude_deg']) for x in g]));az_err=np.abs((az-np.array([float(x['azimuth_deg']) for x in g])+180)%360-180)
check(np.max(alt_err)<.01);check(np.max(az_err)<.01)
out={'checks':checks,'all_checks_pass':True,'scope':'47 unchanged windows and all 31724 stored gate samples; independent TETE/apparent-sidereal spherical coordinates for March28 678-point track. No flux/network.','passes':passes,'independent_track_points':len(g),'max_altitude_error_deg':float(alt_err.max()),'max_azimuth_error_deg':float(az_err.max()),'inputs_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'plan.json',D/'events.csv',D/'geometry.csv',R/'results/t17-access-inquiry-20261013/ASSESSMENT.md']},'limitations':'Both coordinate calculations use Astropy time/ephemeris inputs. Does not verify provider horizon between cardinal points, mount operation, booking or empirical sensitivity.'}
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
