from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());result=json.loads((p/'results.json').read_text());b=plan['clock'];checks=[];raw={};nf=0

def ck(v,label):
 assert v,label
 checks.append(label)
for path,h in plan['inputs'].items():ck(sha(Path(path))==h,'frozen hash')
for s in plan['sectors']:
 with fits.open(f'data/lightcurves/s{s:04d}-402358350.fits') as h:
  d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
  for c in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[c])&(d[c]>0)
  for kind in plan['streams']:
   t=np.array(d['TIME'][mask],float);f=np.array(d[kind+'_FLUX'][mask],float);e=np.array(d[kind+'_FLUX_ERR'][mask],float);med=np.median(f);raw[(s,kind)]=(t,f/med,e/med)

def verify(row,key,center,m,amp=0):
 global nf
 t,y,e=raw[(row['sector'],row['kind'])];x=(t-center)/b['duration'];u=abs(x)<row['outer'];xi=x[u];inside=abs(xi)<.5;left=xi< -1;right=xi>1
 ck(m['n_inside']==inside.sum() and m['n_left']==left.sum() and m['n_right']==right.sum(),'raw coverage')
 if min(left.sum(),right.sum())<10 or inside.sum()<3:ck(m['status']=='insufficient_coverage','coverage failure preserved');return
 ck(m['status']=='measured','fit coverage');a=np.load(p/f'{key}.npz');nf+=1;yy=y.copy();yy[abs(t-center)<b['duration']/2]-=amp;ck(np.array_equal(a['x'],xi) and np.array_equal(a['y'],yy[u]),'raw normalized/injected arrays');outside=left|right;idx=np.where(outside)[0];diff=np.diff(yy[u][idx])[np.diff(t[u][idx])<1.5*np.median(np.diff(t))];floor=1.4826*np.median(abs(diff-np.median(diff)))/np.sqrt(2) if len(diff)>=10 else 0;ee=np.maximum(e[u],floor);ck(np.max(abs(ee-a['e']))<1e-12,'noise floor');X=np.vander(xi,row['degree']+1,increasing=True);Q,R=np.linalg.qr(X[outside]/ee[outside,None]);coef=np.linalg.solve(R,Q.T@(yy[u][outside]/ee[outside]));inv=np.linalg.inv(R);cov=inv@inv.T;ck(np.max(abs(coef-m['coefficients']))<1e-9,'QR baseline');ck(np.max(abs(cov-np.array(m['covariance'])))<1e-12,'QR covariance');resid=yy[u]-X@coef;scale=max(1,np.sqrt(np.sum((resid[outside]/ee[outside])**2)/(outside.sum()-len(coef))));ck(abs(scale-m['scatter_scale'])<1e-8,'scatter scale')
 def measurement(mask,q):
  if mask.sum()<3:ck(q is None,'measurement coverage');return
  weights=ee[mask]**-2;norm=weights/weights.sum();depth=-np.sum(norm*resid[mask]);vec=norm@X[mask];var=1/weights.sum()+vec@cov@vec;ck(abs(depth-q['depth'])<1e-9 and abs(np.sqrt(var)-q['error'])<1e-10 and abs(np.sqrt(var)*scale-q['scatter_scaled_error'])<1e-9,'baseline-propagated measurement')
 measurement(inside,m['depth']);measurement((xi> -1)&(xi<-.5),m['left_annulus']);measurement((xi>.5)&(xi<1),m['right_annulus'])
 for width in m['widths']:measurement(abs(xi)<width['width_multiple']/2,width['measurement'])
for r in result['rows']:
 verify(r,r['key'],r['center'],r['measurement'])
 for c in r['controls']:
  verify(r,c['key'],c['center'],c['measurement']);cm=c['measurement'];m=r['measurement'];matched=m['status']==cm['status']=='measured' and all(.8*m[k]<=cm[k]<=1.2*m[k] for k in ['n_inside','n_left','n_right']);ck(matched==c['matched'],'control matching')
  ck(len(c['injections'])==(2 if matched else 0),'all signed injections')
  for inj in c['injections']:
   verify(r,inj['key'],c['center'],inj['measurement'],inj['depth_injected']);ck(abs(inj['measurement']['depth']['depth']-cm['depth']['depth']-inj['depth_injected'])<1e-10,'signed injection transfer')
ck(nf==result['n_saved_fits'],'saved fit accounting');save_json(p/'verification.json',dict(status='passed',checks=len(checks),verified_fits=nf,check_types=sorted(set(checks)),limits='Independent QR/raw reconstruction; same NumPy and FITS reader. No red-noise calibration/host validation.'));print('PASS',len(checks),'fits',nf)
