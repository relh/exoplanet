"""Fixed-phase NSC coverage; preserve VOTable identifier-width defect."""
from pathlib import Path
from collections import Counter
import json,xml.etree.ElementTree as ET
import numpy as np
from astropy.io.votable import parse
from astropy.coordinates import SkyCoord,EarthLocation
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
iers.conf.auto_download=False
out=Path(__file__).parent;paths={k:Path(f'data/catalogs/nsc-80387959-q3c-{k}.xml') for k in ['objects','measurements','exposures']}
o=parse(paths['objects']).get_first_table().to_table();m=parse(paths['measurements']).get_first_table().to_table()
# Read original TABLEDATA text: exposure field declares24chars but stores26chars.
root=ET.parse(paths['exposures']).getroot()
for node in root.iter():node.tag=node.tag.split('}')[-1]
table=root.find('.//TABLE');fields=table.findall('FIELD');names=[x.attrib['name'] for x in fields]
raw=[dict(zip(names,[x.text or '' for x in row.findall('TD')])) for row in table.findall('.//TR')]
images={r['exposure']:r for r in raw};ids=set(map(str,m['exposure']));assert set(images)==ids and len(raw)==len(images)==27
checks=[]
for r in m:
 im=images[str(r['exposure'])];assert abs(float(im['mjd'])-float(r['mjd']))<1e-8 and im['filter']==str(r['filter'])
 checks.append(abs((Time(im['dateobs'],format='isot',scale='utc').mjd-float(im['mjd']))*86400))
save_json(out/'exposure-join-checks.json',{'utc':now(),'raw_source_sha256':sha(paths['exposures']),'n_exposures':len(images),'all_measurement_names_times_filters_match':True,'max_dateobs_mjd_difference_seconds':max(checks),'exposure_field_declared_arraysize':next(x.attrib.get('arraysize') for x in fields if x.attrib['name']=='exposure'),'max_raw_identifier_length':max(map(len,images)),'policy':'Raw XML TABLEDATA strings used for identifiers; no raw-file rewrite. Earlier Astropy fixed-width parse dropped suffix v1 and failed assertion. Original defect and failed-run log retained.'})
assert max(checks)<1
npth=Path('results/neighbors-80387959-20261009/tic-neighbors.json');neighbors=json.loads(npth.read_text());coords=SkyCoord([r['ra'] for r in neighbors]*u.deg,[r['dec'] for r in neighbors]*u.deg)
fp=Path('results/followup-80387959-qlp90-100-20261009/frozen.json');f=json.loads(fp.read_text());b=f['best'];ranges=f['timing_ranges'];floor=ranges.get('conditional_epoch_floor_days',0)
origin=EarthLocation.from_geocentric(0*u.m,0*u.m,0*u.m);objects=[];rows=[]
for ob in o:
 oid=str(ob['id']);coord=SkyCoord(float(ob['ra'])*u.deg,float(ob['dec'])*u.deg);sep=coord.separation(coords).arcsec;j=int(np.argmin(sep))
 obj={'object_id':oid,'nearest_tic':int(neighbors[j]['ID']),'separation_arcsec':float(sep[j]),'association_within_1arcsec':bool(sep[j]<1)};objects.append(obj)
 for r in m[m['objectid']==oid]:
  im=images[str(r['exposure'])];exp=float(im['exptime']);tm=Time(float(r['mjd'])+exp/172800,format='mjd',scale='utc',location=origin);t=float((tm.tdb+tm.light_travel_time(coord)).jd-2457000)
  phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;event=int(np.rint((t-b['transit_time'])/b['period']));pred=np.array([epoch+event*period for period,epoch in ranges['profile_timing_pairs']]);lo=float(pred.min()-floor-b['duration']/2-exp/86400);hi=float(pred.max()+floor+b['duration']/2+exp/86400)
  mag=float(r['mag_auto']);err=float(r['magerr_auto']);flags=int(r['flags']);finite=np.isfinite(mag) and np.isfinite(err) and 0<mag<50 and 0<err<1
  rows.append({'object_id':oid,'exposure':str(r['exposure']),'filter':str(r['filter']),'midpoint_btjd':t,'exptime_s':exp,'phase_days':phase,'event':event,'inside_best':bool(abs(phase)<b['duration']/2),'inside_generous_envelope':bool(lo<=t<=hi),'envelope_btjd':[lo,hi],'mag_auto':mag,'magerr_auto':err,'flags':flags,'strict':bool(finite and flags==0),'relaxed_blends':bool(finite and flags<4)})
summary=[]
for obj in objects:
 rr=[r for r in rows if r['object_id']==obj['object_id']];rec={**obj,'n_all':len(rr),'flags':dict(Counter(r['flags'] for r in rr)),'n_inside_any_quality':sum(r['inside_generous_envelope'] for r in rr),'quality':{}}
 for q in ['strict','relaxed_blends']:
  qq=[r for r in rr if r[q]];potential=[r for r in qq if r['inside_generous_envelope']];rec['quality'][q]={'n':len(qq),'n_inside_best':sum(r['inside_best'] for r in qq),'n_potential_inside':len(potential),'n_potential_events':len({r['event'] for r in potential}),'by_filter':dict(Counter(r['filter'] for r in qq))}
 summary.append(rec)
save_json(out/'analysis.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_sha256':{k:sha(p) for k,p in paths.items()},'frozen_sha256':sha(fp),'objects':summary,'measurements':rows,'policy':'Fixed frozen TESS phase, no optimization. Interpret exposure dateobs/MJD as UTC start, add half exposure, convert geocentric BJD TDB (topocentric omission<=0.022s). Generous conditional profile envelope additionally padded one full exposure on both sides, covering start/midpoint convention sensitivity. flags0 strict;flags<4 includes deblend/neighbor warnings, exploratory only. Magnitude sentinels>=50 and invalid errors excluded. Nearest TIC positions not propagated for proper motion; associations>1arcsec not treated as matches. Missing catalog sources and absent phase coverage cannot exclude contaminants; no depth/planet claim.'})
for r in summary:print(r['object_id'],r['nearest_tic'],round(r['separation_arcsec'],2),r['n_all'],r['n_inside_any_quality'],r['quality'],flush=True)
