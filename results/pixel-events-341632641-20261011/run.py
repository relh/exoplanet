from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pixel_vet import individual_difference_events
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/341632641-peak1/frozen.json');b=json.loads(fp.read_text())['best']
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'fit_sha256':sha(fp),'module_sha256':sha(Path('src/exoplanet/pixel_vet.py')),'policy':'Unmodified individual raw event maps, no centroid estimation or background correction. Original two-event gate failure retained.'})
fig,axes=plt.subplots(2,2,figsize=(10,9),constrained_layout=True);rows=[];arrays={}
for row,s in enumerate((73,74)):
 p=Path(f'results/tesscut-341632641-s{s}-20261011');f=json.loads((p/'files.json').read_text())[0];path=Path(f['path']);assert sha(path)==f['sha256']
 with fits.open(path) as h:
  assert h[0].header['SECTOR']==s
  d=h[1].data;finite=np.isfinite(d['TIME']);t,flux,err=[np.array(d[k][finite],float) for k in ('TIME','FLUX','FLUX_ERR')]
  maps,variances,numbers=individual_difference_events(t,flux,err,d['QUALITY'][finite],b);assert len(numbers)==(1 if s==73 else 2)
  target=WCS(h[2].header).world_to_pixel_values(156.80329150311,81.2553773672729)
 for col,(n,im) in enumerate(zip(numbers,maps)):
  ax=axes[row,col];z=ax.imshow(im,origin='lower');fig.colorbar(z,ax=ax);ax.plot(*target,'rx');ax.set_title(f'Sector{s}, event{n}: out minus in')
 if len(numbers)==1:axes[row,1].set_visible(False)
 arrays[f's{s}_maps']=maps;arrays[f's{s}_variances']=variances
 rows.append({'sector':s,'input':f,'event_numbers':numbers,'target_xy':list(map(float,target))})
np.savez_compressed(out/'images.npz',**arrays);fig.savefig(out/'individual-events.png',dpi=140)
save_json(out/'manifest.json',{'plan_sha256':sha(out/'plan.json'),'rows':rows,'images_sha256':sha(out/'images.npz'),'plot_sha256':sha(out/'individual-events.png'),'limits':'Independent color scales. Formal variances ignore correlated/background error. No moments or host/source significance inferred.'})
