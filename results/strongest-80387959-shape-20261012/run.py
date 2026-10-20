from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['best'];rows=[]
def solve(X,y,e):
 A=X/e[:,None];v=y/e;beta=np.linalg.lstsq(A,v,rcond=None)[0];cov=np.linalg.inv(A.T@A);res=y-X@beta;chi=float(np.sum((res/e)**2));scale=max(1,np.sqrt(chi/(len(y)-X.shape[1])));return beta,cov*scale**2,dict(chi2=chi,dof=len(y)-X.shape[1],error_scale=float(scale),rank=int(np.linalg.matrix_rank(A)))
def model(t,y,e,cad,offset):
 cyc=np.rint((t-b['transit_time']-offset*b['period'])/b['period']).astype(int);dt=t-(b['transit_time']+(cyc+offset)*b['period']);D=b['duration'];events=[];keep=np.zeros(len(t),bool)
 for n in np.unique(cyc):
  ins=(cyc==n)&(abs(dt)<D/2);oot=(cyc==n)&(abs(dt)>D)&(abs(dt)<3*D)
  if ins.sum()>=2 and oot.sum()>=5 and np.sum(oot&(dt<0))>=2 and np.sum(oot&(dt>0))>=2:events.append(int(n));keep|=(cyc==n)&(abs(dt)<3*D)
 tt,yy,ee,cc,dd=t[keep],y[keep],e[keep],cyc[keep],dt[keep];B=np.column_stack([v for n in events for v in [(cc==n).astype(float),np.where(cc==n,dd,0)]]);overlap=lambda lo,hi:np.maximum(0,np.minimum(dd+cad/2,hi*D)-np.maximum(dd-cad/2,lo*D))/cad
 H=np.column_stack([overlap(a,z) for a,z in zip(p['profile_edges'][:-1],p['profile_edges'][1:])]);box=overlap(-.5,.5);return tt,yy,ee,cc,dd,B,H,box,events
for inp in p['inputs']:
 path=Path(inp['path']);assert sha(path)==inp['sha256']
 with fits.open(path) as h:
  d=h[1].data;t=np.array(d['TIME'],float);y=np.array(d[inp['flux_column']],float);e=np.array(d[inp['error_column']],float);keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);t,y,e=t[keep],y[keep],e[keep];order=np.argsort(t);t,y,e=t[order],y[order],e[order];med=np.median(y);y=y/med-1;e=e/med;cad=float(np.median(np.diff(t)));r=dict(sector=inp['sector'],n_native=len(t),cadence_days=cad,cases=[])
 for phase in [0,.5]:
  tt,yy,ee,cc,dd,B,H,box,events=model(t,y,e,cad,phase);cases=[('profile',H),('primary',box[:,None]),('parity',np.column_stack([box*(cc%2==0),box*(cc%2!=0)]))] if phase==0 else [('secondary',box[:,None])]
  for name,S in cases:
   X=np.column_stack([B,-S]);beta,cov,stat=solve(X,yy,ee);n=S.shape[1];om=[]
   for ev in events:
    m=cc!=ev;cols=np.where(np.any(abs(X[m])>0,axis=0))[0];bb,cv,_=solve(X[m][:,cols],yy[m],ee[m]);om.append(dict(event=ev,depths_ppm=(bb[-n:]*1e6).tolist()))
   rec=dict(name=name,events=events,n=len(tt),depths_ppm=(beta[-n:]*1e6).tolist(),covariance_ppm2=(cov[-n:,-n:]*1e12).tolist(),errors_ppm=(np.sqrt(np.diag(cov)[-n:])*1e6).tolist(),statistics=stat,omission=om)
   if name=='primary':
    # Explicit unmasked baseline comparator; baseline-fit errors are not interpreted as a new detection statistic.
    base=np.linalg.lstsq(B/ee[:,None],yy/ee,rcond=None)[0];res=yy-B@base;w=1/ee**2;depth=-np.sum(box*res*w)/np.sum(box**2*w);injected=yy-.001*box;bi,_,_=solve(X,injected,ee);basei=np.linalg.lstsq(B/ee[:,None],injected/ee,rcond=None)[0];di=-np.sum(box*(injected-B@basei)*w)/np.sum(box**2*w);rec.update(unmasked_baseline_depth_ppm=float(depth*1e6),joint_injection_recovered_ppm=float((bi[-1]-beta[-1])*1e6),unmasked_injection_recovered_ppm=float((di-depth)*1e6))
   if name=='parity':
    diff=beta[-2]-beta[-1];de=np.sqrt(cov[-2,-2]+cov[-1,-1]-2*cov[-2,-1]);rec.update(even_minus_odd_ppm=float(diff*1e6),difference_error_ppm=float(de*1e6))
   if name=='profile':
    contrast=np.array([0,1,0,-1,0]);rec.update(ingress_minus_egress_ppm=float(contrast@beta[-5:]*1e6),asymmetry_error_ppm=float(np.sqrt(contrast@cov[-5:,-5:]@contrast)*1e6))
   np.savez_compressed(O/f's{inp["sector"]}-{name}.npz',t=tt,y=yy,e=ee,cycles=cc,dt=dd,X=X,beta=beta,cov=cov);r['cases'].append(rec)
 rows.append(r);save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows));print(inp['sector'],[(v['name'],np.round(v['depths_ppm']),np.round(v['errors_ppm'])) for v in r['cases']],flush=True)
