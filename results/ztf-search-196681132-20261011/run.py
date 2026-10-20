"""Exploratory TESS-period-guided ZTF search with a chronological reserved set."""
from pathlib import Path
import json,numpy as np
from astropy.timeseries import BoxLeastSquares
from exoplanet.pipeline import save_json,sha,now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json');f=json.loads(fp.read_text());b=f['best'];r=f['timing_ranges'];oids=[373107100003951,373207100006067,373307100008379]
inputs=[fp]+[Path(f'data/ztf/cloud-dr24-{oid}.json') for oid in oids]+[Path(f'results/ztf-timing-20261011/{oid}-timing.npz') for oid in oids]
plan={'created':now(),'script_sha256':sha(Path(__file__)),'inputs':{str(x):sha(x) for x in inputs},'split_hmjd':60000,'period_min':r['period_min'],'period_max':r['period_max'],'n_periods':2049,'durations':[b['duration']*a for a in [.8,1,1.2]],'injection_depths':[.01,.02,.04],'injection_period':b['period'],'injection_epoch':b['transit_time'],'policy':'Existing TESS period range; free epoch search on HMJD<60000 only. Freeze strongest training peak before measuring later data. No further optimization on reserved data. Conditional assumed-UTC converted times; not original TESS-clock validation. Training-median normalization per oid; no outlier clipping.'}
assert not (p/'plan.json').exists();save_json(p/'plan.json',plan)
ts=[];ys=[];es=[];gs=[];hs=[]
for oid in oids:
 o=json.loads(Path(f'data/ztf/cloud-dr24-{oid}.json').read_text());good=[x for x in o['lightcurve'] if x['catflags']==0 and all(x[k] is not None and np.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0]
 z=np.load(f'results/ztf-timing-20261011/{oid}-timing.npz');h=np.array([x['hmjd'] for x in good]);np.testing.assert_array_equal(h,z['hmjd']);mag=np.array([x['mag'] for x in good]);err=np.array([x['magerr'] for x in good]);median=np.median(mag[h<60000]);flux=10**(-.4*(mag-median));dy=flux*np.log(10)*.4*err
 ts.extend(z['btjd_assume_utc']);ys.extend(flux);es.extend(dy);hs.extend(h);gs.extend([oid]*len(h))
t,y,e,h,g=map(np.array,[ts,ys,es,hs,gs]);train=h<60000;periods=np.linspace(r['period_min'],r['period_max'],2049)
def search(flux):
 result=BoxLeastSquares(t[train],flux[train],e[train]).power(periods,plan['durations'],objective='likelihood',oversample=50)
 i=int(np.argmax(result.power));return {k:float(result[k][i]) for k in ['period','transit_time','duration','depth','depth_err','depth_snr','power']}
def measure(mask,clock,flux=y):
 tt=t[mask];gg=g[mask];yy=flux[mask];ee=e[mask];phase=(tt-clock['transit_time']+clock['period']/2)%clock['period']-clock['period']/2;inside=abs(phase)<clock['duration']/2
 x=np.column_stack([(gg==v).astype(float) for v in np.unique(gg)]+[-inside.astype(float)])
 a=x/ee[:,None];v=yy/ee
 if np.linalg.matrix_rank(a)<x.shape[1]:return {'status':'rank_deficient','n':len(tt),'n_inside':int(inside.sum())}
 coeff=np.linalg.lstsq(a,v,rcond=None)[0];cov=np.linalg.inv(a.T@a);err=float(np.sqrt(cov[-1,-1]));events=np.rint((tt[inside]-clock['transit_time'])/clock['period']).astype(int)
 return {'status':'measured','depth':float(coeff[-1]),'formal_error':err,'formal_snr':float(coeff[-1]/err),'n':len(tt),'n_inside':int(inside.sum()),'inside_event_numbers':sorted(set(events.tolist())),'chi2':float(np.sum((a@coeff-v)**2)),'dof':len(tt)-x.shape[1]}
best=search(y);save_json(p/'frozen.json',{'created':now(),'best':best,'plan_sha256':sha(p/'plan.json'),'training':measure(train,best),'policy':'Written before reserved-data measurement. Selected training power is not a calibrated significance.'})
held=measure(~train,best);bands={str(oid):measure((~train)&(g==oid),best) for oid in oids}
controls=[]
for depth in plan['injection_depths']:
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 injected=y-depth*(abs(phase)<b['duration']/2)
 found=search(injected);phase_offset=abs((found['transit_time']-b['transit_time']+b['period']/2)%b['period']-b['period']/2)
 controls.append({'depth':depth,'best':found,'period_fractional_error':abs(found['period']/b['period']-1),'epoch_offset_modulo_injected_period_days':float(phase_offset),'reserved':measure(~train,found,injected)})
np.savez_compressed(p/'processed.npz',t=t,flux=y,error=e,hmjd=h,oid=g,training=train)
fig,axes=plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
for ax,mask,title in zip(axes,[train,~train],['Discovery before HMJD60000','Reserved HMJD60000 onward']):
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
 ax.errorbar(phase[mask]*24,y[mask]-1,yerr=e[mask],fmt='.',ms=3,alpha=.45,lw=.4);ax.axvspan(-best['duration']*12,best['duration']*12,color='red',alpha=.15);ax.set(title=title,xlabel='Hours from selected training ephemeris',ylabel='Normalized flux minus1')
fig.savefig(p/'fold.png',dpi=140)
save_json(p/'results.json',{'best':best,'training':measure(train,best),'reserved':held,'reserved_by_oid':bands,'injections':controls,'limits':'Guided exploratory search, not original TESS-clock validation. Formal errors ignore correlated systematics. Sparse sampling and period uncertainty remain; no FAP or physical classification. Injections added to real data, not completeness estimates. Cloud count discrepancies unresolved.'});print(json.dumps({'best':best,'training':measure(train,best),'reserved':held,'controls':controls},indent=2))
