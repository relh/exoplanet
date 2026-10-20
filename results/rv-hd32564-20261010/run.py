import csv,json
from pathlib import Path
import numpy as np
from astropy.time import Time
from exoplanet.rv_search import fit,scan,refine,design
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;path=Path('data/rv/HD32564.csv')
rows=list(csv.DictReader(path.open()));data={k:np.array([float(r[k]) for r in rows]) for k in rows[0] if k not in ['target','TIMEID','MASK','PROGID','PROGPI','OBHAB','THAR_FP','DPR_TYPE']}
# HARPS fiber change: separate pre/post offsets. No RV-dependent clipping.
cut=2457163.;t=data['BJD'];groups=(t>=cut).astype(int)
valid=(data['f_RV']==0)&np.isfinite(t)&(data['e_RV_mlc_nzp']>0)&(data['e_RV_mlc_nzp']<100)&np.isfinite(data['RV_mlc_nzp'])
night=np.floor(t+.5).astype(int)
# Consecutive observations from one night count once. Formal precision combined;
# independent 2 m/s nightly jitter is a declared screening assumption.
series={}
for column,errorcol in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp'),('Halpha','e_Halpha'),('RHKp','dRHKp'),('BIS',None),('FWHM_DRS',None),('dLW','e_dLW')]:
 ts=[];ys=[];es=[];gs=[]
 for n in np.unique(night[valid]):
  mask=valid&(night==n)&np.isfinite(data[column])&(abs(data[column])<1e6)
  if errorcol:mask&=np.isfinite(data[errorcol])&(data[errorcol]>0)&(data[errorcol]<1e6)
  if not mask.any():continue
  w=1/data[errorcol][mask]**2 if errorcol else np.ones(mask.sum())
  ts.append(np.average(t[mask],weights=w));ys.append(np.average(data[column][mask],weights=w));es.append(1/np.sqrt(w.sum()) if errorcol else 1.);gs.append(int(groups[mask][0]))
 series[column]=[np.array(v) for v in [ts,ys,es,gs]]
rv=series['RV_mlc_nzp'];tt,yy,ee,gg=rv;ee=np.hypot(ee,2.)
# Freeze configuration before scanning. External period suggestions are known;
# temporal split is retrospective predictive validation, not a blind discovery.
split=np.quantile(tt,.75);train=tt<=split
save_json(out/'configuration.json',dict(created_utc=now(),input_sha256=sha(path),script_sha256=sha(Path(__file__)),module_sha256=sha(Path('src/exoplanet/rv_search.py')),instrument_boundary_bjd=cut,jitter_ms=2.,period_range=[.8,100],samples_per_peak=8,train_max_bjd=float(split),raw_rows=len(rows),nights=len(tt),external_periods_days=[2.6,11.1,23.6,49.1],status='Replication of externally reported lead; not our discovery; chronological split not blind to externally suggested periods'))
f=np.arange(1/100,1/.8,1/(8*np.ptp(tt)))
known=[];history=[]
for step in range(4):
 power=scan(tt,yy,ee,gg,f,known);indices=np.argsort(np.nan_to_num(power,nan=-np.inf))[::-1];peaks=[]
 for idx in indices:
  p=1/f[idx]
  if all(abs(f[idx]-1/x['period'])>3/np.ptp(tt) for x in peaks):peaks.append(dict(period=float(p),delta_chi2=float(power[idx])))
  if len(peaks)==8:break
 known.append(peaks[0]['period']);sol=refine(tt,yy,ee,gg,known,fraction=.001);known=list(sol['periods'])
 history.append(dict(step=step+1,peaks=peaks,periods=known,amplitudes=sol['amplitudes'].tolist(),chi2=sol['chi2']))
 np.savez_compressed(out/f'periodogram-{step+1}.npz',frequency=f,delta_chi2=power)
 print('step',step+1,known,sol['amplitudes'],flush=True)
# Separately fit reported modes; rounded periods are not precise enough over years.
reported=[2.6,11.1,23.6,49.1];picks=[]
for p in reported:
 local=f[(1/f>p*.97)&(1/f<p*1.03)]
 power=scan(tt[train],yy[train],ee[train],gg[train],local,picks)
 picks.append(float(1/local[np.nanargmax(power)]))
frozen=refine(tt[train],yy[train],ee[train],gg[train],picks,fraction=.001)
save_json(out/'frozen-training.json',{k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in frozen.items()})
# Train is pre-upgrade only. Validate pre-upgrade future points with unchanged
# coefficients; post-upgrade requires an unknown offset, reported separately.
held=(~train)&(gg==gg[train][0]);pred=design(tt[held],gg[held],frozen['periods'],frozen['epoch'])@frozen['coefficients']
base=fit(tt[train],yy[train],ee[train],gg[train],[])
basepred=design(tt[held],gg[held],[],base['epoch'])@base['coefficients']
validation=dict(n_train=int(train.sum()),n_held_preupgrade=int(held.sum()),n_postupgrade=int(np.sum((~train)&(gg!=gg[train][0]))),periods=frozen['periods'].tolist(),rms_model=float(np.sqrt(np.mean((yy[held]-pred)**2))),rms_baseline=float(np.sqrt(np.mean((yy[held]-basepred)**2))),delta_chi2=float(np.sum(((yy[held]-basepred)/ee[held])**2)-np.sum(((yy[held]-pred)/ee[held])**2)))
checks=[]
for name,(at,ay,ae,ag) in series.items():
 if name.startswith('RV_'):ae=np.hypot(ae,2.)
 full=fit(at,ay,ae,ag,known);null=fit(at,ay,ae,ag,[])
 checks.append(dict(column=name,n=len(at),chi2_null=null['chi2'],chi2_model=full['chi2'],amplitudes=full['amplitudes'].tolist(),periods=known,limitations='Activity significance not calibrated; some indicators lack errors. Shared observations across RV reductions.'))
np.savez_compressed(out/'nightly.npz',time=tt,rv=yy,error=ee,group=gg,train=train)
save_json(out/'analysis.json',dict(created_utc=now(),history=history,validation=validation,columns=checks))
print('validation',validation,flush=True)
