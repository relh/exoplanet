from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from exoplanet.pipeline import sha,save_json,now
from exoplanet.followup import prediction_spread
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['best'];rng=np.random.default_rng(p['fit']['rng_seed']);results=[]
def fit_events(t,y,e,maskarr):
 parts=[]
 for n,inside,outside in maskarr:
  sel=inside|outside;dt=t[sel]-(b['transit_time']+n*b['period']);parts.append((n,dt,y[sel],e[sel],inside[sel]))
 N=sum(len(a[1]) for a in parts);X=np.zeros((N,2*len(parts)+1));Y=np.zeros(N);E=np.zeros(N);sl=[];pos=0
 for i,(n,dt,yy,ee,ins) in enumerate(parts):
  s=slice(pos,pos+len(dt));X[s,2*i]=1;X[s,2*i+1]=dt;X[s,-1]=-ins.astype(float);Y[s]=yy;E[s]=ee;sl.append(s);pos+=len(dt)
 A=X/E[:,None];v=Y/E;beta=np.linalg.lstsq(A,v,rcond=None)[0];cov=np.linalg.inv(A.T@A);res=Y-X@beta;pinv=np.linalg.pinv(A);vals=[]
 for k in range(200):
  rr=np.zeros(N)
  for s,part in zip(sl,parts):
   dt=part[1];n=len(dt);cad=np.median(np.diff(dt));length=min(n,max(1,round(.1/cad)));starts=rng.integers(0,n,int(np.ceil(n/length)));ix=((starts[:,None]+np.arange(length))%n).ravel()[:n];rr[s]=res[s][ix]
  vals.append((pinv@(rr/E))[-1])
 return dict(depth=float(beta[-1]),formal_error=float(np.sqrt(cov[-1,-1])),bootstrap_error=float(np.std(vals,ddof=1)),conditional_error=float(max(np.sqrt(cov[-1,-1]),np.std(vals,ddof=1))),rank=int(np.linalg.matrix_rank(A)),n_parameters=X.shape[1]),dict(X=X,Y=Y,E=E,beta=beta)
for sector in p['sectors']:
 src=json.loads((O/f'source-s{sector}.json').read_text());r=dict(sector=sector,source_status=src['status'],apertures=[])
 if src['status']!='downloaded':results.append(r);continue
 for file in src['files']:
  path=Path(file['path']);assert sha(path)==file['sha256']
  with fits.open(path) as h:
   d=h[1].data;w=WCS(h[2].header);xy=np.array(w.world_to_pixel_values(p['ra'],p['dec']),float);t=np.array(d['TIME'],float);f=np.array(d['FLUX'],float);fe=np.array(d['FLUX_ERR'],float);q=np.array(d['QUALITY']);yy,xx=np.indices(f.shape[1:]);rad=np.hypot(xx-xy[0],yy-xy[1]);ann=(rad>=4)&(rad<=6);finite=np.isfinite(t);valid=(q==0)&finite;r.update(path=str(path),target_xy=xy.tolist(),shape=list(f.shape),n_quality_zero=int(valid.sum()),span=[float(np.nanmin(t)),float(np.nanmax(t))],headers={k:h[0].header.get(k,h[1].header.get(k)) for k in ['SECTOR','CAMERA','CCD','RA_OBJ','DEC_OBJ']});image=np.nanmedian(f[valid],axis=0) if valid.any() else np.nanmedian(f,axis=0);np.savez_compressed(O/f'image-s{sector}.npz',median=image,target_xy=xy,annulus=ann)
   for radius in p['extraction']['aperture_radii_pixels']:
    ap=rad<=radius;rr=dict(radius=radius,n_pixels=int(ap.sum()));edge=xy[0]-radius<-.5 or xy[1]-radius<-.5 or xy[0]+radius>f.shape[2]-.5 or xy[1]+radius>f.shape[1]-.5
    nbg=np.isfinite(f[:,ann]).sum(axis=1);bg=np.nanmedian(f[:,ann],axis=1);mad=1.4826*np.nanmedian(abs(f[:,ann]-bg[:,None]),axis=1);flux=np.sum(f[:,ap],axis=1)-ap.sum()*bg;error=np.sqrt(np.sum(fe[:,ap]**2,axis=1)+(ap.sum()*1.253*mad/np.sqrt(np.maximum(nbg,1)))**2);good=valid&(nbg>=20)&np.all(np.isfinite(f[:,ap]),axis=1)&np.isfinite(flux)&(flux>0)
    rr.update(edge_truncated=bool(edge),usable_points=int(good.sum()),median_flux=float(np.nanmedian(flux[good])) if good.any() else None)
    if edge or good.sum()<30:rr['outcome']='unusable_geometry_or_points';r['apertures'].append(rr);continue
    tt,ff,ee=t[good],flux[good],error[good];order=np.argsort(tt);tt,ff,ee=tt[order],ff[order],ee[order];med=np.median(ff);ff=ff/med;ee=ee/med;errkind='propagated_pixel_errors_plus_background_MAD'
    if not np.all(np.isfinite(ee)&(ee>0)):
     scale=1.4826*np.median(abs(np.diff(ff)-np.median(np.diff(ff))))/np.sqrt(2);ee=np.full(len(tt),scale);errkind='sector_adjacent_difference_MAD_fallback'
    rr['error_model']=errkind;rr['median_error']=float(np.median(ee));phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2;ev=np.rint((tt-b['transit_time'])/b['period']).astype(int);arr=[];events=[]
    for n in np.unique(ev):
     inside=(ev==n)&(abs(phase)<b['duration']/2);outside=(ev==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration']);left=outside&(phase<0);right=outside&(phase>0);rec=dict(event=int(n),n_inside=int(inside.sum()),n_outside=int(outside.sum()),n_left=int(left.sum()),n_right=int(right.sum()));rec['usable']=bool(inside.sum()>=5 and outside.sum()>=10 and left.sum()>=5 and right.sum()>=5)
     if rec['usable']:
      a=(n,inside,outside);arr.append(a);v,_=fit_events(tt,ff,ee,[a]);rec.update(v)
     events.append(rec)
    rr.update(events=events,usable_events=len(arr),timing_spread_days=float(prediction_spread(tt,b,p['timing_ranges'])),half_duration=b['duration']/2)
    if len(arr)>=2:
     total,design=fit_events(tt,ff,ee,arr);used=[v for v in events if v['usable']];weights=np.array([1/v['formal_error']**2 for v in used]);positive=sum(v['depth']>0 for v in used);om=[]
     for i in range(len(arr)):a,_=fit_events(tt,ff,ee,arr[:i]+arr[i+1:]);om.append(dict(omitted_event=int(arr[i][0]),**a))
     gates=dict(timing=rr['timing_spread_days']<b['duration']/2 and not p['timing_ranges']['search_boundary_hit'],snr=total['depth']/total['conditional_error']>=5,majority_positive=positive>len(arr)/2,balanced_weights=float(weights.max()/weights.sum())<=.5)
     rr.update(total=total,delete_one_event=om,max_event_weight_fraction=float(weights.max()/weights.sum()),gates=gates,outcome='passes_single_aperture_gates' if all(gates.values()) else 'inconclusive_or_failed_gate');np.savez_compressed(O/f'fit-s{sector}-r{radius}.npz',t=tt,y=ff,e=ee,**design)
    else:rr['outcome']='fewer_than_two_usable_events'
    np.savez_compressed(O/f'curve-s{sector}-r{radius}.npz',t=tt,y=ff,e=ee,aperture=ap);r['apertures'].append(rr)
  aa=r['apertures']
  if len(aa)==2 and all('total' in a for a in aa):
   x,y=[a['total'] for a in aa];agreement=abs(x['depth']-y['depth'])<=3*np.hypot(x['conditional_error'],y['conditional_error']);r['aperture_agreement']=bool(agreement);r['outcome']='qualified_frozen_clock_recurrence' if agreement and all(a['outcome']=='passes_single_aperture_gates' for a in aa) else 'inconclusive_or_failed_gate'
  else:r['outcome']='unusable_or_insufficient_events'
 results.append(r);save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),rows=results));print(sector,r['outcome'],[(a['radius'],a.get('usable_points'),a.get('usable_events'),a.get('total')) for a in r['apertures']],flush=True)
