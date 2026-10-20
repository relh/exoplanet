from pathlib import Path
import json,hashlib,numpy as np
from scipy.linalg import solve_triangular
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
import astropy.units as u
from astropy.utils import iers
iers.conf.auto_download=False
p=Path(__file__).parent;plan=json.loads((p/'ztf-plan.json').read_text());res=json.loads((p/'ztf-results.json').read_text());manifest=json.loads((p/'ztf-cloud-results.json').read_text());checks=[];streams={}
def ck(v,s):
 assert v,s
 checks.append(s)
for path,h in plan['source_hashes'].items():ck(hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,'input hash')
ck(plan['frozen_utc']<json.loads((p/'ztf-fetch-start.json').read_text())['started_utc'],'freeze precedes fetch')
ck(set(x['objectid'] for x in manifest['objects'])==set(int(x['row']['oid']) for x in plan['selected']),'all frozen OIDs retained')
site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m)
for item in manifest['objects']:
 raw=Path(item['path']);ck(hashlib.sha256(raw.read_bytes()).hexdigest()==item['sha256'],'raw export hash');r=json.loads(raw.read_text());a=[q for q in r['lightcurve'] if q['catflags']==0 and all(q[k] is not None and np.isfinite(q[k]) for k in ['hmjd','mag','magerr']) and q['magerr']>0];arr=np.array([[q['hmjd'],q['mag'],q['magerr']] for q in a]);z=np.load(p/f"ztf-{r['objectid']}-processed.npz");ck(len(a)==len(z['h']),'quality selection');f=10**(-.4*(arr[:,1]-np.median(arr[:,1])));err=f*arr[:,2]*np.log(100)/5;ck(np.max(abs(f-z['y']))<1e-10 and np.max(abs(err-z['e']))<1e-10,'flux and uncertainty conversion');sky=SkyCoord(r['objra']*u.deg,r['objdec']*u.deg);target=SkyCoord(float(plan['source_position']['ra'])*u.deg,float(plan['source_position']['dec'])*u.deg);ck(sky.separation(target).arcsec<1,'cloud source position within1arcsec')
 for scale in ['utc','tdb']:
  time=Time(arr[:,0],format='mjd',scale=scale,location=site)
  for n in range(7):time=Time(arr[:,0],format='mjd',scale=scale,location=site)-time.light_travel_time(sky,kind='heliocentric')
  out=(time.tdb+time.light_travel_time(sky,kind='barycentric')).jd-2457000;ck(np.max(abs(out-z[scale]))<1e-8,'independent time iteration')
 streams[r['objectid']]=dict(z=z,filterid=r['filterid'])
for m in res['measurements']:
 ids=sorted(streams) if m['stream'].startswith('filter') else [int(m['stream'])]
 if m['stream'].startswith('filter'):ids=[i for i in ids if streams[i]['filterid']==int(m['stream'][-1])]
 h=np.concatenate([streams[i]['z']['h'] for i in ids]);oid=np.concatenate([np.repeat(i,len(streams[i]['z']['h'])) for i in ids]);keep=[]
 for i in sorted(range(len(h)),key=lambda k:(int(oid[k]),float(h[k]))):
  if not m['stream'].startswith('filter') or not any(abs(h[i]-h[j])<=1/86400 for j in keep):keep.append(i)
 keep=sorted(keep);ck(keep==m['kept_indices'],'deterministic exposure selection');oid=oid[keep];t=np.concatenate([streams[i]['z'][m['scale']] for i in ids])[keep];y=np.concatenate([streams[i]['z']['y'] for i in ids])[keep];e=np.concatenate([streams[i]['z']['e'] for i in ids])[keep];c=plan['clocks'][m['clock_index']];b=c['best'];cycles=np.round((t-b['transit_time'])/b['period']);inside=abs(t-(b['transit_time']+cycles*b['period']))<b['duration']/2;ck(inside.sum()==m['n_inside'],'independent event count');ck(np.unique(cycles[inside]).astype(int).tolist()==m['inside_cycles'],'event cycles')
 offsets=[]
 for per,ep in c['ranges']['profile_timing_pairs']:
  ep+=round((b['transit_time']-ep)/per)*per
  for tt in [min(t),max(t)]:
   k=round((tt-b['transit_time'])/b['period']);offsets.append(abs(ep-b['transit_time']+k*(per-b['period'])))
 spread=max(offsets,default=0)+3*c['ranges']['conditional_epoch_floor_days'];ck(abs(spread-m['timing_spread'])<1e-10,'timing profile propagation');ck(m['outcome']=='inconclusive' and (spread+m['scale_difference_days']+1/86400>=b['duration']/2 or len(m['inside_cycles'])<2),'inconclusive classification')
 X=np.column_stack([*[oid==i for i in ids],-inside.astype(float)]).astype(float);ck(np.linalg.matrix_rank(X/e[:,None])==m['rank'],'design rank')
 if 'depth' in m:
  Q,R=np.linalg.qr(X/e[:,None]);coef=solve_triangular(R,Q.T@(y/e));inv=solve_triangular(R,np.eye(len(R)));cov=inv@inv.T;err=np.sqrt(cov[-1,-1]);ck(abs(coef[-1]-m['depth'])<1e-10 and abs(err-m['formal_error'])<1e-10,'QR coefficient and covariance');chi=np.sum(((y-X@coef)/e)**2);ck(abs(err*max(1,np.sqrt(chi/(len(y)-len(coef))))-m['scatter_scaled_error'])<1e-10,'scatter-scaled error')
(p/'ztf-verification.json').write_text(json.dumps(dict(status='passed',n_checks=len(checks),checks=checks),indent=2)+'\n');print('PASS',len(checks))
