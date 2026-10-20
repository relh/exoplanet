"""Fixed original TESS clocks for the other two signals; no retiming or exclusion."""
from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;catalog=Path('results/ztf-catalog-route-20261011/catalog-results.json');cat=json.loads(catalog.read_text());inputs={str(catalog):sha(catalog),str(Path(__file__)):sha(Path(__file__))};output=[];fig,axes=plt.subplots(2,3,figsize=(14,8),constrained_layout=True)
def measure(t,y,e,g,b,mask,offset=0):
 tt=t[mask];yy=y[mask];ee=e[mask];gg=g[mask];phase=(tt-b['transit_time']-offset+b['period']/2)%b['period']-b['period']/2;inside=abs(phase)<b['duration']/2
 if len(tt)==0:return {'status':'no_observations','n':0,'n_inside':0}
 x=np.column_stack([(gg==oid).astype(float) for oid in np.unique(gg)]+[-inside.astype(float)]);a=x/ee[:,None];v=yy/ee
 if np.linalg.matrix_rank(a)<a.shape[1]:return {'status':'rank_deficient','n':len(tt),'n_inside':int(inside.sum())}
 coeff=np.linalg.lstsq(a,v,rcond=None)[0];cov=np.linalg.inv(a.T@a);err=float(np.sqrt(cov[-1,-1]));chi=float(np.sum((v-a@coeff)**2));dof=len(v)-a.shape[1]
 return {'status':'measured','depth':float(coeff[-1]),'formal_error':err,'formal_snr':float(coeff[-1]/err),'chi2':chi,'dof':dof,'residual_scaled_snr':float(coeff[-1]/err/np.sqrt(chi/dof)),'n':len(tt),'n_inside':int(inside.sum()),'inside_events':sorted(set(np.rint((tt[inside]-b['transit_time']-offset)/b['period']).astype(int).tolist()))}
for i,tic in enumerate([241928959,422626648]):
 fp=Path(f'results/qlp-faint-midradius-single-review-20261011/{tic}-peak0/frozen.json');inputs[str(fp)]=sha(fp);b=json.loads(fp.read_text())['best'];oids=sorted(int(x['oid']) for row in cat if row['tic']==tic for x in row['rows']);arrays=[[] for _ in range(7)]
 for oid in oids:
  file=Path(f'data/ztf/cloud-dr24-{oid}.json');tp=Path(f'results/ztf-timing-20261011/{oid}-timing.npz');inputs[str(file)]=sha(file);inputs[str(tp)]=sha(tp);obj=json.loads(file.read_text());z=np.load(tp)
  good=[x for x in obj['lightcurve'] if x['catflags']==0 and all(x[k] is not None and np.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0];mag=np.array([x['mag'] for x in good]);err=np.array([x['magerr'] for x in good]);h=np.array([x['hmjd'] for x in good]);np.testing.assert_array_equal(h,z['hmjd'])
  # Full-object normalization is only a scale choice; separate fitted intercepts follow.
  flux=10**(-.4*(mag-np.median(mag)));error=flux*np.log(10)*.4*err
  for a,v in zip(arrays,[z['btjd_assume_utc'],flux,error,[oid]*len(h),h,[obj['filterid']]*len(h),z['btjd_assume_tdb']]):a.extend(v)
 t,y,e,g,h,band,tdb=map(np.array,arrays);allmask=np.ones(len(t),bool);early=h<60000;sets=[('all',allmask),('early',early),('later',~early)];rows={name:measure(t,y,e,g,b,mask) for name,mask in sets};bands={str(k):measure(t,y,e,g,b,band==k) for k in np.unique(band)};scale=measure(tdb,y,e,g,b,allmask);controls=[{'shift_fraction':float(f),'measurement':measure(t,y,e,g,b,allmask,f*b['period'])} for f in np.linspace(.1,.9,41)]
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;inside=abs(phase)<b['duration']/2
 synthetic=1+.1*np.searchsorted(np.unique(g),g)-.02*inside;test=measure(t,synthetic,e,g,b,allmask);assert test['status']=='measured';np.testing.assert_allclose(test['depth'],.02,atol=1e-12)
 np.savez_compressed(p/f'{tic}-processed.npz',t=t,flux=y,error=e,oid=g,hmjd=h,band=band,t_assume_tdb=tdb)
 for ax,(name,mask) in zip(axes[i],sets):
  ax.errorbar(phase[mask]*24,y[mask]-1,yerr=e[mask],fmt='.',alpha=.4,ms=3,lw=.4);ax.axvspan(-b['duration']*12,b['duration']*12,color='red',alpha=.15);ax.set(xlim=(-2,2),ylim=(-.12,.12),title=f'{tic}: {name}',xlabel='Hours from original TESS clock',ylabel='Flux minus1')
 output.append({'tic':tic,'clock':b,'measurements':rows,'bands':bands,'assume_tdb':scale,'shifted_controls':controls,'synthetic_depth_recovery':test['depth']});print(tic,rows,flush=True)
fig.savefig(p/'folds.png',dpi=140);save_json(p/'results.json',{'inputs':inputs,'targets':output,'limits':'Original clocks unchanged. Broad TESS prediction uncertainty makes nominal phase unreliable far from TESS. No new blind validation or calibrated FAP. Early/later are descriptive; normalization uses full-object median. Rank deficiency means absent contrast, not zero depth. No photometric outlier clipping.'})
