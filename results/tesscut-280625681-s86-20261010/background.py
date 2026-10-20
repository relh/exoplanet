"""Post-selection spatial-background sensitivity check, not calibrated attribution."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;a=json.loads((out/'analysis.json').read_text());z=np.load(out/'images.npz');d=z['difference'];e=z['error'];yy,xx=np.indices(d.shape);target=np.array(a['target_xy']);rows=[]
fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
for ax,radius in zip(axes,[2.,3.]):
 mask=np.isfinite(d)&np.isfinite(e)&(e>0)
 for s in a['neighbors']:
  if s['Tmag'] is not None and s['Tmag']<17:mask&=(xx-s['x'])**2+(yy-s['y'])**2>radius**2
 mask&=(xx-target[0])**2+(yy-target[1])**2>radius**2
 design=np.stack([np.ones(d.shape),xx,yy],axis=-1);X=design[mask];w=1/e[mask]**2
 if mask.sum()<=10:
  rows.append({'mask_radius_pixels':radius,'n_background_pixels':int(mask.sum()),'status':'insufficient_background_pixels'});ax.set_title(f'No fit: {mask.sum()} background pixels');continue
 cov=np.linalg.inv(X.T@(w[:,None]*X));beta=cov@(X.T@(w*d[mask]));res=d-design@beta
 iy,ix=np.unravel_index(np.argmax(res),res.shape)
 rows.append({'mask_radius_pixels':radius,'n_background_pixels':int(mask.sum()),'plane_coefficients':beta.tolist(),'background_residual_rms':float(np.std(res[mask])),'maximum_residual_xy':[int(ix),int(iy)],'maximum_residual':float(res[iy,ix]),'maximum_offset_from_target':float(np.linalg.norm(np.array([ix,iy])-target))})
 im=ax.imshow(res,origin='lower');fig.colorbar(im,ax=ax);ax.plot(*target,'rx');ax.set_title(f'Plane removed; exclusion radius {radius:g}px')
 np.savez_compressed(out/f'background-r{radius:g}.npz',mask=mask,residual=res,plane=design@beta,covariance=cov)
save_json(out/'background.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'analysis_sha256':sha(out/'analysis.json'),'images_sha256':sha(out/'images.npz'),'results':rows,'limits':'Post-selection weighted spatial plane fit excluding catalog sources Tmag<17 and target at two radii. Not a PRF fit, independent data, calibrated significance, or proof of a transit. Unmodeled scattered light and source-dependent instrumental effects remain.'})
fig.savefig(out/'background.png',dpi=140);print(rows)
