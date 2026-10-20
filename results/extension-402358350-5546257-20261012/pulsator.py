from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());b=plan['clock402'];freq=plan['published_frequency402'];out=[];inject=[]
for name,h in plan['inputs'].items():assert sha(Path(name))==h
def model(t,y,e,sec,nuisance):
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;event=np.rint((t-b['transit_time'])/b['period']).astype(int);inside=abs(phase)<b['duration']/2;use=inside|((abs(phase)>b['duration'])&(abs(phase)<3*b['duration']));t=t[use];y=y[use];e=e[use];sec=sec[use];event=event[use];inside=inside[use];events=sorted(set(zip(sec.tolist(),event.tolist())));cols=[((sec==s)&(event==n)).astype(float) for s,n in events];names=[f'event{s}:{n}' for s,n in events]
 if nuisance:
  for s in sorted(set(sec)):
   cols.extend([np.sin(2*np.pi*freq*t)*(sec==s),np.cos(2*np.pi*freq*t)*(sec==s)]);names.extend([f'sin{s}',f'cos{s}'])
 cols.append(-inside.astype(float));names.append('depth');X=np.column_stack(cols);A=X/e[:,None];coef=np.linalg.lstsq(A,y/e,rcond=None)[0];cov=np.linalg.inv(A.T@A);res=(y-X@coef)/e;return dict(n=len(t),n_inside=int(inside.sum()),names=names,coef=coef.tolist(),depth=float(coef[-1]),error=float(np.sqrt(cov[-1,-1])),chi2=float(res@res),dof=len(t)-len(coef),rank=int(np.linalg.matrix_rank(A)),condition=float(np.linalg.cond(A))),dict(t=t,y=y,e=e,sec=sec,X=X)
for kind in ['SAP','PDCSAP']:
 for w in [1.5,2.5]:
  arrays=[]
  for s in [40,41,54,81]:
   z=np.load(f'results/sap-pdc-402358350-20261011/{kind}-{w}-s{s}.npz');arrays.append((z['t'],z['y'],z['e'],np.full(len(z['t']),s)))
  for selection in [40,41,54,81,'all']:
   chosen=arrays if selection=='all' else [arrays[[40,41,54,81].index(selection)]];t,y,e,sec=[np.concatenate([a[k] for a in chosen]) for k in range(4)]
   for nuisance in [False,True]:
    m,a=model(t,y,e,sec,nuisance);key=f'{kind}-{w}-{selection}-{int(nuisance)}';np.savez_compressed(p/f'fit-{key}.npz',**a);out.append(dict(key=key,kind=kind,window=w,sector=selection,nuisance=nuisance,**m))
  for s in [40,41,54,81]:
   with fits.open(f'data/lightcurves/s{s:04d}-402358350.fits') as h:
    d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
    for k in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[k])&(d[k]>0)
    rawt=np.array(d['TIME'][mask],float);rawy=np.array(d[kind+'_FLUX'][mask],float);rawe=np.array(d[kind+'_FLUX_ERR'][mask],float)
   t0,y0,e0=flatten(rawt,rawy,rawe,window=w)
   for phase in [0,np.pi/2,np.pi,3*np.pi/2]:
    t1,y1,e1=flatten(rawt,rawy*(1+.001*np.sin(2*np.pi*freq*rawt+phase)),rawe,window=w);common,a0,a1=np.intersect1d(t0,t1,return_indices=True);se=np.full(len(common),s);m0,_=model(common,y0[a0],e0[a0],se,False);m1,_=model(common,y1[a1],e0[a0],se,False);key=f'{kind}-{w}-{s}-{phase:.4f}';np.savez_compressed(p/f'inject-{key}.npz',t=common,y0=y0[a0],y1=y1[a1],e=e0[a0]);inject.append(dict(key=key,kind=kind,window=w,sector=s,phase=phase,amplitude=.001,baseline_clean=len(t0),injected_clean=len(t1),common_clean=len(common),depth_change=m1['depth']-m0['depth'],baseline_depth=m0['depth'],injected_depth=m1['depth'],fractional_transfer=(m1['depth']-m0['depth'])/.001))
save_json(p/'pulsator-results.json',dict(created_utc=now(),plan_sha256=sha(p/'plan.json'),fits=out,injections=inject,limitations='Retrospective fixed clock and frequency. Sinusoids/per-event baselines are nuisance models, not source attribution. Injection transfer tested only fourphases1000ppm; nonlinear and amplitude-dependent. Common point sets and baselineerrors isolate processing response; no claimFAP.'))
print('fits',len(out),'injections',len(inject));print([(r['key'],r['depth'],r['error']) for r in out if r['sector']=='all'])
