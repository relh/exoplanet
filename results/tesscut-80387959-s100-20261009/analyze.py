import json
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json,now
from exoplanet.integrity import verify_hdus
from exoplanet.pixel_vet import difference_events,centroid
from exoplanet.pixel_injection import localization_controls
out=Path(__file__).parent;manifest=json.loads((out/'files.json').read_text());assert len(manifest)==1
p=Path(manifest[0]['path']);assert sha(p)==manifest[0]['sha256']
frozen=Path('results/followup-80387959-qlp90-100-20261009/frozen.json');best=json.loads(frozen.read_text())['best']
with fits.open(p) as h:
 integrity=verify_hdus(p,h);assert h[0].header['SECTOR']==100
 assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
 d=h[1].data;good=np.isfinite(d['TIME']);t=np.array(d['TIME'][good],float);f=np.array(d['FLUX'][good],float);e=np.array(d['FLUX_ERR'][good],float);q=d['QUALITY'][good];w=WCS(h[2].header)
 target=np.array(w.world_to_pixel_values(165.31041473672,-48.6136321332977))
 diff,err,events,numbers=difference_events(t,f,e,q,best);median=np.nanmedian(f[q==0],axis=0);center=centroid(diff,target)
 neighbors=json.loads(Path('results/neighbors-80387959-20261009/tic-neighbors.json').read_text());summaries={}
 for tic in [80387959,80387965,80387961]:
  star=next(s for s in neighbors if int(s['ID'])==tic);offset=np.array(w.world_to_pixel_values(star['ra'],star['dec']))-target
  result,maps=localization_controls(t,f,e,q,best,target,source_offset=offset)
  save_json(out/f'controls-{tic}.json',result);np.savez_compressed(out/f'controls-{tic}.npz',**maps)
  summaries[str(tic)]={k:result[k] for k in ['observed_offset_from_control_median_pixels','n_controls','n_controls_at_least_observed_offset','control_radius_quantiles_pixels']}
 np.savez_compressed(out/'images.npz',median=median,difference=diff,error=err,event_differences=events)
 save_json(out/'analysis.json',{'created_utc':now(),'source':manifest[0],'integrity':integrity,'frozen_sha256':sha(frozen),'script_sha256':sha(Path(__file__)),'n_events':len(numbers),'event_numbers':numbers,'target_xy':target.tolist(),'fixed_aperture_centroid':center.tolist(),'centroid_sky':list(map(float,w.pixel_to_world_values(*center))),'control_summary':summaries,'limitations':'TESScut FFI pixels, same photons as QLP. Local-baseline moments and empirical injection templates, not calibrated PRF confidence or independent photometry. Fixed catalog positions without proper-motion correction.'})
 fig,axes=plt.subplots(1,3,figsize=(14,4),constrained_layout=True)
 for ax,im,title in zip(axes,[np.log10(np.maximum(median,1)),diff,diff/err],['Median image','Out minus in','Difference / formal error']):
  a=ax.imshow(im,origin='lower');fig.colorbar(a,ax=ax,shrink=.7);ax.plot(*target,'rx');ax.plot(*center,'w+');ax.set_title(title)
  for tic in [80387965,80387961]:
   star=next(s for s in neighbors if int(s['ID'])==tic);xy=w.world_to_pixel_values(star['ra'],star['dec']);ax.plot(*xy,'o',mfc='none',mec='orange');ax.annotate(str(tic),xy,fontsize=7,color='orange')
 fig.suptitle('TIC 80387959, Sector 100: conditional source diagnostics');fig.savefig(out/'difference.png',dpi=140)
 print(summaries)
