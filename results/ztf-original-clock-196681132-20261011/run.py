"""Post-inspection diagnostic at the preexisting TESS clock; no new validation set."""
from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json');dp=Path('results/ztf-search-196681132-20261011/processed.npz');b=json.loads(fp.read_text())['best'];z=np.load(dp);t,y,e,g,tr,h=[z[k] for k in ['t','flux','error','oid','training','hmjd']];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;events=np.rint((t-b['transit_time'])/b['period']).astype(int)
def measure(mask,epoch=b['transit_time'],season=False):
 tt=t[mask];yy=y[mask];ee=e[mask];gg=g[mask].astype(str)
 if season:gg=np.char.add(np.char.add(gg,':'),np.floor((h[mask]-58000)/365.25).astype(int).astype(str))
 inside=abs((tt-epoch+b['period']/2)%b['period']-b['period']/2)<b['duration']/2
 design=np.column_stack([(gg==v).astype(float) for v in np.unique(gg)]+[-inside.astype(float)]);a=design/ee[:,None];data=yy/ee
 if np.linalg.matrix_rank(a)<a.shape[1]:return {'status':'rank_deficient','n_inside':int(inside.sum())}
 co=np.linalg.lstsq(a,data,rcond=None)[0];cov=np.linalg.inv(a.T@a);err=np.sqrt(cov[-1,-1]);chi=float(np.sum((data-a@co)**2));dof=len(yy)-len(co)
 return {'status':'measured','n':len(yy),'n_inside':int(inside.sum()),'depth':float(co[-1]),'formal_error':float(err),'formal_snr':float(co[-1]/err),'chi2':chi,'dof':dof,'residual_scaled_snr':float(co[-1]/(err*np.sqrt(chi/dof))),'inside_events':sorted(set(events[mask][inside].tolist()))}
allmask=np.ones(len(t),bool);rows={name:measure(mask) for name,mask in [('all',allmask),('early',tr),('later',~tr)]};bands={str(oid):measure(g==oid) for oid in np.unique(g)};seasons=measure(allmask,season=True)
inside=abs(phase)<b['duration']/2;loo=[{'excluded_event':int(n),'measurement':measure(events!=n)} for n in np.unique(events[inside])]
controls=[{'phase_shift':float(frac),'measurement':measure(allmask,b['transit_time']+frac*b['period'])} for frac in np.linspace(.1,.9,41)]
fig,axes=plt.subplots(1,3,figsize=(14,4),constrained_layout=True)
for ax,(name,mask) in zip(axes,[('All',allmask),('Early',tr),('Later (previously opened)',~tr)]):
 ax.errorbar(phase[mask]*24,y[mask]-1,yerr=e[mask],fmt='.',ms=3,alpha=.5,lw=.4);ax.set(xlim=(-2,2),ylim=(-.12,.12),title=name,xlabel='Hours from original TESS clock',ylabel='Normalized flux minus1');ax.axvspan(-b['duration']*12,b['duration']*12,color='red',alpha=.15)
fig.savefig(p/'fold.png',dpi=140)
save_json(p/'results.json',{'inputs':{str(fp):sha(fp),str(dp):sha(dp),str(Path(__file__)):sha(Path(__file__))},'clock':b,'measurements':rows,'bands':bands,'object_season_intercepts':seasons,'leave_one_event_out':loo,'shifted_controls':controls,'inside_points':[{'index':int(i),'btjd':float(t[i]),'oid':int(g[i]),'flux':float(y[i]),'error':float(e[i]),'phase_days':float(phase[i]),'event':int(events[i])} for i in np.flatnonzero(inside)],'limits':'Post-inspection follow-up motivated by injected trials. Original TESS clock retained, but its propagated uncertainty is large. Later ZTF data already opened. Diagonal errors, approximate seasonal baselines, shifted controls not exchangeable; no calibrated FAP or new validation claim.'})
print(rows);print('bands',bands);print('season',seasons);print('loo range',min(x['measurement']['depth'] for x in loo),max(x['measurement']['depth'] for x in loo));print('controls exceed',sum(x['measurement'].get('formal_snr',-np.inf)>=rows['all']['formal_snr'] for x in controls))
