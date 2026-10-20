from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (93,94):
 p=Path(f'results/tesscut-324894265-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-324894265-20261011/neighbors.json')) and a['n_events']==(2 if s==93 else 3)
 assert [e['inside_quality_zero'] for e in c['events']]==([1,94,93] if s==93 else [93,93,37])
 q=Path(f'results/spoc-pixels-324894265-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-324894265-s94-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacked and five individual plots inspected. All dominated by strong positive/negative structure near bright324894237 atcutoutedge. No reliable target source attribution; targetfeatures not excluded by plots scaled to brightneighbor.','limits':'Background/source-systematics concern; not planet exclusion or exact physical-cause attribution. S93event0 onlyoneq0inside; S94event5 has56flag128 exposures; remaining in-event exposures quality zero do not ensure clean background. Processed exact-product404 not nondetection; same epochs as QLP. No Gaia inference from invalid moments.'})
print('Raw evidence, quality coverage and processed failures verified.')
