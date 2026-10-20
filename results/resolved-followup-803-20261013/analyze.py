import json,math,hashlib
from pathlib import Path
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.utils import iers
import astropy.units as u
iers.conf.auto_download=False
R=Path(__file__).parent;p=json.loads((R/'plan.json').read_text());b=p['clock'];rng=p['timing_ranges'];phot=json.loads((R/'photometry.json').read_text())['rows'];ims={x['image_id']:x for x in json.loads((R/'images.json').read_text())['rows']};coord=SkyCoord(165.29891*u.deg,-48.61982*u.deg);loc=EarthLocation.from_geocentric(0*u.m,0*u.m,0*u.m);rows=[]
for r in phot:
 im=ims[r['image_id']];exp=float(im['exp_time']);t=Time(float(im['date'])+exp/172800,format='mjd',scale='utc',location=loc);bt=float((t.tdb+t.light_travel_time(coord)).jd-2457000);event=round((bt-b['transit_time'])/b['period']);phase=bt-b['transit_time']-event*b['period'];centers=np.array([epoch+event*period for period,epoch in rng['profile_timing_pairs']]);floor=rng['conditional_epoch_floor_days'];half=b['duration']/2
 def num(k):
  try:return float(r[k])
  except:return None
 mag=num('mag_psf');err=num('e_mag_psf');valid=mag is not None and err is not None and math.isfinite(mag) and math.isfinite(err) and err>0
 strict=valid and int(r['flags'])==0 and int(r['nimaflags'])==0 and int(im['img_qual'])<=2;relaxed=valid and int(r['flags'])<4 and int(r['nimaflags'])<5 and int(im['img_qual'])<=2
 rows.append({'image_id':r['image_id'],'band':r['filter'],'btjd':bt,'event':event,'phase':phase,'night':int(im['night_mjd']),'mag':mag,'error':err,'flags':int(r['flags']),'nimaflags':int(r['nimaflags']),'img_qual':int(im['img_qual']),'strict':bool(strict),'relaxed':bool(relaxed),'nominal_in':abs(phase)<half,'possible_in':bool(centers.min()-floor-half-exp/172800<=bt<=centers.max()+floor+half+exp/172800),'robust_in':bool(np.max(np.abs(bt-centers))+floor+exp/172800<half)})
summary={}
for pol in ['strict','relaxed']:
 rr=[r for r in rows if r[pol]];inside=[r for r in rr if r['nominal_in']];possible=[r for r in rr if r['possible_in']];robust=[r for r in rr if r['robust_in']];summary[pol]={'n':len(rr),'nominal_in':len(inside),'possible_in':len(possible),'robust_in':len(robust),'robust_events':len(set(r['event'] for r in robust)),'potential_rows':possible}
print(json.dumps(summary,indent=2));(R/'analysis.json').write_text(json.dumps({'plan_sha256':hashlib.sha256((R/'plan.json').read_bytes()).hexdigest(),'n':len(rows),'rows':rows,'summary':summary},indent=2))
