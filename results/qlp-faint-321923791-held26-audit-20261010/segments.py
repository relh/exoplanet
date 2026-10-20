from pathlib import Path
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.qlp_campaign import bin_curve
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;raw=Path('data/qlp/321923791-s0026.fits')
with fits.open(raw) as h:
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
 t,y,e=[np.array(d[c],float) for c in ['TIME',fc,ec]]
 good=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)&np.isfinite(e)&(e>0)
 t,y,e=t[good],y[good],e[good];ix=np.argsort(t);t,y,e=t[ix],y[ix],e[ix]
 native=len(t);t,y,e=bin_curve(t,y,e);rows=[]
 for ix in np.split(np.arange(len(t)),np.where(np.diff(t)>.3)[0]+1):
  tt=t[ix];cad=float(np.median(np.diff(tt))) if len(tt)>1 else None;w=max(3,int(1.5/cad)//2*2+1) if cad and cad>0 else None
  eligible=len(ix)>=30 and w is not None and len(ix)>=w
  n=int(((tt>tt[0]+.75)&(tt<tt[-1]-.75)).sum()) if eligible else 0
  rows.append({'n':len(ix),'span_days':float(np.ptp(tt)),'window_bins':w,'eligible':eligible,'max_after_edge_trim':n})
assert sum(r['max_after_edge_trim'] for r in rows)<200
save_json(out/'segments.json',{'utc':now(),'raw_sha256':sha(raw),'script_sha256':sha(Path(__file__)),'native_pairs':native,'binned_pairs':len(t),'segments':rows,'max_after_edge_trim':sum(r['max_after_edge_trim'] for r in rows),'limits':'Upper bound before positive-excursion removal; demonstrates why published positive-flux samples can fail the 200-clean-cadence requirement. Does not loosen gates or imply a transit nondetection.'});print(rows)
