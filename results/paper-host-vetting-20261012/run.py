from pathlib import Path
import json,hashlib,datetime
import numpy as np
from astropy.io import fits
R=Path('results/paper-host-vetting-20261012'); plan=json.loads((R/'plan.json').read_text())
for p,h in plan['inputs'].items(): assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
rows=[];measurements=[]
for tic,sectors,catpath,clockpath in [(80387959,[10,36,37,63],'results/neighbors-80387959-20261009/tic-neighbors.json','results/strongest-80387959-shape-20261012/plan.json'),(402358350,[40,41,54,81],'results/neighbors-402358350-20261011/neighbors.json','results/strongest-402358350-baselines-20261012/plan.json')]:
 cat=json.loads(Path(catpath).read_text());target=next(x for x in cat if x['ID']==tic); cp=json.loads(Path(clockpath).read_text()); clock=cp.get('best',cp.get('clock'));P=clock['period'];D=clock['duration'];T=clock['transit_time']
 selected=[]
 for x in cat:
  ra1,dec1,ra2,dec2=np.deg2rad([target['ra'],target['dec'],x['ra'],x['dec']]); a=np.sin((dec1-dec2)/2)**2+np.cos(dec1)*np.cos(dec2)*np.sin((ra1-ra2)/2)**2;sep=float(np.rad2deg(2*np.arcsin(np.sqrt(a)))*3600)
  if sep<=150:selected.append((x,sep))
 for s in sectors:
  raw=f'data/lightcurves/s{s:04d}-{tic}.fits'
  with fits.open(raw) as h:
   z=h[1].data;hd=h[1].header;c=float(hd['CROWDSAP']);eta=float(hd['FLFRCSAP']); mask=(z['QUALITY']==0)&np.isfinite(z['TIME'])&np.isfinite(z['SAP_FLUX'])&np.isfinite(z['SAP_FLUX_ERR'])&(z['SAP_FLUX']>0)&(z['SAP_FLUX_ERR']>0); t=np.array(z['TIME'][mask]);y=np.array(z['SAP_FLUX'][mask],float);err=np.array(z['SAP_FLUX_ERR'][mask],float)
  norm=np.median(y);y/=norm;err/=norm;exposure=float(np.median(np.diff(t)));event=np.rint((t-T)/P).astype(int);dt=t-(T+event*P); cases=[];skipped=[]
  for e in np.unique(event):
   m=(event==e)&(abs(dt)<3*D); n_in=int(np.sum(m&(abs(dt)<D/2)));n_l=int(np.sum(m&(dt<-D/2)));n_r=int(np.sum(m&(dt>D/2)))
   if n_in>=2 and n_l>=5 and n_r>=5:cases.append(int(e))
   else:skipped.append({'event':int(e),'n_inside':n_in,'n_left':n_l,'n_right':n_r})
  m=np.isin(event,cases)&(abs(dt)<3*D);t,y,err,dt,event=[a[m] for a in [t,y,err,dt,event]]
  overlap=np.maximum(0,np.minimum(dt+exposure/2,D/2)-np.maximum(dt-exposure/2,-D/2))/exposure
  X=np.zeros((len(t),1+2*len(cases)));X[:,0]=-overlap
  for j,e in enumerate(cases):X[:,1+2*j]=(event==e);X[:,2+2*j]=(event==e)*dt/D
  A=X/err[:,None];b=y/err;beta=np.linalg.lstsq(A,b,rcond=None)[0];res=y-X@beta;chi=float(np.sum((res/err)**2));dof=len(y)-len(beta);cov=np.linalg.inv(A.T@A)*max(1,chi/dof)
  base=float(np.mean(beta[1::2]));depth=float(beta[0]/base);g=np.zeros(len(beta));g[0]=1/base;g[1::2]=-beta[0]/(base*base*len(cases));error=float(np.sqrt(g@cov@g))
  np.savez_compressed(R/f'{tic}-s{s}-sap.npz',time=t,flux=y,error=err,dt=dt,event=event,design=X,beta=beta,covariance=cov,residual=res)
  measurement={'tic':tic,'sector':s,'depth':depth,'error':error,'crowdsap':c,'flfrcsap':eta,'events':cases,'skipped':skipped,'median_flux':float(norm),'fitted_reference_baseline':base,'exposure_days':exposure,'chi2':chi,'dof':dof,'raw_path':raw};measurements.append(measurement)
  for x,sep in selected:
   o={'tic':tic,'sector':s,'neighbor':int(x['ID']),'gaia_dr2':x.get('GAIA'),'separation_arcsec':sep,'Tmag':x.get('Tmag'),'e_Tmag':x.get('e_Tmag'),'target_Tmag':target['Tmag'],'target_e_Tmag':target.get('e_Tmag'),'disposition':x.get('disposition'),'duplicate_id':x.get('duplicate_id')}
   if x.get('Tmag') is None: o['status']='missing_Tmag';rows.append(o);continue
   dm=x['Tmag']-target['Tmag'];r=10**(-.4*dm);q_min=depth/(c*r); is_target=x['ID']==tic
   q_max=1 if is_target else 1/eta
   # Non-target source cannot exceed the header's entire contaminant budget.
   q_budget=1 if is_target else (1-c)/(c*r)
   q_allowed=min(q_max,q_budget)
   sigma_dm=None if x.get('e_Tmag') is None or target.get('e_Tmag') is None else float(np.hypot(x['e_Tmag'],target['e_Tmag']))
   r_bright=r if sigma_dm is None else 10**(-.4*(dm-3*sigma_dm))
   shallow=max(0,depth-3*error);c_hi=min(1,c*1.1);eta_lo=max(.001,eta*.9)
   # Jointly require target+neighbor fractions <=1. Increasing c can hurt this budget;
   # report a lower bound allowing each optimistic factor separately, not an attainable joint case.
   optimistic=shallow*eta_lo/(c_hi*r_bright) if not is_target else shallow/c_hi
   o.update(status='conditional_model_only',delta_Tmag=dm,flux_ratio=r,delta_Tmag_sigma=sigma_dm,q_min_total_eclipse=q_min,q_upper_physical=q_max,q_upper_contamination_budget=q_budget,minimum_eclipse_fraction=depth/(c*r*q_allowed),optimistic_lower_bound=optimistic,nominal_requires_more_than_total_eclipse=depth/(c*r*q_allowed)>1,sensitivity_also_above_one=optimistic>1,equal_throughput_eclipse_fraction=depth/(c*r),q_grid=[])
   for q in ([1.] if is_target else [.25,.5,1.,1/eta]):
    o['q_grid'].append({'q':q,'required_eclipse_fraction':depth/(c*r*q),'within_throughput_and_budget':bool(q<=q_allowed*(1+1e-12))})
   rows.append(o)
(R/'results.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':hashlib.sha256((R/'plan.json').read_bytes()).hexdigest(),'measurements':measurements,'neighbors':rows},indent=2)+'\n')
print('measurements',len(measurements),'source-sector rows',len(rows))
for m in measurements:print(m['tic'],m['sector'],m['depth']*1e6,m['error']*1e6)
