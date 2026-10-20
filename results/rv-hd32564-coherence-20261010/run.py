import csv,json
from pathlib import Path
import numpy as np
from astropy.time import Time
from exoplanet.rv_search import refine,predict
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('data/rv/HD32564.csv');raw=list(csv.DictReader(source.open()))
periods=[2.55663,11.06327,23.61185,49.10219]
results=[]
for column,ecol in [('RV_mlc_nzp','e_RV_mlc_nzp'),('RV_drs_nzp','e_RV_drs_nzp')]:
 good=[r for r in raw if float(r['f_RV'])==0 and float(r['BJD'])<2457163 and 0<float(r[ecol])<100 and np.isfinite(float(r[column]))]
 tt=np.array([float(r['BJD']) for r in good]);ys=np.array([float(r[column]) for r in good]);es=np.array([float(r[ecol]) for r in good]);nights=np.floor(tt+.5)
 t=[];y=[];e=[]
 for n in np.unique(nights):
  m=nights==n;w=1/es[m]**2;t.append(np.average(tt[m],weights=w));y.append(np.average(ys[m],weights=w));e.append(np.hypot(1/np.sqrt(w.sum()),2.))
 t,y,e=map(np.array,[t,y,e]);g=np.zeros(len(t),int);years=np.floor(Time(t,format='jd').decimalyear).astype(int)
 for year in np.unique(years):
  held=years==year;train=~held
  if held.sum()<20:continue
  full=refine(t[train],y[train],e[train],g[train],periods,fraction=.001)
  residual=(y[held]-predict(full,t[held],g[held]))/e[held]
  drops=[]
  for i,p in enumerate(periods):
   reduced=refine(t[train],y[train],e[train],g[train],periods[:i]+periods[i+1:],fraction=.001)
   resid=(y[held]-predict(reduced,t[held],g[held]))/e[held]
   drops.append(dict(omitted_period=p,held_delta_chi2=float(resid@resid-residual@residual)))
  row=dict(reduction=column,year=int(year),n_held=int(held.sum()),train_periods=full['periods'].tolist(),train_amplitudes=full['amplitudes'].tolist(),held_rms=float(np.sqrt(np.mean((y[held]-predict(full,t[held],g[held]))**2))),components=drops)
  results.append(row);print(column,year,[(r['omitted_period'],round(r['held_delta_chi2'],2)) for r in drops],flush=True)
 save_json(out/(column+'-nightly.json'),dict(time=t.tolist(),rv=y.tolist(),error=e.tolist(),years=years.tolist()))
save_json(out/'coherence.json',dict(created_utc=now(),input_sha256=sha(source),script_sha256=sha(Path(__file__)),module_sha256=sha(Path('src/exoplanet/rv_search.py')),results=results,limitations='Post-hoc leave-calendar-year-out checks of externally reported and already-opened modes; not blind discovery. Period neighborhoods seeded from full-data modes. Pre-upgrade only; >=20 nights per held year. Two reductions use the same spectra, not independent observations. Fixed2m/s jitter, circular orbits, no activity GP. Positive delta chi-square means omitted-year predictions improve when that component is included; it is not a false-alarm significance.'))
