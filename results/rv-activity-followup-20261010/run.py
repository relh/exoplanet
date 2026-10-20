import csv,json
from pathlib import Path
import numpy as np
from exoplanet.rv_search import fit,scan
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;screen={r['name']:r for r in json.loads(Path('results/rv-coverage-search-20261010/screening.json').read_text())['results']};results=[]
for name in ['HD95542','HD297396','HD157172','HD16008','HD41248']:
 source=Path('data/rv/coverage-selected')/(name+'.csv');raw=list(csv.DictReader(source.open()));periods=screen[name]['frozen_solution']['periods'];columns=[]
 for col in ['RV_mlc_nzp','RV_drs_nzp','RHKp','Halpha','BIS','FWHM_DRS','dLW','CRX']:
  a=np.array([[float(r['BJD']),float(r[col])] for r in raw if float(r['f_RV'])==0]);valid=np.isfinite(a).all(axis=1)&(abs(a[:,1])<1e6);a=a[valid];days=np.floor(a[:,0]+.5);b=np.array([[np.mean(a[days==n,0]),np.mean(a[days==n,1])] for n in np.unique(days)]);t,y=b.T;g=(t>=2457163).astype(int);e=np.ones(len(t))*np.std(y)
  baseline=fit(t,y,e,g,[]);full=fit(t,y,e,g,periods);frequency=np.arange(1/300,1/2,1/(6*np.ptp(t)));power=scan(t,y,e,g,frequency);indices=np.argsort(power)[::-1];peaks=[]
  for i in indices:
   if all(abs(frequency[i]-1/r['period'])>3/np.ptp(t) for r in peaks):peaks.append(dict(period=float(1/frequency[i]),delta_chi2=float(power[i])))
   if len(peaks)==5:break
  drops=[]
  for i,p in enumerate(periods):
   reduced=fit(t,y,e,g,periods[:i]+periods[i+1:]);drops.append(dict(period=p,delta_chi2=reduced['chi2']-full['chi2']))
  columns.append(dict(column=col,nights=len(t),peaks=peaks,component_improvements=drops))
  if col in ['RV_mlc_nzp','RHKp','FWHM_DRS']:print(name,col,[(round(r['period'],3),round(r['delta_chi2'],1)) for r in peaks[:3]],flush=True)
 results.append(dict(name=name,input_sha256=sha(source),columns=columns))
 save_json(out/'activity.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),results=results,limitations='All already-opened nights, post-hoc follow-up. Equal-weight nightly means, full-series standard-deviation scaling, offsets/trend, 2–300day activity scan. Peaks and conditional improvements not significance; no red-noise calibration. RV aliases below2days not in this diagnostic grid.'))
