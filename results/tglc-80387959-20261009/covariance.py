"""Check shared extraction structure without treating regression as deblending."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha
out=Path(__file__).parent;b=json.loads(Path('results/followup-80387959-qlp90-100-20261009/frozen.json').read_text())['best'];rows=[]
for sector in [10,36,37]:
 a=np.load(out/f'80387959-s{sector}-processed.npz');n=np.load(out/f'80387965-s{sector}-processed.npz');t=a['t'];index=np.searchsorted(n['t'],t);index=np.clip(index,0,len(n['t'])-1);prev=np.maximum(index-1,0);index=np.where(abs(n['t'][prev]-t)<abs(n['t'][index]-t),prev,index)
 matched=abs(n['t'][index]-t)<2e-5;phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;keep=matched&(abs(phase)>2*b['duration']);x=a['y'][keep]-1;y=n['y'][index[keep]]-1
 rows.append({'sector':sector,'n_common_outside':int(keep.sum()),'outside_pearson_correlation':float(np.corrcoef(x,y)[0,1]),'outside_least_squares_neighbor_relative_per_target_relative':float(np.polyfit(x,y,1)[0]),'input_sha256':{f'{tic}':sha(out/f'{tic}-s{sector}-processed.npz') for tic in [80387959,80387965]},'note':'Common-cadence diagnostic, no detrending by the other star, no source probability. Shared systematics/blend leakage can correlate both extractions.'})
save_json(out/'shared-structure.json',{'script_sha256':sha(Path(__file__)),'rows':rows});print(rows)
