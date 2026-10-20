from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text())
parent=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/183257459-peak2/frozen.json')
f=read(parent);plan=read(out/'plan.json');assert plan['frozen_sha256']==sha(parent)
base=Path('results/tesscut-183257459-s88-20261011')
assert sha(base/'files.json')==plan['source_files_sha256']
rows=[]
for k in [1,2]:
 p=out/f'phase{k}';ff=read(p/'frozen-phase.json');a=read(p/'analysis.json')
 assert ff['parent_sha256']==sha(parent)
 expected=dict(f['best']);expected['transit_time']+=k*f['best']['period']/3
 assert ff['best']==expected and ff['phase_fraction']==k/3
 assert a['fit_sha256']==sha(p/'frozen-phase.json') and a['script_sha256']==sha(p/'analyze.py')
 assert sha(p/'files.json')==sha(base/'files.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['neighbor_sha256']==sha(Path('results/neighbors-183257459-20261011/neighbors.json'))
 assert read(p/'status.json')['exit_code']==0 and a['n_events']=={1:14,2:14}[k]
 rows.append({'phase_fraction':k/3,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'frozen_sha256':sha(p/'frozen-phase.json'),'target_offset_pixels':a['offset_pixels'],'nearest_sources':a['neighbors'][:3],'n_events':a['n_events']})
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'Both extra-phase plots inspected. Phase1/3 has a relative target-region enhancement on predominantly negative background, with formal maximum only1.85; phase2/3 has offset positive target-region feature and bright edge-neighbor structure. They do not securely localize both extra dips or establish a unique period/host. Same photons and post-selection diagnostics; no calibrated joint confidence.'})
print('Verified both fixed-third source diagnostics.')
