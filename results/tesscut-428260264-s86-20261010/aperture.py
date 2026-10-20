"""Post-selection raw-pixel aperture/background diagnostic at frozen timing."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;ap=out/'analysis.json';a=json.loads(ap.read_text());fp=Path('results/qlp-faint-sector86-followup-20261010/428260264-peak0/frozen.json');b=json.loads(fp.read_text())['best'];raw=Path(a['source']['path']);assert sha(raw)==a['source']['sha256']
with fits.open(raw) as h:
 d=h[1].data;good=(d['QUALITY']==0)&np.isfinite(d['TIME']);t=np.array(d['TIME'][good],float);flux=np.array(d['FLUX'][good],float);err=np.array(d['FLUX_ERR'][good],float)
yy,xx=np.indices(flux.shape[1:]);x0,y0=a['target_xy'];mask=np.ones(xx.shape,bool)
for s in a['neighbors']:
 if s['Tmag'] is not None and s['Tmag']<17:mask&=(xx-s['x'])**2+(yy-s['y'])**2>4
mask&=(xx-x0)**2+(yy-y0)**2>4
assert mask.sum()>10, 'Insufficient background pixels'
X=np.stack([np.ones(xx.shape),xx,yy],axis=-1);pinv=np.linalg.pinv(X[mask]);beta=flux[:,mask]@pinv.T;plane=np.einsum('tc,ijc->tij',beta,X)
rows=[];fig,axes=plt.subplots(4,1,figsize=(10,9),constrained_layout=True)
for radius in [1.5,2.0]:
 aperture=(xx-x0)**2+(yy-y0)**2<radius**2
 # Exact linear propagation of published errors through spatial plane subtraction.
 coeff=aperture.astype(float);coeff[mask]-=X[aperture].sum(axis=0)@pinv
 star=np.einsum('tij,ij->t',flux,coeff);error=np.sqrt(np.einsum('tij,ij->t',err**2,coeff**2));sky=plane[:,aperture].sum(axis=1);norm=np.nanmedian(star);assert norm>0
 keep=np.isfinite(star)&np.isfinite(error)&(error>0)
 m=fixed_measure(t[keep],star[keep]/norm,error[keep]/norm,b['period'],b['transit_time'],b['duration']);rows.append({'radius_pixels':radius,'aperture_pixels':int(aperture.sum()),'median_source_flux':float(norm),'measurement':m,'sky_measurement_in_source_units':fixed_measure(t[keep],sky[keep]/norm,error[keep]/norm,b['period'],b['transit_time'],b['duration'])})
 for ax,n in zip(axes,a['event_numbers']):
  center=b['transit_time']+n*b['period'];local=keep&(abs(t-center)<.8)
  ax.plot((t[local]-center)*24,star[local]/norm,'.',ms=2,alpha=.5,label=f'{radius:g}px source')
  ax.axvspan(-12*b['duration'],12*b['duration'],alpha=.08,color='red');ax.set_title(f'Event {n}; BTJD {center:.5f}');ax.set_ylim(.95,1.05)
 np.savez_compressed(out/f'aperture-r{radius:g}.npz',time=t,source_flux=star,error=error,sky_flux=sky,coefficients=coeff)
axes[0].legend();axes[-1].set_xlabel('Hours from frozen event');fig.savefig(out/'aperture.png',dpi=130)
save_json(out/'aperture.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'analysis_sha256':sha(ap),'frozen_sha256':sha(fp),'raw_sha256':sha(raw),'background_pixels':int(mask.sum()),'results':rows,'limits':'Exploratory same-photon aperture extraction, no retuning/flattening. Spatial plane chosen post-selection with 2-pixel exclusions; 3-pixel mask has no background pixels. Plot shows only the first four generic pixel windows; measurements use all qualifying windows. Published independent pixel errors omit correlated noise and plane-model systematics; sky SNR uses source error only as a diagnostic scaling, not significance. Not independent validation or source proof.'});print([(r['radius_pixels'],r['measurement']['total'],r['measurement']['supported_events']) for r in rows])
