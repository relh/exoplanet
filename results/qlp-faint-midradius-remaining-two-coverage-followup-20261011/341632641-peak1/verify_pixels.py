from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (73,74):
 raw=Path(f'results/tesscut-341632641-s{s}-20261011');proc=Path(f'results/spoc-pixels-341632641-s{s}-20261011');f=read(raw/'files.json')[0];c=read(raw/'coverage.json')
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
 assert [e['inside_quality_zero'] for e in c['events']]==([58] if s==73 else [57,58])
 assert [e['outside_quality_zero'] for e in c['events']]==([229] if s==73 else [230,230])
 if s==73:assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
 else:
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==f['sha256']
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-341632641-20261011/neighbors.json'))
 assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
 rows.append({'sector':s,'file_sha256':f['sha256'],'coverage_sha256':sha(raw/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt')})
p=Path('results/pixel-events-341632641-20261011');plan=read(p/'plan.json');m=read(p/'manifest.json')
assert plan['script_sha256']==sha(p/'run.py') and plan['module_sha256']==sha(Path('src/exoplanet/pixel_vet.py')) and plan['fit_sha256']==sha(out/'frozen.json')
assert m['plan_sha256']==sha(p/'plan.json') and m['images_sha256']==sha(p/'images.npz') and m['plot_sha256']==sha(p/'individual-events.png')
for r in m['rows']:assert sha(Path(r['input']['path']))==r['input']['sha256'] and r['event_numbers']==([0] if r['sector']==73 else [1,2])
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'individual_manifest_sha256':sha(p/'manifest.json'),'visual_review':'S74 stack and all three usable individual raw maps inspected. S73 off-edge positive/negative structure; S74 event1 negative field/event2 positive field with gradients. No consistent isolated source.','limits':'Background/contamination and coverage concerns, exact cause unresolved. Exact-product404 and failed two-event aggregate are not nondetections. Original S73 aggregate failure retained; individual view leaves original gates unchanged. No Gaia source assignment.'})
print('Source and coverage provenance verified.')
