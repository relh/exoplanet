"""Fixed-ephemeris coverage audit; no period/phase optimization."""
from pathlib import Path
from collections import Counter
import json
import numpy as np
from astropy.io.votable import parse
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
iers.conf.auto_download=False
out=Path(__file__).parent
paths={n:Path(f'data/catalogs/skymapper-80387959-dr4-{n}.xml') for n in ['photometry','images','master']}
tables={n:parse(p).get_first_table().to_table() for n,p in paths.items()}
images={int(r['image_id']):r for r in tables['images']};master={int(r['object_id']):r for r in tables['master']}
npth=Path('results/neighbors-80387959-20261009/tic-neighbors.json');neighbors=json.loads(npth.read_text());coords=SkyCoord([r['ra'] for r in neighbors]*u.deg,[r['dec'] for r in neighbors]*u.deg)
fp=Path('results/followup-80387959-qlp90-100-20261009/frozen.json');frozen=json.loads(fp.read_text());b=frozen['best'];ranges=frozen['timing_ranges'];floor=ranges.get('conditional_epoch_floor_days',0)
origin=EarthLocation.from_geocentric(0*u.m,0*u.m,0*u.m)
objects=[];rows=[]
for oid,m in master.items():
 coord=SkyCoord(float(m['raj2000'])*u.deg,float(m['dej2000'])*u.deg);sep=coord.separation(coords).arcsec;j=int(np.argmin(sep));objects.append({'object_id':oid,'nearest_tic':int(neighbors[j]['ID']),'separation_arcsec':float(sep[j]),'ra':float(m['raj2000']),'dec':float(m['dej2000'])})
for row in tables['photometry']:
 oid=int(row['object_id']);im=images[int(row['image_id'])];m=master[oid];coord=SkyCoord(float(m['raj2000'])*u.deg,float(m['dej2000'])*u.deg)
 tm=Time(float(im['date'])+float(im['exp_time'])/172800,format='mjd',scale='utc',location=origin)
 t=float((tm.tdb+tm.light_travel_time(coord)).jd-2457000);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 event=int(np.rint((t-b['transit_time'])/b['period']));pred=np.array([e+event*p for p,e in ranges['profile_timing_pairs']]);lo=float(pred.min()-floor-b['duration']/2-float(im['exp_time'])/172800);hi=float(pred.max()+floor+b['duration']/2+float(im['exp_time'])/172800)
 mag=float(row['mag_psf']) if not np.ma.is_masked(row['mag_psf']) else None;err=float(row['e_mag_psf']) if not np.ma.is_masked(row['e_mag_psf']) else None
 valid=mag is not None and err is not None and np.isfinite(mag) and np.isfinite(err) and err>0
 strict=valid and int(row['flags'])==0 and int(row['nimaflags'])==0 and int(im['img_qual'])<=2
 relaxed=valid and int(row['flags'])<4 and int(row['nimaflags'])<5 and int(im['img_qual'])<=2
 rows.append({'object_id':oid,'image_id':int(row['image_id']),'filter':str(row['filter']),'midpoint_btjd':t,'night_mjd':int(im['night_mjd']),'exptime_s':float(im['exp_time']),'phase_days':phase,'event':event,'inside_best':bool(abs(phase)<b['duration']/2),'inside_timing_envelope':bool(lo<=t<=hi),'timing_envelope_btjd':[lo,hi],'mag':mag,'error':err,'flags':int(row['flags']),'nimaflags':int(row['nimaflags']),'img_qual':int(im['img_qual']),'strict':bool(strict),'relaxed':bool(relaxed)})
summaries=[]
for obj in objects:
 rr=[r for r in rows if r['object_id']==obj['object_id']];rec={**obj,'n_all':len(rr),'quality':{}}
 for policy in ['strict','relaxed']:
  q=[r for r in rr if r[policy]];inside=[r for r in q if r['inside_best']];potential=[r for r in q if r['inside_timing_envelope']]
  rec['quality'][policy]={'n':len(q),'n_nights':len({r['night_mjd'] for r in q}),'n_inside_best':len(inside),'n_potential_inside':len(potential),'n_potential_events':len({r['event'] for r in potential}),'by_filter':dict(Counter(r['filter'] for r in q)),'potential_rows':potential}
 summaries.append(rec)
save_json(out/'analysis.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_sha256':{n:sha(p) for n,p in paths.items()},'frozen_sha256':sha(fp),'neighbor_sha256':sha(npth),'objects':summaries,'detections':rows,'policy':'Fixed TESS ephemeris, no fit. MJD UTC exposure-start metadata plus half exposure -> geocentric BJD TDB; omitted observatory displacement <=0.022seconds, negligible versus conditional timing envelope. Image metadata documents start time; image-date scale interpreted as UT per public access documentation. Strict flags0/nimaflags0/imgqual<=2; relaxed flags<4/nimaflags<5/imgqual<=2. Both require finite positive PSF uncertainty. Per-object/filter, no pooled colors. Nearest TIC positions not proper-motion propagated; inspect association separations. Timing profile is conditional and not a calibrated confidence interval. Sparse or absent in-event points do not exclude a contaminant.'})
for r in summaries:print(r['object_id'],r['nearest_tic'],r['separation_arcsec'],{k:{x:y for x,y in v.items() if x!='potential_rows'} for k,v in r['quality'].items()},flush=True)
