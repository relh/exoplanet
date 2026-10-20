from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (103,104):
 raw=Path(f'results/tesscut-74189224-s{s}-20261011');proc=Path(f'results/spoc-pixels-74189224-s{s}-20261011');f=read(raw/'files.json')[0];c=read(raw/'coverage.json')
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
 assert [e['inside_quality_zero'] for e in c['events']]==([32,0] if s==104 else [32,32])
 assert [e['outside_quality_zero'] for e in c['events']]==([126,0] if s==104 else [127,127])
 if s==104:
  assert [e['quality_counts'] for e in c['events']]==[{'0':32},{'2048':32}]
  assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
 else:
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==f['sha256']
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-74189224-20261011/neighbors.json'))
 assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
 rows.append({'sector':s,'file_sha256':f['sha256'],'coverage_sha256':sha(raw/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt')})
p=Path('results/pixel-events-74189224-20261011');plan=read(p/'plan.json');m=read(p/'manifest.json')
assert plan['script_sha256']==sha(p/'run.py') and plan['module_sha256']==sha(Path('src/exoplanet/pixel_vet.py')) and plan['fit_sha256']==sha(out/'frozen.json')
assert m['plan_sha256']==sha(p/'plan.json') and m['images_sha256']==sha(p/'images.npz') and m['plot_sha256']==sha(p/'individual-events.png')
for r in m['rows']:assert sha(Path(r['input']['path']))==r['input']['sha256'] and r['event_numbers']==([0,1] if r['sector']==103 else [2])
r=Path('results/tesscut-74189224-s103-20261011');n=read(p/'neighbor-projection.json');assert n['script_sha256']==sha(p/'project_neighbor.py') and n['neighbors_sha256']==sha(Path('results/neighbors-74189224-20261011/neighbors.json'))
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'individual_manifest_sha256':sha(p/'manifest.json'),'projection_sha256':sha(p/'neighbor-projection.json'),'s103_analysis_sha256':sha(r/'analysis.json'),'s103_plot_sha256':sha(r/'difference.png'),'visual_review':'S103 stack and all three usable raw event maps inspected. Positive field-wide background and changing off-target features. S103 relative feature near bright74181772; S104 strong feature elsewhere, no unique source attribution.','limits':'Background/contamination and coverage concerns; S104 event3 all32flag2048. Exact-product404 is not nondetection. Original S104 aggregate failure retained; separate individual-event view leaves original gates unchanged. No Gaia inference.'})
print('Source and coverage provenance verified.')
