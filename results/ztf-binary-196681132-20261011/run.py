from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json');dp=Path('results/ztf-search-196681132-20261011/processed.npz');b=json.loads(fp.read_text())['best'];z=np.load(dp);t,y,e,g,tr,h=[z[k] for k in ['t','flux','error','oid','training','hmjd']]
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;cycle=np.rint((t-b['transit_time'])/b['period']).astype(int);inside=abs(phase)<b['duration']/2;secondary=abs(abs(phase)-b['period']/2)<b['duration']/2
indicators=np.array([inside&(cycle%2==0),inside&(cycle%2==1),secondary]).T
names=['even_primary','odd_primary','half_phase']
def fit(mask,season=False,flux=y):
 gg=g[mask].astype(str)
 if season:gg=np.char.add(np.char.add(gg,':'),np.floor((h[mask]-58000)/365.25).astype(int).astype(str))
 x=np.column_stack([(gg==v).astype(float) for v in np.unique(gg)]+[-indicators[mask,k].astype(float) for k in range(3)]);a=x/e[mask,None];v=flux[mask]/e[mask];rank=np.linalg.matrix_rank(a)
 if rank<x.shape[1]:return {'status':'rank_deficient','counts':indicators[mask].sum(axis=0).tolist()}
 coeff=np.linalg.lstsq(a,v,rcond=None)[0];cov=np.linalg.inv(a.T@a);chi=float(np.sum((a@coeff-v)**2));dof=len(v)-len(coeff);factor=np.sqrt(chi/dof);depth=coeff[-3:];errors=np.sqrt(np.diag(cov)[-3:]);delta=depth[0]-depth[1];deltaerr=np.sqrt(cov[-3,-3]+cov[-2,-2]-2*cov[-3,-2])
 return {'status':'measured','counts':indicators[mask].sum(axis=0).tolist(),'depths':dict(zip(names,depth.tolist())),'formal_errors':dict(zip(names,errors.tolist())),'formal_snr':dict(zip(names,(depth/errors).tolist())),'residual_scaled_snr':dict(zip(names,(depth/errors/factor).tolist())),'even_minus_odd':float(delta),'difference_formal_error':float(deltaerr),'difference_formal_snr':float(delta/deltaerr),'difference_scaled_snr':float(delta/deltaerr/factor),'chi2':chi,'dof':dof,'covariance_depths':cov[-3:,-3:].tolist()}
allmask=np.ones(len(t),bool);rows={name:fit(mask) for name,mask in [('all',allmask),('early',tr),('later',~tr)]};rows['seasonal']=fit(allmask,True);bands={str(oid):fit(g==oid) for oid in np.unique(g)}
# Unequal synthetic primaries and secondary with different object baselines.
truth=np.array([.02,.04,.01]);synthetic=1+.1*np.searchsorted(np.unique(g),g)-indicators@truth;control=fit(allmask,flux=synthetic);np.testing.assert_allclose(list(control['depths'].values()),truth,atol=1e-12)
fig,axes=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
for k,ax in enumerate(axes):
 if k<2:
  mask=cycle%2==k;plotphase=phase
 else:
  mask=allmask;plotphase=(t-(b['transit_time']+b['period']/2)+b['period']/2)%b['period']-b['period']/2
 ax.errorbar(plotphase[mask]*24,y[mask]-1,yerr=e[mask],fmt='.',ms=3,alpha=.4,lw=.4);ax.axvspan(-b['duration']*12,b['duration']*12,color='red',alpha=.15);ax.set(xlim=(-2,2),ylim=(-.12,.12),title=names[k],xlabel='Hours from fixed center',ylabel='Normalized flux minus1')
fig.savefig(p/'diagnostics.png',dpi=140)
save_json(p/'results.json',{'inputs':{str(fp):sha(fp),str(dp):sha(dp),str(Path(__file__)):sha(Path(__file__))},'clock':b,'measurements':rows,'bands':bands,'synthetic_control':control,'limits':'Post-inspection fixed-clock diagnostics, not a new blind validation. Half-phase test assumes circular timing and same duration; eccentric/unequal-duration binaries not excluded. Sparse observations and uncertain propagated clock; correlated errors and unknown blends not modeled.'});print(rows)
