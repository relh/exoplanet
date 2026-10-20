from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
helper=Path('results/tesscut-254039664-s67-20261010/background.py')
for sector in [71,72]:
 small=Path(f'results/tesscut-392005513-s{sector}-20261011');wide=Path(f'results/tesscut-392005513-s{sector}-wide-20261011')
 a=read(wide/'analysis.json');b=read(wide/'background.json');s=read(small/'background.json')
 assert all(r['status']=='insufficient_background_pixels' for r in s['results'])
 assert sha(wide/'background.py')==sha(helper)==b['script_sha256']
 assert b['analysis_sha256']==sha(wide/'analysis.json') and b['images_sha256']==sha(wide/'images.npz')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-392005513-wide-20261011/neighbors.json'))
 assert b['results'][0]['n_background_pixels']=={71:59,72:53}[sector]
 assert b['results'][1]['status']=='insufficient_background_pixels'
 with np.load(wide/'background-r2.npz') as z:
  x,y=np.rint(a['target_xy']).astype(int);value=float(z['residual'][y,x])
 assert (value<0 if sector==71 else value>0)
 rows.append({'sector':sector,'analysis_sha256':sha(wide/'analysis.json'),'background_sha256':sha(wide/'background.json'),'plot_sha256':sha(wide/'background.png'),'nearest_target_pixel_residual':value,'interpretation':'Negative target-area residual after spatial plane removal.' if sector==71 else 'Positive near-target residual persists; blend and systematic uncertainty remain.'})
save_json(out/'background_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Four wider difference/background plots inspected. Existing spatial-plane helper unchanged. Two-pixel source-exclusion fit possible; three-pixel fit fails for no remaining background pixels. No calibrated PRF fit, independent observation, or planet exclusion. Source-dependent systematics can survive a spatial plane.'})
print('Verified background sensitivity checks; cross-sector source disagreement remains')
