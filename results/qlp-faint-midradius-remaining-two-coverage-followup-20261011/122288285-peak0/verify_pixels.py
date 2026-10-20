from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
read=lambda p:json.loads(p.read_text());root=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011');rows=[]
for peak in (0,1):
 out=root/f'122288285-peak{peak}';fp=out/'frozen.json';items=[]
 for s in (102,103):
  p=Path(f"results/tesscut-122288285-s{s}{'-peak1' if peak else ''}-20261011");f=read(p/'files.json')[0];assert sha(Path(f['path']))==f['sha256']
  c=read(p/'coverage.json');assert c['raw_sha256']==f['sha256'] and c['frozen_sha256']==sha(fp) and c['script_sha256']==sha(p/'audit_coverage.py')
  if peak==0 and s==102:
   assert read(p/'status.json')['exit_code']==1 and len(c['events'])==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  else:
   a=read(p/'analysis.json');assert a['fit_sha256']==sha(fp) and a['script_sha256']==sha(p/'analyze.py') and a['n_events']==2
   assert a['neighbor_sha256']==sha(Path('results/neighbors-122288285-20261011/neighbors.json'))
  q=Path(f'results/spoc-pixels-122288285-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
  items.append({'sector':s,'directory':str(p),'coverage_sha256':sha(p/'coverage.json'),'status_sha256':sha(p/'status.json'),'processed_error_sha256':sha(q/'stderr.txt')})
 rows.append(items)
p=Path('results/tesscut-122288285-s103-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_all_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
f0=read(root/'122288285-peak0/frozen.json')['training_measurement']['events'];f1=read(root/'122288285-peak1/frozen.json')['training_measurement']['events'];delta=abs(f0[1]['center_btjd']-f1[1]['center_btjd'])*86400;assert delta<60
for peak in (0,1):
 out=root/f'122288285-peak{peak}'
 save_json(out/'source_review.json',{'verifier':str(Path(__file__)),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows[peak],'individual_plot_sha256':sha(p/'individual-events.png'),'shared_later_event_seconds':delta,'visual_review':'All three available stacked plots and six individual panels inspected. Peak0S103event0 fieldwide negative, event1 positive; peak1S102/S103 all fieldwide positive with other structure. No isolated repeatable stellar source.','limits':'Background/source-systematics concern, exact cause/host unresolved. Moments invalid for attribution; no Gaia inference. Two fits share later measured event. Processed exact-product404 not nondetection; peak0S102 onlyoneacceptedimageevent. No gates relaxed.'})
print('Both fits verified; shared later event offset seconds',delta)
