import json,shutil
from pathlib import Path
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
from exoplanet.qlp_campaign import empirical_errors
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;seed=Path('results/followup-80387959-qlp90-100-20261009/frozen.json');best=json.loads(seed.read_text())['best'];downloads=json.loads((out/'downloads.json').read_text());results=[]
fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
run={'created_utc':now(),'seed_sha256':sha(seed),'script_sha256':sha(Path(__file__)),'source_sha256':{p.name:sha(p) for p in (out/'source').iterdir()},'policy':'Already-opened sectors10/36/37 only; fixed ephemeris. Require TESS_flags=TGLC_flags=0, finite positive flux. No published error column: explicit adjacent-difference MAD uncertainty and existing flatten scatter floor. Compare raw/calibrated PSF/aperture and windows1.5/2.5d. Dependent extractions of same photons; PSF separation can leak signals. No source probability.'}
save_json(out/'analysis-run.json',run)
for item in downloads:
 if item['status']!='downloaded':continue
 path=Path(item['path']);assert sha(path)==item['source']['sha256']
 with fits.open(path) as h:
  integrity=verify_hdus(path,h);tic=int(h[0].header['TICID']);sector=h[0].header['SECTOR'];assert tic==item['tic'] and sector==item['sector'];assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
  d=h[1].data;assert int(h[0].header['GAIADR3'])=={80387959:5362389543781401216,80387965:5362389543781400192}[tic]
  for col in ['psf_flux','aperture_flux','cal_psf_flux','cal_aper_flux']:
   for window in [1.5,2.5]:
    row={'tic':tic,'sector':sector,'column':col,'window_days':window,'source':item['source'],'integrity':integrity,'status':'error'}
    try:
     t=np.array(d['time'],float);f=np.array(d[col],float);mask=(d['TESS_flags']==0)&(d['TGLC_flags']==0)&np.isfinite(t)&np.isfinite(f)&(f>0);t,f=t[mask],f[mask];order=np.argsort(t);t,f=t[order],f[order];assert np.all(np.diff(t)>0)
     sigma,errors=empirical_errors(t,f);t,y,dy=flatten(t,f,np.full(len(t),sigma),window=window)
     m=fixed_measure(t,y,dy,best['period'],best['transit_time'],best['duration']);row.update(status='measured',n_clean=len(t),error_model=errors,measurement=m)
     if col=='cal_psf_flux' and window==1.5:
      np.savez_compressed(out/f'{tic}-s{sector}-processed.npz',t=t,y=y,dy=dy)
      phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2;ax=axes[0 if tic==80387959 else 1,[10,36,37].index(sector)];ax.plot(phase*24,(y-1)*1e6,'.',ms=2,alpha=.4);ax.set(xlim=(-8,8),title=f'TIC {tic}, S{sector}',xlabel='Hours from frozen TESS epoch',ylabel='Relative PSF flux, ppm')
      edges=np.linspace(-.33,.33,27);centers=[];means=[]
      for l,r in zip(edges[:-1],edges[1:]):
       sel=(phase>=l)&(phase<r)
       if sel.any():centers.append((l+r)*12);means.append(np.average(y[sel]-1,weights=1/dy[sel]**2)*1e6)
      ax.plot(centers,means,'ko-',ms=3)
    except Exception as exc:row['error']=repr(exc)
    results.append(row);save_json(out/'measurements.json',results)
fig.suptitle('TGLC calibrated PSF, fixed ephemeris; empirical errors, same TESS observations');fig.savefig(out/'psf-folds.png',dpi=140)
for r in results:
 if r['window_days']==1.5:print(r['tic'],r['sector'],r['column'],r.get('measurement',{}).get('total',r.get('error')))
