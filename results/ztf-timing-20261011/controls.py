from pathlib import Path
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.utils import iers
import astropy.units as u
from exoplanet.pipeline import save_json,sha
iers.conf.auto_download=False
p=Path(__file__).parent;site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m);rows=[]
for scale in ['utc','tdb']:
 for ra,dec in [(202.6412,-10.5554),(297.9869,-21.5031)]:
  sky=SkyCoord(ra*u.deg,dec*u.deg);known=Time([58200.,60800.],format='mjd',scale=scale,location=site)
  h=known.mjd+known.light_travel_time(sky,kind='heliocentric',ephemeris='builtin').to_value(u.day)
  expected=(known.tdb+known.light_travel_time(sky,kind='barycentric',ephemeris='builtin')).jd
  estimate=h.copy()
  for _ in range(5):
   t=Time(estimate,format='mjd',scale=scale,location=site);estimate=h-t.light_travel_time(sky,kind='heliocentric',ephemeris='builtin').to_value(u.day)
  t=Time(estimate,format='mjd',scale=scale,location=site);actual=(t.tdb+t.light_travel_time(sky,kind='barycentric',ephemeris='builtin')).jd
  error=float(np.max(abs(actual-expected))*86400);assert error<.0001
  rows.append({'scale':scale,'position':[ra,dec],'known_mjd':known.mjd.tolist(),'max_bjd_error_seconds':error})
save_json(p/'controls.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Deterministic synthetic roundtrip under assumed time scales; does not establish the archive time scale or validate TESS ephemerides.'});print(rows)
