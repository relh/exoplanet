"""Conditional timing coverage under two explicitly assumed HMJD scales."""
from pathlib import Path
import json,numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.utils import iers
import astropy.units as u
from exoplanet.pipeline import sha,save_json
from exoplanet.followup import prediction_spread
iers.conf.auto_download=False
p=Path(__file__).parent;cloud=Path('results/ztf-cloud-20261011/results.json');catalog=Path('results/ztf-catalog-route-20261011/catalog-results.json');lookup={int(x['oid']):r['tic'] for r in json.loads(catalog.read_text()) for x in r['rows']};site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m)
rows=[];inputs={str(cloud):sha(cloud),str(catalog):sha(catalog),str(Path(__file__)):sha(Path(__file__))}
for record in json.loads(cloud.read_text())['objects']:
 file=Path(record['path']);assert sha(file)==record['sha256'];inputs[str(file)]=sha(file);o=json.loads(file.read_text());tic=lookup[o['objectid']];fp=Path(f'results/qlp-faint-midradius-single-review-20261011/{tic}-peak0/frozen.json');inputs[str(fp)]=sha(fp);f=json.loads(fp.read_text());b=f['best'];ranges=f['timing_ranges']
 good=[x for x in o['lightcurve'] if x['catflags']==0 and all(x[k] is not None and np.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0]
 h=np.array([x['hmjd'] for x in good]);sky=SkyCoord(o['objra']*u.deg,o['objdec']*u.deg);converted=[];roundtrip=[]
 for scale in ['utc','tdb']:
  # Invert the assumed heliocentric correction before applying barycentric/TDB.
  observed=h.copy()
  for _ in range(5):
   t=Time(observed,format='mjd',scale=scale,location=site)
   observed=h-t.light_travel_time(sky,kind='heliocentric',ephemeris='builtin').to_value(u.day)
  t=Time(observed,format='mjd',scale=scale,location=site)
  roundtrip.append(float(np.max(abs(observed+t.light_travel_time(sky,kind='heliocentric',ephemeris='builtin').to_value(u.day)-h))*86400))
  converted.append((t.tdb+t.light_travel_time(sky,kind='barycentric',ephemeris='builtin')).jd-2457000)
 utc,tdb=converted;difference=abs(utc-tdb)
 # Existing heuristic evaluated independently at each observation; no new fit.
 spread=np.array([prediction_spread(np.array([x]),b,ranges) for x in utc]);combined=spread+difference+1/86400
 useful=(combined<b['duration']/2)&(not ranges['search_boundary_hit'])
 phase=(utc-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 np.savez_compressed(p/f"{o['objectid']}-timing.npz",hmjd=h,btjd_assume_utc=utc,btjd_assume_tdb=tdb,conditional_spread=spread,combined_heuristic=combined,timing_useful=useful,phase_assume_utc=phase)
 rows.append({'tic':tic,'oid':o['objectid'],'n':len(h),'btjd_range_assume_utc':[float(utc.min()),float(utc.max())],'roundtrip_max_seconds':roundtrip,'scale_difference_seconds':[float(difference.min()*86400),float(difference.max()*86400)],'n_timing_useful':int(useful.sum()),'n_nominal_in_window_useful':int((useful&(abs(phase)<b['duration']/2)).sum()),'half_duration_days':b['duration']/2,'spread_days_range':[float(spread.min()),float(spread.max())],'search_boundary_hit':ranges['search_boundary_hit']})
 assert max(roundtrip)<.001
save_json(p/'results.json',{'inputs':inputs,'objects':rows,'method':'Invert heliocentric delay then add barycentric delay and convert to TDB. Approximate Palomar site, builtin ephemeris, five fixed-point iterations. Both UTC and TDB interpretations retained. Midpoint: no half exposure added. Useful gate = existing TESS conditional spread + full scale difference +1second < half duration, and no profile search boundary.','limits':'Time scale unverified; UTC/TDB sensitivity is not an exhaustive bound. HJD approximation, source position and model mismatch not fully propagated. Existing TESS spread is a heuristic, not posterior. Counts describe timing coverage, not transit detection or exclusion.'})
print(rows)
