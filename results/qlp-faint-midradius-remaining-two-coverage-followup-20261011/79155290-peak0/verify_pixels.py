from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (94,95):
 p=Path(f'results/tesscut-79155290-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-79155290-20261011/neighbors.json')) and a['n_events']==2
 assert all(e['inside']==e['inside_quality_zero'] for e in c['events'])
 q=Path(f'results/spoc-pixels-79155290-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-79155290-s95-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacked and four individual plots inspected. S94event-1largefieldwidenegative/event0positive with target-region positive/negative structure. S95event1fieldwidepositive; event2 weaker background with target-positive and adjacent negative feature. No consistently isolated stellar source; stacked edge moments invalid host locations.','limits':'Background/source-systematics concern; last-event target feature retained, not planet exclusion or exact physical-cause attribution. All raw in-event exposures quality zero, which does not ensure clean background. Processed exact-product404 not nondetection; same epochs as QLP. No Gaia inference from invalid moments.'})
print('Raw evidence, quality coverage and processed failures verified.')
