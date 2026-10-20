from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['best'];out=[]
def load(inp):
 assert sha(Path(inp['path']))==inp['sha256']
 with fits.open(inp['path']) as h:
  d=h[1].data;t=np.asarray(d['TIME'],float);y=np.asarray(d[inp['flux']],float);e=np.asarray(d[inp['error']],float);m=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);order=np.argsort(t[m]);t,y,e=t[m][order],y[m][order],e[m][order];return t,y,e,float(np.median(np.diff(t)))
def fit(X,y,e,empirical=False):
 A=X/e[:,None];v=y/e;beta=np.linalg.lstsq(A,v,rcond=None)[0];res=v-A@beta;variance=np.sum(res**2)/(len(v)-X.shape[1]);cov=np.linalg.inv(A.T@A)*(variance if empirical else max(1,variance));return beta,cov
for sector in [36,37]:
 inputs=[i for i in p['inputs'] if i['sector']==sector];a,c=map(load,inputs);t,y,e,cad=a;u,z,ze,zcad=c;ind=np.searchsorted(u,t);ind=np.clip(ind,1,len(u)-1);ind=np.where(abs(u[ind]-t)<abs(u[ind-1]-t),ind,ind-1);m=abs(u[ind]-t)<=1e-4;ia=np.flatnonzero(m);ic=ind[m];assert len(np.unique(ic))==len(ic);times=(t[ia]+u[ic])/2;Y=[y[ia]/np.median(y[ia])-1,z[ic]/np.median(z[ic])-1];E=[e[ia]/np.median(y[ia]),ze[ic]/np.median(z[ic])];cyc=np.round((times-b['transit_time'])/b['period']).astype(int);dt=times-b['transit_time']-cyc*b['period'];D=b['duration'];events=[];keep=np.zeros(len(times),bool)
 for n in np.unique(cyc):
  ins=(cyc==n)&(abs(dt)<D/2);oot=(cyc==n)&(abs(dt)>D)&(abs(dt)<3*D)
  if ins.sum()>=2 and oot.sum()>=5 and np.sum(oot&(dt<0))>=2 and np.sum(oot&(dt>0))>=2:events.append(int(n));keep|=(cyc==n)&(abs(dt)<3*D)
 cc=cyc[keep];dd=dt[keep];B=np.column_stack([v for n in events for v in [(cc==n).astype(float),np.where(cc==n,dd,0)]]);rows=[]
 for product,yy,ee,exptime in [('SPOC',Y[0],E[0],cad),('QLP',Y[1],E[1],zcad),('SPOC-minus-QLP',Y[0]-Y[1],np.ones(len(times)),(cad+zcad)/2)]:
  yy,ee=yy[keep],ee[keep];box=np.maximum(0,np.minimum(dd+exptime/2,D/2)-np.maximum(dd-exptime/2,-D/2))/exptime;X=np.column_stack([B,-box]);beta,cov=fit(X,yy,ee,product=='SPOC-minus-QLP');om=[]
  for n in events:
   m=cc!=n;xx=X[m];cols=np.any(abs(xx)>0,axis=0);bb,_=fit(xx[:,cols],yy[m],ee[m],product=='SPOC-minus-QLP');om.append(dict(event=n,depth_ppm=float(bb[-1]*1e6)))
  rows.append(dict(product=product,depth_ppm=float(beta[-1]*1e6),conditional_error_ppm=float(np.sqrt(cov[-1,-1])*1e6),omissions=om));np.savez_compressed(O/f's{sector}-{product}.npz',X=X,y=yy,e=ee,beta=beta,cov=cov,t=times[keep],cycles=cc,matched_spoc_indices=ia,matched_qlp_indices=ic)
 out.append(dict(sector=sector,matched_cadences=len(times),n_spoc=len(t),n_qlp=len(u),max_timestamp_difference_seconds=float(np.max(abs(t[ia]-u[ic]))*86400),cadence_days=[cad,zcad],events=events,rows=rows));save_json(O/'results.json',dict(utc=now(),plan_sha256=sha(O/'plan.json'),rows=out));print(out[-1],flush=True)
