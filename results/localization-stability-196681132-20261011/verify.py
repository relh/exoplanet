from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.pixel_vet import centroid
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json');assert sha(out/'run.py')==p['script_sha256']
for f,h in p['inputs'].items():assert sha(Path(f))==h
root=Path('results/tesscut-196681132-s91-20261011');a=read(root/'analysis.json');images=np.load(root/'images.npz')['event_differences'];target=np.array(p['target_xy']);neighbor=np.array(p['neighbor_xy']);assert len(r['rows'])==88
for row in r['rows']:
 im=images[a['event_numbers'].index(row['event'])];center=target if row['aperture_center']=='target' else neighbor;c=centroid(im,center,halfwidth=row['halfwidth']);np.testing.assert_array_equal(c,row['xy']);assert row['closer_to_target']==(np.linalg.norm(c-target)<np.linalg.norm(c-neighbor))
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'comparison.png'),'status':'88 moment calculations and input hashes reconstructed. Window-dependent estimates are not source probabilities.'});print('88 reconstructed')
