"""Exploratory TESScut difference image using an already-opened-epoch fit."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from exoplanet.pixel_vet import difference_events,centroid
from exoplanet.integrity import verify_hdus
from exoplanet.pipeline import save_json,sha,now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent;files=json.loads((out/'files.json').read_text());assert len(files)==1
p=Path(files[0]['path']);assert sha(p)==files[0]['sha256']
bp=Path('results/qlp-faint-sector72-recovery-20261010/26587095/targets/26587095.json');b=json.loads(bp.read_text())['screened_peaks'][0]['best'];npth=Path('results/neighbors-26587095-20261010/neighbors.json');neighbors=json.loads(npth.read_text())
with fits.open(p) as h:
 integrity=verify_hdus(p,h);assert h[0].header['SECTOR']==71
 assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
 d=h[1].data;good=np.isfinite(d['TIME']);t=np.array(d['TIME'][good],float);f=np.array(d['FLUX'][good],float);e=np.array(d['FLUX_ERR'][good],float);q=d['QUALITY'][good];w=WCS(h[2].header)
 target=np.array(w.world_to_pixel_values(107.954929021097,14.9319048300592))
 center_time=b['transit_time']+3*b['period']; delta=t-center_time
 inside=(q==0)&(abs(delta)<b['duration']/2); outside=(q==0)&(abs(delta)>b['duration'])&(abs(delta)<3*b['duration'])
 assert inside.sum()>=2 and outside.sum()>=5
 diff=np.nanmean(f[outside],axis=0)-np.nanmean(f[inside],axis=0)
 err=np.sqrt(np.nansum(e[outside]**2,axis=0)/outside.sum()**2+np.nansum(e[inside]**2,axis=0)/inside.sum()**2)
 events=np.array([diff]);numbers=[3];median=np.nanmedian(f[q==0],axis=0)
 py,px=np.unravel_index(np.nanargmax(diff/err),diff.shape);center=centroid(diff,(px,py));near=[]
 for s in neighbors:
  xy=np.array(w.world_to_pixel_values(s['ra'],s['dec']));near.append({'tic':int(s['ID']),'Tmag':s.get('Tmag'),'x':float(xy[0]),'y':float(xy[1]),'distance_from_moment_pixels':float(np.linalg.norm(xy-center))})
 near.sort(key=lambda x:x['distance_from_moment_pixels'])
 result={'utc':now(),'source':files[0],'integrity':integrity,'fit_sha256':sha(bp),'neighbor_sha256':sha(npth),'script_sha256':sha(Path(__file__)),'n_events':len(numbers),'event_numbers':numbers,'target_xy':target.tolist(),'peak_xy':[int(px),int(py)],'difference_moment_xy':center.tolist(),'peak_snr':float(np.nanmax(diff/err)),'offset_pixels':float(np.linalg.norm(center-target)),'difference_sky':list(map(float,w.pixel_to_world_values(*center))),'neighbors':near,'single_event_time_btjd':float(center_time),'n_inside':int(inside.sum()),'n_outside':int(outside.sum()),'limits':'Single-event post-selection difference; no repeatability or established period. Post-hoc ephemeris, same photons as QLP. Raw FFI background not modeled beyond local temporal subtraction. Moments and formal pixel errors are not calibrated PRF confidence. Catalog positions not proper-motion propagated.'}
 save_json(out/'analysis.json',result);np.savez_compressed(out/'images.npz',median=median,difference=diff,error=err,event_differences=events)
 fig,axes=plt.subplots(1,3,figsize=(14,4),constrained_layout=True)
 for ax,im,title in zip(axes,[np.log10(np.maximum(median,1)),diff,diff/err],['Median image','Out minus in','Difference / formal error']):
  a=ax.imshow(im,origin='lower');fig.colorbar(a,ax=ax,shrink=.7);ax.plot(*target,'rx');ax.plot(*center,'w+');ax.set_title(title)
  for s in near:
   if s['Tmag'] is not None and s['Tmag']<15 and 0<=s['x']<diff.shape[1] and 0<=s['y']<diff.shape[0]:ax.plot(s['x'],s['y'],'o',mfc='none',mec='orange');ax.annotate(str(s['tic']),(s['x'],s['y']),fontsize=6,color='orange')
 fig.suptitle('TIC26587095 sector71: single-event source diagnostic');fig.savefig(out/'difference.png',dpi=140)
 print({k:result[k] for k in ['n_events','peak_snr','offset_pixels','difference_sky']})
