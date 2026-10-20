"""Merge separately recorded recovery paths without double-counting targets."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
paths=[Path('results')/name for name in ['campaign-qlp-expanded-20261010','campaign-qlp-expanded-recovery-20261010','campaign-qlp-expanded-data-fallback-20261010']]
final={};runs=[]
for folder in paths:
 run=json.loads((folder/'run.json').read_text());assert run['status']=='complete'
 runs.append({'path':str(folder/'run.json'),'sha256':sha(folder/'run.json')})
 for p in (folder/'targets').glob('*.json'):
  d=json.loads(p.read_text());final[d['tic']]={'row':d,'path':str(p),'sha256':sha(p)}
selected=json.loads(Path('results/selection-qlp-only-20261010/selected.json').read_text())
assert set(final)=={t['tic'] for t in selected}
counts=Counter();routes=Counter();reviews=[];failures=[];records=[]
for tic,item in sorted(final.items()):
 d=item['row'];counts[d.get('disposition',d['status'])]+=1
 records.append({k:v for k,v in dict(tic=tic,**item).items() if k!='row'})
 if d['status']=='error':failures.append({'tic':tic,'error':d['error'],'path':item['path']});continue
 routes[Path(item['path']).parent.parent.name]+=1
 for i,p in enumerate(d.get('screened_peaks',[])):
  if set(p['flags'])<={'crowding_or_missing_crowding'}:reviews.append({'tic':tic,'peak_index':i,'best':p['best']})
save_json(out/'final-audit.json',{'utc':now(),'runs':runs,'n_selected':len(final),'n_usable':len(final)-len(failures),'dispositions':dict(counts),'usable_by_route':dict(routes),'remaining_failures':failures,'review_peaks':reviews,'final_records':records,'scope_note':'Fallbacks include two single-sector searches whose maximum period is baseline/2.5, less than20d. One target remains unusable; do not count it as searched. Original and recovery failures remain preserved.'})
print(len(final)-len(failures),dict(counts),dict(routes),failures,reviews)
