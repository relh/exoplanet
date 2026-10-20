"""Recheck retained hashes and all passing windows at an independent 31-second grid."""
import csv,json,hashlib,warnings,math
from pathlib import Path
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz,get_sun
from astropy.time import Time
from astropy.utils import iers
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
iers.conf.auto_download=False
manifest=json.loads((P/'provenance.json').read_text())
for f,h in manifest['inputs_sha256'].items(): assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
for f,h in manifest['generated_sha256'].items(): assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
rows=list(csv.DictReader((P/'site-events.csv').open())); assert len(rows)==320
sites={s['code']:s for s in json.loads((P/'sites.json').read_text())}
targets={str(t['tic']):t for t in json.loads((ROOT/'results/followup-planning-20261013/targets.json').read_text())['targets']}
checks=[]
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always')
 for r in rows:
  if r['passes_full_track']!='True': continue
  c=targets[r['tic']]['coordinates'];s=sites[r['site']]
  target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
  loc=EarthLocation.from_geodetic(s['lon']*u.deg,s['lat']*u.deg,s['height']*u.m)
  a=Time(r['start_utc'],scale='utc');b=Time(r['end_utc'],scale='utc');duration=(b-a).to_value(u.s)
  ts=a+np.linspace(0,duration,math.ceil(duration/31)+1)*u.s
  aa=AltAz(obstime=ts,location=loc,pressure=0*u.hPa)
  alt=target.transform_to(aa).alt.deg;sun=get_sun(ts).transform_to(aa).alt.deg
  assert alt.min()>=30 and sun.max()<=-18
  if r['passes_one_degree_margin']=='True': assert alt.min()>=31 and sun.max()<=-19
  checks.append({'tic':int(r['tic']),'event':int(r['event']),'site':r['site'],'minimum_target_altitude_deg':float(alt.min()),'maximum_sun_altitude_deg':float(sun.max()),'grid_points':len(ts)})
result={'status':'pass','source_and_output_hashes_verified':True,'all_320_site_rows_present':True,'passing_tracks_rechecked_at_31_seconds':len(checks),'checks':checks,'warnings':sorted(set(str(w.message) for w in caught)),'limits':'Independent denser grid uses same Astropy transformation. Main calculation separately checks spherical altitude relation. Neither establishes weather, operational horizon, time allocation or photometric sensitivity.'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','tracks':len(checks)}))
