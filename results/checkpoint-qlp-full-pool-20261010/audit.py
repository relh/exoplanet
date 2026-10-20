"""Point-in-time inventory; live discovery run is not a completed survey."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;root=Path('results/campaign-qlp-full-pool-20261010')
records=[];review=[];counts=Counter()
for p in sorted((root/'targets').glob('*.json')):
 d=json.loads(p.read_text());counts[d['status']]+=1
 records.append({'tic':d['tic'],'path':str(p),'sha256':sha(p),'status':d['status']})
 for i,k in enumerate(d.get('screened_peaks',[])):
  if set(k['flags'])<={'crowding_or_missing_crowding'}:
   dest=Path(f'results/qlp-full-pool-followup-20261010/{d["tic"]}-peak{i}')
   review.append({'tic':d['tic'],'peak_index':i,'followup_written':(dest/'heldout.json').exists(),'assessment_written':(dest/'ASSESSMENT.md').exists()})
run=json.loads((root/'run.json').read_text())
save_json(out/'audit.json',{'utc':now(),'run_status':run['status'],'run_sha256_at_snapshot':sha(root/'run.json'),'selection_sha256':sha(Path('results/qlp-full-pool-coverage-20261010/selected.json')),'n_target_records':len(records),'status_counts':dict(counts),'review_peaks':review,'records':records,'limits':'Point-in-time snapshot while workers continue. Errors are not nondetections. Review passes are not planets. Later files and mutable progress may exceed this inventory.'})
print(len(records),dict(counts),'review',len(review),'pending assessments',[x['tic'] for x in review if not x['assessment_written']])
