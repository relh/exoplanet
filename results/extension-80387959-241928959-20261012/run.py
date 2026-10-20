from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;plan=json.loads((O/'plan.json').read_text());rng=np.random.default_rng(plan['rng_seed']);rows=[]
for target in plan['targets']:
 b=target['seed'];tic=target['tic']
 for inp in target['inputs']:
  raw=Path(inp['path']);assert sha(raw)==inp['sha256']
  with fits.open(raw) as hd:
   assert hd[0].header['TICID']==tic and hd[0].header['SECTOR']==inp['sector'];d=hd[1].data
   for col in ['SAP_FLUX','DET_FLUX' if 'DET_FLUX' in d.names else 'KSPSAP_FLUX']:
    tt=np.array(d['TIME'],float);yy=np.array(d[col],float);keep=(d['QUALITY']==0)&np.isfinite(tt)&np.isfinite(yy)&(yy>0);tt,yy=tt[keep],yy[keep];order=np.argsort(tt);tt,yy=tt[order],yy[order];med=np.median(yy);yy=yy/med
    phase=(tt-b['transit_time'])/b['period'];dist=abs((phase+.5)%1-.5)*b['period'];dist2=abs(phase%1-.5)*b['period'];keep=(dist>1.5*b['duration'])&(dist2>1.5*b['duration']);tt,yy=tt[keep],yy[keep]
    bins=np.floor((tt-tt[0])/plan['bin_days']).astype(int);u,inv=np.unique(bins,return_inverse=True);cnt=np.bincount(inv);t=np.bincount(inv,weights=tt)/cnt;y=np.bincount(inv,weights=yy)/cnt-1
    segment=np.cumsum(np.r_[0,np.diff(t)>.5]);phi=(t-b['transit_time'])/b['period'];cycles=np.floor(phi+.5).astype(int);H=np.column_stack([np.cos(2*np.pi*phi),np.sin(2*np.pi*phi),np.cos(4*np.pi*phi),np.sin(4*np.pi*phi)])
    for degree in plan['polynomial_degrees']:
     B=[]
     for s in np.unique(segment):
      ix=segment==s;x=(t-np.mean(t[ix]))/max(np.ptp(t[ix]),1)
      for k in range(degree+1):B.append(np.where(ix,x**k,0))
     X=np.column_stack(B+[H[:,j] for j in range(4)]);beta,_,rank,sv=np.linalg.lstsq(X,y,rcond=None);res=y-X@beta;pinv=np.linalg.pinv(X);boot=[]
     for block in plan['block_days']:
      vals=[];length=max(1,round(block/plan['bin_days']))
      for draw in range(plan['draws']):
       rr=np.zeros(len(y))
       for s in np.unique(segment):
        ix=np.flatnonzero(segment==s);n=len(ix);starts=rng.integers(0,n,size=int(np.ceil(n/length)));indices=((starts[:,None]+np.arange(length))%n).ravel()[:n];rr[ix]=res[ix][indices]
       vals.append((pinv@rr)[-4:])
      vals=np.array(vals);boot.append(dict(block_days=block,coefficient_sd_ppm=(np.std(vals,axis=0,ddof=1)*1e6).tolist(),coefficient_cov_ppm2=(np.cov(vals.T)*1e12).tolist()))
     jack=[]
     for cyc in np.unique(cycles):
      mask=cycles!=cyc;bb,_,rk,_=np.linalg.lstsq(X[mask],y[mask],rcond=None);jack.append(dict(omitted_cycle=int(cyc),rank=int(rk),coefficients_ppm=(bb[-4:]*1e6).tolist()))
     inj=[]
     for j in range(4):
      bj=np.linalg.lstsq(X,y+.001*H[:,j],rcond=None)[0];inj.append(((bj[-4:]-beta[-4:])*1e6).tolist())
     name=f'{tic}-s{inp["sector"]}-{col}-d{degree}';np.savez_compressed(O/f'{name}.npz',t=t,y=y,X=X,beta=beta,segment=segment,cycles=cycles)
     rows.append(dict(name=name,tic=tic,sector=inp['sector'],column=col,degree=degree,n=len(y),rank=int(rank),n_parameters=X.shape[1],condition=float(sv[0]/sv[-1]),coefficients_ppm=(beta[-4:]*1e6).tolist(),amplitudes_ppm=[float(np.linalg.norm(beta[-4:-2])*1e6),float(np.linalg.norm(beta[-2:])*1e6)],residual_rms_ppm=float(np.std(res)*1e6),bootstrap=boot,orbit_omission=jack,injection_recovered_coefficients_ppm=inj,npz_sha256=sha(O/f'{name}.npz')))
     print(name,rows[-1]['coefficients_ppm'],flush=True)
     save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows))
