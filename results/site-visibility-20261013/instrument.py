"""Apply separately frozen LCO 1m hour-angle constraint to retained geometry."""
import csv,json,hashlib
from pathlib import Path
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord,EarthLocation,CIRS
from astropy.time import Time
from astropy.utils import iers
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
iers.conf.auto_download=False
sites={s['code']:s for s in json.loads((P/'sites.json').read_text())}
targets={str(t['tic']):t for t in json.loads((ROOT/'results/followup-planning-20261013/targets.json').read_text())['targets']}
rows=list(csv.DictReader((P/'site-events.csv').open()));out=[]
for r in rows:
 if r['passes_full_track']!='True':continue
 c=targets[r['tic']]['coordinates'];s=sites[r['site']]
 target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
 loc=EarthLocation.from_geodetic(s['lon']*u.deg,s['lat']*u.deg,s['height']*u.m)
 a=Time(r['start_utc']);b=Time(r['end_utc']);ts=a+np.linspace(0,(b-a).to_value(u.s),1001)*u.s
 cirs=target.transform_to(CIRS(obstime=ts,location=loc))
 ha=(ts.earth_rotation_angle(longitude=loc.lon)-cirs.ra).wrap_at(180*u.deg).hour
 out.append({'tic':int(r['tic']),'event':int(r['event']),'site':r['site'],'maximum_absolute_hour_angle_hours':float(np.abs(ha).max()),'passes_lco_1m_hour_angle':bool(np.abs(ha).max()<=4.6),'passes_lco_1m_with_1deg_margin':bool(np.abs(ha).max()<=(4.6-1/15))})
result={'rows':out,'note':'Only original full-track geometry passes need the additional filter; all failed geometry remains failed. Site OGG has no LCO 1m; no OGG tracks passed geometry. This is a mechanical-limit screen, not a booking or precision guarantee.','sources':{'url':'https://lco.global/observatory/telescopes/1m0/','path':'data/site-visibility-20261013/lco-1m.html','sha256':hashlib.sha256((ROOT/'data/site-visibility-20261013/lco-1m.html').read_bytes()).hexdigest()},'inputs_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['instrument-amendment.json','instrument.py','site-events.csv','sites.json']}}
(P/'instrument-screen.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
