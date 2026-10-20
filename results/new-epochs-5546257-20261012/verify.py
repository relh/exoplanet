from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.search import flatten
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());checks=[]
def ck(v,s):
 assert v,s
 checks.append(s)
for path,h in plan['inputs'].items():ck(sha(Path(path))==h,'frozen hash')
for product in r['products']:
 s=product['sector'];path=Path(f'data/new-epochs-5546257-20261012/5546257-s{s:04d}.fits');ck(sha(path)==product['source']['sha256'],'FITS hash');ck(product['started_utc']>plan['frozen_utc'],'freeze precedes access')
 with fits.open(path) as h:
  ck(h[0].header['TICID']==5546257 and h[0].header['SECTOR']==s,'FITS identity');ck(h[1].header.get('BJDREFI',h[0].header.get('BJDREFI'))==2457000 and h[1].header.get('TIMESYS',h[0].header.get('TIMESYS'))=='TDB','time context');d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])&np.isfinite(d['DET_FLUX'])&(d['DET_FLUX']>0)&np.isfinite(d['DET_FLUX_ERR'])&(d['DET_FLUX_ERR']>0);ck(mask.sum()==product['n_input'],'raw quality mask');t=np.array(d['TIME'][mask],float);y=np.array(d['DET_FLUX'][mask],float);e=np.array(d['DET_FLUX_ERR'][mask],float);ii=np.argsort(t);t,y,e=t[ii],y[ii],e[ii]
 for w in plan['windows']:
  out=flatten(t,y,e,window=w);a=np.load(p/f's{s}-w{w}.npz');ck(all(np.array_equal(a[k],v) for k,v in zip(['t','y','e'],out)),'raw-to-flattened reconstruction')
def measure(a,b,epoch,event=None):
 t,y,e=a['t'],a['y'],a['e'];cycle=np.round((t-epoch)/b['period']).astype(int);dist=abs(t-epoch-cycle*b['period']);inside=dist<b['duration']/2;outside=(dist>b['duration'])&(dist<min(3*b['duration'],b['period']/2))
 if event is not None:inside &= cycle==event;outside &= cycle==event
 if inside.sum()<2 or outside.sum()<5:return None
 use=inside|outside;X=np.column_stack([np.ones(use.sum()),-inside[use].astype(float)]);A=X/e[use,None];Q,R=np.linalg.qr(A);coef=np.linalg.solve(R,Q.T@(y[use]/e[use]));inv=np.linalg.inv(R);return float(coef[1]),float(np.sqrt((inv@inv.T)[1,1])),int(inside.sum())
def compare(m,s,label):
 ck((m is None)==(s is None),label+' coverage')
 if m is not None:ck(abs(m[0]-s['depth'])<1e-9 and abs(m[1]-s['error'])<1e-10 and m[2]==s['n'],label+' QR depth/error/count')
for row in r['rows']:
 a=np.load(p/f"s{row['sector']}-w{row['window']}.npz");c=next(c for c in plan['clocks'] if c['name']==row['clock']);b=c['best'];compare(measure(a,b,b['transit_time']),row['measurement']['total'],'total')
 for ev in row['measurement']['events']:compare(measure(a,b,b['transit_time'],ev['event']),ev,'event')
 for ctr in row['controls']:compare(measure(a,b,b['transit_time']+ctr['shift']),ctr['measurement'],'phase control')
 ck(row['measurement']['supported_events']==sum(ev['snr']>=2 for ev in row['measurement']['events']),'supported events')
 if c['ranges']:
  offsets=[]
  for per,ep in c['ranges']['profile_timing_pairs']:
   ep+=round((b['transit_time']-ep)/per)*per
   for t in [min(a['t']),max(a['t'])]:offsets.append(abs(ep-b['transit_time']+round((t-b['transit_time'])/b['period'])*(per-b['period'])))
  spread=max(offsets)+3*c['ranges']['conditional_epoch_floor_days'];ck(abs(spread-row['spread_days'])<1e-10,'timing propagation');ck(spread>=b['duration']/2,'failed timing gate')
 else:ck(row['spread_days'] is None,'missing seed profile')
 ck(row['conclusion']=='timing_prediction_inconclusive','inconclusive retained')
save_json(p/'verification.json',dict(status='passed',n_checks=len(checks),checks=checks,limits='Shared flatten and FITS reader; independent QR measurements and scalar timing. Not source attribution.'));print('PASS',len(checks))
