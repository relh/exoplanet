from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;paths=[out.parent/f'303599188-peak{k}/frozen.json' for k in (0,2)];fitspec=[json.loads(p.read_text())['best'] for p in paths];rows=[]
for s in (43,44):
 f=json.loads(Path(f'results/tesscut-303599188-s{s}-20261011/files.json').read_text())[0];assert sha(Path(f['path']))==f['sha256']
 with fits.open(f['path']) as h:t=np.array(h[1].data['TIME']);q=np.array(h[1].data['QUALITY'])
 masks=[]
 for b in fitspec:
  phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
  masks.append(np.isfinite(t)&(q==0)&(abs(phase)<b['duration']/2))
 common=masks[0]&masks[1]
 rows.append({'sector':s,'input_sha256':f['sha256'],'quality_zero_inside_counts':[int(m.sum()) for m in masks],'common_inside_count':int(common.sum()),'common_time_range':None if not common.any() else [float(t[common].min()),float(t[common].max())]})
save_json(out/'window-overlap.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':[sha(p) for p in paths],'rows':rows,'limits':'Exposure overlap only, not equality of periods or full event baselines. Two fits use one star, not independent confirmations.'});print(rows)
