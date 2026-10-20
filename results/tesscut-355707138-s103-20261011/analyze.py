"""Per-event raw coverage and descriptive background maps; no host fit."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent
jobs=[{'status':'complete','tic':355707138,'sector':103,'ra':1.24493454078526,'dec':-60.835855926073,'files':json.loads((out/'files.json').read_text())}];rows=[]
for j in jobs:
 if j['status']!='complete':continue
 p=Path(j['files'][0]['path']);assert sha(p)==j['files'][0]['sha256']
 fp=Path(f"results/qlp-faint-midradius-remaining-three-followup-20261011/{j['tic']}-peak0/frozen.json")
 f=json.loads(fp.read_text());b=f['best']
 with fits.open(p) as h:
  integrity=verify_hdus(p,h);assert h[0].header['SECTOR']==j['sector']
  assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
  d=h[1].data;t=np.array(d['TIME']);q=np.array(d['QUALITY']);flux=np.array(d['FLUX'])
  xy=WCS(h[2].header).world_to_pixel_values(j['ra'],j['dec'])
  for ev in f['training_measurement']['events']:
   c=ev['center_btjd']
   if ev['snr']<3 or not np.nanmin(t)<=c<=np.nanmax(t):continue
   dt=t-c;inside=np.isfinite(t)&(q==0)&(abs(dt)<b['duration']/2)
   outside=np.isfinite(t)&(q==0)&(abs(dt)>b['duration'])&(abs(dt)<3*b['duration'])
   row={'tic':j['tic'],'sector':j['sector'],'event':ev['event'],'center':c,'n_inside':int(inside.sum()),'n_outside':int(outside.sum()),'pixel_sha256':sha(p),'frozen_sha256':sha(fp),'integrity':integrity,'target_xy':list(map(float,xy))}
   if inside.sum()<2 or outside.sum()<5:row['status']='insufficient_cadences';rows.append(row);continue
   inner=np.nanmean(flux[inside],axis=0);outer=np.nanmean(flux[outside],axis=0);diff=outer-inner
   valid=np.isfinite(diff)
   row.update(status='single_event_diagnostic_only',n_finite_pixels=int(valid.sum()),spatial_median_difference=float(np.nanmedian(diff)),positive_fraction=float(np.mean(diff[valid]>0)))
   name=f"{j['tic']}-s{j['sector']}-event{ev['event']}"
   np.savez_compressed(out/f'{name}.npz',inside=inner,outside=outer,difference=diff)
   fig,axes=plt.subplots(1,3,figsize=(12,4),constrained_layout=True)
   for ax,im,title in zip(axes,[outer,inner,diff],['Local baseline','Event','Baseline minus event']):
    z=ax.imshow(im,origin='lower');fig.colorbar(z,ax=ax,shrink=.7);ax.plot(*xy,'rx');ax.set_title(title)
   fig.suptitle(f"TIC{j['tic']} sector{j['sector']}: one-event descriptive map")
   fig.savefig(out/f'{name}.png',dpi=130);plt.close(fig)
   row['plot']=f'{name}.png';rows.append(row)
save_json(out/'analysis.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Individual event maps at frozen times, not two-event localization. No sector coaddition, PRF fitting, background subtraction, calibrated confidence or independent replication. Different quality masks across products; raw background changes may dominate.'})
print([{k:r[k] for k in ['tic','sector','n_inside','n_outside','status']} for r in rows])
