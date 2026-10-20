from pathlib import Path
import json,numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord,EarthLocation
import astropy.units as u
from astropy.utils import iers
from exoplanet.followup import prediction_spread
from exoplanet.pipeline import save_json,sha,now
iers.conf.auto_download=False
p=Path(__file__).parent;plan=json.loads((p/'ztf-plan.json').read_text());manifest=json.loads((p/'ztf-cloud-results.json').read_text());site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m);streams=[];roundtrips=[]
for row in manifest['objects']:
 raw=Path(row['path']);assert sha(raw)==row['sha256'];r=json.loads(raw.read_text());a=[z for z in r['lightcurve'] if z['catflags']==0 and all(z.get(k) is not None and np.isfinite(z[k]) for k in ['hmjd','mag','magerr']) and z['magerr']>0];h=np.array([z['hmjd'] for z in a]);mag=np.array([z['mag'] for z in a]);me=np.array([z['magerr'] for z in a]);y=10**(-.4*(mag-np.median(mag)));e=y*.4*np.log(10)*me;sky=SkyCoord(r['objra']*u.deg,r['objdec']*u.deg);times={}
 for scale in ['utc','tdb']:
  obs=h.copy()
  for _ in range(5):
   tt=Time(obs,format='mjd',scale=scale,location=site);obs=h-tt.light_travel_time(sky,kind='heliocentric',ephemeris='builtin').to_value(u.day)
  tt=Time(obs,format='mjd',scale=scale,location=site);roundtrips.append(float(np.max(abs(tt.mjd+tt.light_travel_time(sky,kind='heliocentric').to_value(u.day)-h))*86400));times[scale]=(tt.tdb+tt.light_travel_time(sky,kind='barycentric')).jd-2457000
 oid=r['objectid'];np.savez_compressed(p/f'ztf-{oid}-processed.npz',h=h,y=y,e=e,utc=times['utc'],tdb=times['tdb']);streams.append(dict(oid=oid,filterid=r['filterid'],h=h,y=y,e=e,utc=times['utc'],tdb=times['tdb'],raw_count=len(r['lightcurve'])))
sets=[]
for s in streams:sets.append((str(s['oid']),[s],np.arange(len(s['h']))))
for f in sorted(set(s['filterid'] for s in streams)):
 ss=sorted([s for s in streams if s['filterid']==f],key=lambda x:x['oid']);h=np.concatenate([s['h'] for s in ss]);oid=np.concatenate([np.full(len(s['h']),s['oid']) for s in ss]);keep=[]
 for idx in np.lexsort((h,oid)):
  if all(abs(h[idx]-h[k])*86400>1 for k in keep):keep.append(int(idx))
 sets.append((f'filter{f}',ss,np.array(sorted(keep))))
measurements=[]
for name,ss,keep in sets:
 y=np.concatenate([s['y'] for s in ss])[keep];e=np.concatenate([s['e'] for s in ss])[keep];oid=np.concatenate([np.full(len(s['y']),s['oid']) for s in ss])[keep];delta=np.max(abs(np.concatenate([s['utc']-s['tdb'] for s in ss])[keep]));
 for scale in ['utc','tdb']:
  t=np.concatenate([s[scale] for s in ss])[keep]
  for ci,c in enumerate(plan['clocks']):
   b=c['best'];inside=abs((t-b['transit_time']+b['period']/2)%b['period']-b['period']/2)<b['duration']/2;cycles=np.unique(np.rint((t[inside]-b['transit_time'])/b['period']).astype(int));spread=prediction_spread(t,b,c['ranges']);X=np.column_stack([*[oid==o for o in sorted(set(oid))],-inside.astype(float)]).astype(float);A=X/e[:,None];rank=np.linalg.matrix_rank(A);m=dict(stream=name,scale=scale,clock_index=ci,n=len(t),n_inside=int(inside.sum()),inside_cycles=cycles.tolist(),timing_spread=spread,scale_difference_days=float(delta),half_duration=b['duration']/2,rank=int(rank),n_parameters=X.shape[1],outcome='inconclusive' if spread+delta+1/86400>=b['duration']/2 or len(cycles)<2 else 'timing_count_pass_only',kept_indices=keep.tolist())
   if rank==X.shape[1]:
    coef=np.linalg.lstsq(A,y/e,rcond=None)[0];cov=np.linalg.inv(A.T@A);error=float(np.sqrt(cov[-1,-1]));res=(y-X@coef)/e;scaleerr=max(1,float(np.sqrt(np.sum(res**2)/(len(y)-X.shape[1]))));m.update(depth=float(coef[-1]),formal_error=error,snr=float(coef[-1]/error),scatter_scaled_error=error*scaleerr,illustrative_expected_snr=plan['illustrative_fractional_eclipse_for_635ppm']/error)
   measurements.append(m)
save_json(p/'ztf-results.json',dict(created_utc=now(),streams=[dict(oid=s['oid'],filterid=s['filterid'],raw_count=s['raw_count'],quality_count=len(s['h']),hmjd_span=[float(min(s['h'])),float(max(s['h']))],flux_p05_p95=np.percentile(s['y'],[5,95]).tolist(),median_error=float(np.median(s['e']))) for s in streams],roundtrip_max_seconds=max(roundtrips),measurements=measurements,limits='All fixed clocks retained; no period tuning. Per-stream intercepts; all non-inside points baseline. Historical metadata ngoodobs differs from cloud release nepochs; all retrieved preselected OIDs retained. Sparse and imprecise ephemerides prevent exclusion; source PSF may remain blended.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(4,2,figsize=(12,10),constrained_layout=True)
for i,s in enumerate(sorted(streams,key=lambda s:s['oid'])):
 b=plan['clocks'][2]['best'];phase=(s['utc']-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 axs[i,0].errorbar(s['utc'],s['y'],yerr=s['e'],fmt='.',ms=3);axs[i,0].set(title=f"OID {s['oid']} filter{s['filterid']}",xlabel='BTJD (UTC HMJD interpretation)',ylabel='Relative flux');axs[i,1].errorbar(phase,s['y'],yerr=s['e'],fmt='.',ms=3);axs[i,1].axvspan(-b['duration']/2,b['duration']/2,color='orange',alpha=.3);axs[i,1].set(xlabel='Days from unchanged expanded ephemeris',ylabel='Relative flux')
fig.savefig(p/'ztf-diagnostic.png',dpi=120);print([(m['stream'],m['n_inside'],m.get('depth'),m.get('formal_error'),m['timing_spread']) for m in measurements if m['scale']=='utc' and m['clock_index']==2])
