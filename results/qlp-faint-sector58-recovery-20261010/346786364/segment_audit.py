from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.qlp_campaign import bin_curve
from exoplanet.pipeline import sha,save_json,now
out=Path('results/qlp-faint-sector58-recovery-20261010/346786364')
raw=Path('data/qlp/346786364-s0058.fits')
with fits.open(raw) as h:
 assert h[0].header['TICID']==346786364 and h[0].header['SECTOR']==58
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
 t,y,e=[np.array(d[c],float) for c in ['TIME',fc,ec]]
 good=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)&np.isfinite(e)&(e>0)
 t,y,e=t[good],y[good],e[good];ix=np.argsort(t);t,y,e=t[ix],y[ix],e[ix]
 native=len(t);t,y,e=bin_curve(t,y,e);pieces=np.split(np.arange(len(t)),np.where(np.diff(t)>.3)[0]+1);rows=[]
 for ix in pieces:
  tt=t[ix];cad=float(np.median(np.diff(tt))) if len(tt)>1 else None;w=max(3,int(1.5/cad)//2*2+1) if cad and cad>0 else None
  rows.append({'n':len(ix),'span_days':float(np.ptp(tt)),'cadence_days':cad,'window_bins':w,'eligible':len(ix)>=30 and w is not None and len(ix)>=w})
for r in rows:
 r['alternative_window_bins']=max(3,int(2.5/r['cadence_days'])//2*2+1)
 r['alternative_eligible']=r['n']>=30 and r['n']>=r['alternative_window_bins']
assert any(r['eligible'] for r in rows) and not any(r['alternative_eligible'] for r in rows)
original=json.loads(Path('results/qlp-faint-sector58-expanded-20261010/targets/346786364.json').read_text())
assert original.get('data') and original.get('best') and original['status']=='error'
assert 'No sufficiently long contiguous data segment' in original['error']
save_json(out/'segment-audit.json',{'utc':now(),'raw_sha256':sha(raw),'script_sha256':sha(Path(__file__)),'native_pairs':native,'n_binned':len(t),'segments':rows,'policy':'Reproduce original 10-minute binning and 1.5- and 2.5-day contiguous-segment eligibility without altering gates or opening reserved data.'})
print(native,len(t),rows)
