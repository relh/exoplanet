from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
original=read(out/'frozen.json');shifted=read(out/'shifted-diagnostic.json')
assert shifted['exploratory_shift']['original_sha256']==sha(out/'frozen.json')
assert abs(shifted['best']['transit_time']-original['best']['transit_time']-.1*original['best']['period'])<1e-10
for s,n in ((53,7),(54,11)):
 for mode in ('frozen','shift'):
  p=Path(f'results/tesscut-425293543-'+('shift-' if mode=='shift' else '')+f's{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json');fp=out/('frozen.json' if mode=='frozen' else 'shifted-diagnostic.json')
  assert a['source']['sha256']==sha(Path(a['source']['path']))==c['raw_sha256']
  assert a['fit_sha256']==c['frozen_sha256']==sha(fp) and a['n_events']==n
  assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
  assert a['neighbor_sha256']==sha(Path('results/neighbors-425293543-20261011/neighbors.json'))
  rows.append({'sector':s,'mode':mode,'analysis_sha256':sha(p/'analysis.json'),'coverage_sha256':sha(p/'coverage.json'),'plot_sha256':sha(p/'difference.png')})
m=read(out/'shift-measurement.json');assert m['script_sha256']==sha(out/'measure_shift.py') and m['frozen_sha256']==sha(out/'frozen.json') and m['heldout_sha256']==sha(out/'heldout.json')
for row in m['rows']:
 for d in row['data']:assert d['source']['sha256']==sha(Path(f"data/qlp/425293543-s{row['sector']:04d}.fits"))
save_json(out/'held-source-review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'shift_measurement_sha256':sha(out/'shift-measurement.json'),'visual_review':'All four held-sector stacks inspected. Frozen phases show field background/neighbor structure, no compact target feature comparable to training. Posthoc+.1phase images show compact target-region features in both sectors, S53additionalnegative neighboring residuals.','limits':'Exploratory selected phase offset, not independent validation. Deep eclipsing signal present in earlier epochs away from frozen phase; true timing model/unique host/physical class unresolved. Original failed heldout validation unchanged. Individual held-event images not reviewed here.'})
print('Held-sector frozen and exploratory-shift evidence verified.')
