import json,pathlib,hashlib
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.utils import iers
import astropy.units as u
iers.conf.auto_download=False
R=pathlib.Path('results/lco-archive-metadata-20261013');p=pathlib.Path('results/followup-planning-20261013/targets.json');t=json.loads(p.read_text())['targets'][0];c=t['coordinates'];sky=SkyCoord(c['ra_j2016_deg']*u.deg,c['dec_j2016_deg']*u.deg)
# Geocentric correction; site timing at most21.3ms, negligible relative to hour-scale separation.
loc=EarthLocation.from_geocentric(0,0,0,unit=u.m);raw=json.loads((R/'80387959-j2016-paginated.json').read_text());rows=[]
for r in raw['records']:
 a=Time(r['DATE_OBS'],scale='utc',location=loc);b=a+r['EXPTIME']*u.s
 lo=float((a.tdb+a.light_travel_time(sky)).jd)-2457000;hi=float((b.tdb+b.light_travel_time(sky)).jd)-2457000
 n=round(((lo+hi)/2-t['epoch_btjd_tdb'])/t['period_days']);center=t['epoch_btjd_tdb']+n*t['period_days'];profile=t['clock_profiles'][0]['ranges'];centers=[ep+n*per for per,ep in profile['profile_timing_pairs']];floor=3*profile['conditional_epoch_floor_days'];half=t['duration_hours']/48
 wlo=min(centers)-floor-half;whi=max(centers)+floor+half
 rows.append({'id':r['id'],'object':r['OBJECT'],'utc_start':r['DATE_OBS'],'exptime_seconds':r['EXPTIME'],'rlevel':r['RLEVEL'],'instrument':r['INSTRUME'],'filter':r['FILTER'],'btjd_start':lo,'btjd_end':hi,'cycle':n,'nominal_center_btjd':center,'start_from_center_hours':24*(lo-center),'end_from_center_hours':24*(hi-center),'full_profile_dip_start_btjd':wlo,'full_profile_dip_end_btjd':whi,'overlaps_full_profile':bool(lo<=whi and hi>=wlo)})
out={'target_input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'clock':'Original frozen clock and all5 original profile pairs; each expanded3heuristic epoch floors plus halfduration. No refit.','time_conversion':'UTC to geocentric BJD_TDB using Astropy bundled ephemeris; observatory correction omitted, at most21.3ms. No newflux.','n_records':len(rows),'overlap_records':sum(r['overlaps_full_profile'] for r in rows),'records':rows}
(R/'803-timing.json').write_text(json.dumps(out,indent=2)+'\n')
for obj in sorted({r['object'] for r in rows}):
 rr=[r for r in rows if r['object']==obj];print(obj,len(rr),min(r['start_from_center_hours'] for r in rr),max(r['end_from_center_hours'] for r in rr),sum(r['overlaps_full_profile'] for r in rr))
