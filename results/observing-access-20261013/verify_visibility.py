"""Independently check hour-angle convention; no network or new flux."""
import csv,json,hashlib
from pathlib import Path
import numpy as np
from astropy.coordinates import EarthLocation,SkyCoord,TETE
from astropy.time import Time
from astropy import units as u
from astropy.utils import iers
iers.conf.auto_download=False
p=Path('results/site-visibility-20261013')
sites={s['code']:s for s in json.loads((p/'sites.json').read_text())}
targets={str(t['tic']):t for t in json.loads(Path('results/followup-planning-20261013/targets.json').read_text())['targets']}
checks=[]
for r in csv.DictReader((p/'site-events.csv').open()):
 if r['passes_full_track']!='True':continue
 s=sites[r['site']];c=targets[r['tic']]['coordinates'];loc=EarthLocation.from_geodetic(s['lon']*u.deg,s['lat']*u.deg,s['height']*u.m)
 a=Time(r['start_utc'],location=loc);b=Time(r['end_utc'],location=loc);times=a+np.linspace(0,(b-a).to_value(u.s),1001)*u.s
 target=SkyCoord(c['linear_ra_j2027_deg']*u.deg,c['linear_dec_j2027_deg']*u.deg)
 app=target.transform_to(TETE(obstime=times,location=loc));ha=(times.sidereal_time('apparent')-app.ra).wrap_at(180*u.deg).hour
 mx=float(np.max(np.abs(ha)));checks.append({'event':int(r['event']),'site':r['site'],'max_abs_HA_TETE_LST_hours':mx,'passes_4p6':mx<=4.6,'margin_sidereal_seconds':(4.6-mx)*3600})
inputs=['ASSESSMENT.md','summary.json','instrument-screen.json','verification.json','site-events.csv']
obj={'status':'pass','method':'Independent apparent LST minus topocentric TETE RA; original uses ERA minus CIRS RA. Same Astropy library; checks convention consistency, not instrument availability.','checks':checks,'inputs_sha256':{str(p/f):hashlib.sha256((p/f).read_bytes()).hexdigest() for f in inputs},'protocol_sha256':hashlib.sha256(Path('results/decisive-observation-protocol-20261013/ASSESSMENT.md').read_bytes()).hexdigest()}
assert [x['passes_4p6'] for x in checks]==[True,False,False]
Path('results/observing-access-20261013/review-verification.json').write_text(json.dumps(obj,indent=2)+'\n')
print('Hour-angle decisions independently reproduced')
