"""Reuse existing moment helper on both background masks at raw-map peak locations."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pixel_vet import centroid
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;rows=[]
fig,axes=plt.subplots(2,2,figsize=(10,9),constrained_layout=True)
for iy,s in enumerate([87,88]):
 p=Path(f'results/tesscut-148001520-s{s}-wide-20261011');a=json.loads((p/'analysis.json').read_text());target=np.array(a['target_xy']);peak=a['peak_xy']
 for ix,r in enumerate([2,3]):
  source=p/f'background-r{r}.npz'
  with np.load(source) as z:res=z['residual']
  center=centroid(res,peak);neighbors=sorted([dict(n,corrected_distance_pixels=float(np.linalg.norm(center-[n['x'],n['y']]))) for n in a['neighbors']],key=lambda n:n['corrected_distance_pixels'])
  rows.append({'sector':s,'radius_pixels':r,'raw_peak_anchor':peak,'source_sha256':sha(source),'analysis_sha256':sha(p/'analysis.json'),'moment_xy':center.tolist(),'offset_from_target_pixels':float(np.linalg.norm(center-target)),'nearest':neighbors[:8]})
  ax=axes[iy,ix];im=ax.imshow(res,origin='lower');fig.colorbar(im,ax=ax,shrink=.65);ax.plot(*target,'rx',label='Target');ax.plot(*center,'w+',label='Moment')
  for n in neighbors[:8]:
   if np.linalg.norm(np.array([n['x'],n['y']])-target)<5:
    ax.plot(n['x'],n['y'],'o',mfc='none',mec='orange');ax.annotate(str(n['tic']),(n['x'],n['y']),fontsize=7,color='orange')
  ax.set_xlim(target[0]-4,target[0]+4);ax.set_ylim(target[1]-4,target[1]+4);ax.set_title(f'S{s}, source exclusion {r}px');ax.legend(fontsize=7)
save_json(out/'corrected-moments.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'helper_sha256':sha(Path('src/exoplanet/pixel_vet.py')),'rows':rows,'limits':'Post-selection diagnostic at original raw-map peak anchors; same images and ephemeris. Both background masks reported. Existing moment helper is not calibrated PRF astrometry. Does not assign a unique host or establish planetary origin. Sector87 has a stronger unrelated/unknown edge residual in the full field.'})
fig.savefig(out/'corrected-moments.png',dpi=140)
for r in rows:print(r['sector'],r['radius_pixels'],r['offset_from_target_pixels'],[(n['tic'],n['corrected_distance_pixels']) for n in r['nearest'][:3]])
