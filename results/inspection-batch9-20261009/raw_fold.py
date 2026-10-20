"""Inspect sector-normalized flux without running-median detrending."""
import json
from pathlib import Path
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now

out=Path('results/inspection-batch9-20261009')
frozen=Path('results/followup-399450592-expanded-20261009/frozen.json')
b=json.loads(frozen.read_text())['best'];rows=[]
fig,axes=plt.subplots(2,3,figsize=(14,7),constrained_layout=True)
for j,sector in enumerate([24,25,58]):
    path=Path(f'data/lightcurves/s{sector:04d}-399450592.fits')
    with fits.open(path) as h:
        d=h[1].data
        for i,column in enumerate(['SAP_FLUX','PDCSAP_FLUX']):
            t,f,e=[np.array(d[c],float) for c in ['TIME',column,column+'_ERR']]
            keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(f)&np.isfinite(e)&(f>0)&(e>0)
            t,f,e=t[keep],f[keep],e[keep];normal=np.median(f);y=f/normal;dy=e/normal
            phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
            bins=[]
            for left,right in zip(np.linspace(-b['period']/2,b['period']/2,81)[:-1],np.linspace(-b['period']/2,b['period']/2,81)[1:]):
                m=(phase>=left)&(phase<right)
                if not m.any():continue
                bins.append({'phase_days':float((left+right)/2),'flux':float(np.average(y[m],weights=1/dy[m]**2)),'n':int(m.sum())})
            rows.append({'sector':sector,'column':column,'source_sha256':sha(path),'normalization':float(normal),'bins':bins})
            ax=axes[i,j];ax.plot(phase*24,(y-1)*1e6,'.',ms=1,alpha=.15)
            ax.plot([z['phase_days']*24 for z in bins],[(z['flux']-1)*1e6 for z in bins],'o-',ms=2,color='black')
            ax.set(title=f'Sector {sector}: {column}',xlabel='Hours from frozen event',ylabel='Relative flux, ppm')
            ax.axvspan(-b['duration']*12,b['duration']*12,color='orange',alpha=.15)
fig.suptitle('TIC 399450592: median normalization only; no running detrend')
fig.savefig(out/'399450592-raw-fold.png',dpi=140);plt.close(fig)
save_json(out/'399450592-raw-fold.json',{'created_utc':now(),'frozen_sha256':sha(frozen),'script_sha256':sha(out/'raw_fold.py'),'note':'Diagnostic bins, not independent inference or calibrated statistics. All sectors already opened.','rows':rows})
