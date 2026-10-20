from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,now,sha
p=Path(__file__).parent;clockpath=Path('results/expanded-402358350-20261011/frozen-for81.json');b=json.loads(clockpath.read_text())['rows'][0]['best'];paths=[Path(f'data/lightcurves/s{s:04d}-402358350.fits') for s in [40,41,54,81]]
if not (p/'plan.json').exists():save_json(p/'plan.json',dict(created_utc=now(),clock=b,inputs={str(x):sha(x) for x in paths+[clockpath,Path(__file__)]},sectors=[40,41,54,81],streams=['SAP','PDCSAP'],baseline_degrees=[0,1,2],baseline_outer_duration_multiples=[3,5],mask_duration_multiple=1,width_multiples=[.5,.75,1,1.25,1.5,2],control_offsets=[-.4,-.25,.25,.4],control_match_fraction=[.8,1.2],injection_depths=[-.0006,.0006],policy='Alreadyopenedraw40/41/54/81 only; no downloads/clockrefit/runningmedian. Commonfinitepositivequality0 SAP/PDC mask. Flux/error normalizedbysectorstreammedian. For each nominalevent intersectingdata, outsidebaseline D<abs(dt)<outer*D; >=10points eachside and>=3insideD/2 required. Errorfloor robustadjacentdifferenceMAD onbaseline pairs separated<1.5mediansectorcadence, maxpublishedsigma. Polynomialfittedonlyoutofevent; nooutlierclipping. Propagatebaselinecovariance intoboxdepth, also scatter-scaledcovariance/error; allwidths/methods retained. Annuli D/2<abs(dt)<D protectedfrombaseline. Controls usefrozennonzero phaseoffsets andmatchinginside/left/right counts80-120percent; unmatched/failedkept. Injectadditive±600ppm boxes intoalready-normalized selectedarchivedproduct atcontrolcenters, re-runlocalfit identically; doesnotrerunupstreamPDC. No thresholdsinterpretedplanetprobability. Durationmeasurements exploratory fixedcenter only, notclockupdates.'))
plan=json.loads((p/'plan.json').read_text());rows=[];arrays={};counter=0
for s,path in zip(plan['sectors'],paths):
 with fits.open(path) as h:
  assert h[0].header['TICID']==402358350 and h[0].header['SECTOR']==s;d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
  for name in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[name])&(d[name]>0)
  t=np.array(d['TIME'][mask],float)
  for kind in plan['streams']:
   y=np.array(d[kind+'_FLUX'][mask],float);e=np.array(d[kind+'_FLUX_ERR'][mask],float);med=np.median(y);arrays[(s,kind)]=(t,y/med,e/med)

def fit(t,y,e,center,degree,outer,key):
 global counter
 dt=(t-center)/b['duration'];use=abs(dt)<outer;x=dt[use];yy=y[use];ee=e[use];tt=t[use];inside=abs(x)<.5;left=x<-1;right=x>1;oo=left|right;m=dict(n_inside=int(inside.sum()),n_left=int(left.sum()),n_right=int(right.sum()),status='insufficient_coverage')
 if min(left.sum(),right.sum())<10 or inside.sum()<3:return m
 oidx=np.where(oo)[0];pairs=(np.diff(tt[oidx])<1.5*np.median(np.diff(t)))&(np.diff(tt[oidx])>0);diff=np.diff(yy[oidx])[pairs];floor=1.4826*np.median(abs(diff-np.median(diff)))/np.sqrt(2) if len(diff)>=10 else 0;ee=np.maximum(ee,floor);X=np.column_stack([x**j for j in range(degree+1)]);A=X[oo]/ee[oo,None];coef=np.linalg.lstsq(A,yy[oo]/ee[oo],rcond=None)[0];cov=np.linalg.inv(A.T@A);resid=yy-X@coef;chi=float(np.sum((resid[oo]/ee[oo])**2));scale=max(1,np.sqrt(chi/(oo.sum()-len(coef))));widths=[]
 def measure(mask):
  if mask.sum()<3:return None
  w=1/ee[mask]**2;v=np.average(X[mask],axis=0,weights=w);depth=-np.average(resid[mask],weights=w);error=np.sqrt(1/w.sum()+v@cov@v);return dict(n=int(mask.sum()),depth=float(depth),error=float(error),scatter_scaled_error=float(error*scale))
 for width in plan['width_multiples']:widths.append(dict(width_multiple=width,measurement=measure(abs(x)<width/2)))
 m.update(status='measured',coefficients=coef.tolist(),covariance=cov.tolist(),baseline_chi2=chi,baseline_dof=int(oo.sum()-len(coef)),scatter_scale=float(scale),noise_floor=float(floor),depth=measure(inside),left_annulus=measure((x> -1)&(x<-.5)),right_annulus=measure((x>.5)&(x<1)),widths=widths)
 np.savez_compressed(p/f'{key}.npz',x=x,y=yy,e=ee,X=X,outside=oo,inside=inside);counter+=1;return m
for (s,kind),(t,y,e) in arrays.items():
 events=range(int(np.ceil((min(t)-b['transit_time'])/b['period'])),int(np.floor((max(t)-b['transit_time'])/b['period']))+1)
 for event in events:
  center=b['transit_time']+event*b['period']
  for degree in plan['baseline_degrees']:
   for outer in plan['baseline_outer_duration_multiples']:
    key=f's{s}-{kind}-e{event}-deg{degree}-r{outer}';m=fit(t,y,e,center,degree,outer,key);row=dict(key=key,sector=s,kind=kind,event=event,center=center,degree=degree,outer=outer,measurement=m,controls=[])
    for offset in plan['control_offsets']:
     c=center+offset*b['period'];ckey=key+f'-shift{offset}';cm=fit(t,y,e,c,degree,outer,ckey);matched=m['status']==cm['status']=='measured' and all(.8*m[n]<=cm[n]<=1.2*m[n] for n in ['n_inside','n_left','n_right']);ctr=dict(key=ckey,offset=offset,center=c,matched=matched,measurement=cm,injections=[])
     if matched:
      for amplitude in plan['injection_depths']:
       yi=y.copy();yi[abs(t-c)<b['duration']/2]-=amplitude;ikey=ckey+f'-inj{amplitude}';im=fit(t,yi,e,c,degree,outer,ikey);ctr['injections'].append(dict(key=ikey,depth_injected=amplitude,measurement=im))
     row['controls'].append(ctr)
    rows.append(row)
save_json(p/'results.json',dict(created_utc=now(),plan_sha256=sha(p/'plan.json'),rows=rows,n_saved_fits=counter,limits='Allmethods/clocksselectedbeforecalculation; theseepochs werepreviouslyinspected. Localbaselinesandwhite/scatter-scalederrors notred-noisecalibration orhosttest.'))
print('rows',len(rows),'savedfits',counter)
