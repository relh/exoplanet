"""Read-only checks of the two explicitly authorized LCO baseline frames."""
from pathlib import Path
import json,hashlib
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy import units as u
from astropy.utils import iers
iers.conf.auto_download=False
R=Path('results/lco-archive-metadata-20261013');P=Path('results/site-visibility-20261013')
plan=json.loads((R/'image-plan.json').read_text()); reg=json.loads((R/'registered-feasibility.json').read_text()); original=json.loads((R/'image-feasibility.json').read_text());allowed={r['filename'] for r in plan['allowlist']};assert len(allowed)==2
checks=[]
for r in reg['results']:
 p=Path(r['file']);assert p.name in allowed
 orig=next(o for o in original['results'] if o['file']==str(p));assert hashlib.sha256(p.read_bytes()).hexdigest()==orig['sha256']
 with fits.open(p) as h:
  im=h['SCI'].data;mask=h['BPM'].data;header=h['SCI'].header
  rows=[]
  for s in r['sources']:
   x,y=s['registered_x0'],s['registered_y0']; yy,xx=np.indices(im.shape);ap=(xx-x)**2+(yy-y)**2<36
   # Full-image mask constructs the same aperture without producer crop indexing.
   vals=im[ap];bad=mask[ap]
   sat=int(np.sum(vals>=header['SATURATE']));lin=int(np.sum(vals>=header['MAXLIN']));nb=int(np.sum(bad!=0))
   assert sat==s['pixels_above_saturate'] and lin==s['pixels_above_maxlin'] and nb==s['bad_mask_pixels']
   rows.append({'tic':s['tic'],'saturated_pixels':sat,'nonlinear_pixels':lin,'masked_pixels':nb,'aperture_pixels':len(vals)})
  checks.append({'file':str(p),'sha256':orig['sha256'],'saturate':header['SATURATE'],'maxlin':header['MAXLIN'],'sources':rows})
target=json.loads(Path('results/followup-planning-20261013/targets.json').read_text())['targets'][0]
c=target['coordinates'];sky=SkyCoord(c['ra_j2016_deg']*u.deg,c['dec_j2016_deg']*u.deg)
geo=EarthLocation.from_geocentric(0,0,0,unit=u.m); site=EarthLocation.from_geodetic(-70.8048*u.deg,-30.1674*u.deg,2198*u.m)
tim=json.loads((R/'803-timing.json').read_text());differences=[];nominal_errors=[]
for record in tim['records']:
 n=record['cycle']; center=target['epoch_btjd_tdb']+n*target['period_days']; assert abs(center-record['nominal_center_btjd'])<1e-10
 nominal_errors.append(abs(24*(record['btjd_start']-center)-record['start_from_center_hours']))
 prof=target['clock_profiles'][0]['ranges'];cs=[ep+n*period for period,ep in prof['profile_timing_pairs']]
 lo=min(cs)-3*prof['conditional_epoch_floor_days']-target['duration_hours']/48
 hi=max(cs)+3*prof['conditional_epoch_floor_days']+target['duration_hours']/48
 assert abs(lo-record['full_profile_dip_start_btjd'])<1e-10 and abs(hi-record['full_profile_dip_end_btjd'])<1e-10
 assert not (record['btjd_start']<=hi and record['btjd_end']>=lo)
 if record['id'] in {r['id'] for r in plan['allowlist']}:
  g=Time(record['utc_start'],scale='utc',location=geo);s=Time(record['utc_start'],scale='utc',location=site)
  gb=g.tdb+g.light_travel_time(sky);sb=s.tdb+s.light_travel_time(sky)
  differences.append(float((sb-gb).to_value(u.s)))
  assert abs(gb.jd-2457000-record['btjd_start'])<1e-9
assert max(abs(x) for x in differences)<0.022
result={'status':'pass','frames':checks,'timing_records_checked':len(tim['records']),'overlap_records':0,'max_nominal_offset_arithmetic_error_hours':max(nominal_errors),'two_frame_site_minus_geocenter_bjd_seconds':differences,'limitations':'Registration coefficients inspected and image apertures independently counted; no independent absolute astrometric solution. No transit measurement or sensitivity validation.'}
(P/'LCO-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
