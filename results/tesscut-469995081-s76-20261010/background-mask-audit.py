from pathlib import Path
import numpy as np,json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;a=json.loads((out/'analysis.json').read_text());z=np.load(out/'images.npz');d=z['difference'];e=z['error'];yy,xx=np.indices(d.shape);rows=[]
for radius in [2.,3.]:
 mask=np.isfinite(d)&np.isfinite(e)&(e>0)
 for s in a['neighbors']:
  if s['Tmag'] is not None and s['Tmag']<17:mask&=(xx-s['x'])**2+(yy-s['y'])**2>radius**2
 mask&=(xx-a['target_xy'][0])**2+(yy-a['target_xy'][1])**2>radius**2
 rows.append({'radius_pixels':radius,'n_background_pixels':int(mask.sum())})
save_json(out/'background-mask-audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'analysis_sha256':sha(out/'analysis.json'),'images_sha256':sha(out/'images.npz'),'rows':rows,'interpretation':'Existing catalog-exclusion plane method lacks background samples in this crowded cutout. No plane was fitted; no correction or host conclusion.'})
print(rows)
