from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (85,86):
 p=Path(f'results/tesscut-317713012-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-317713012-20261011/neighbors.json')) and a['n_events']==(2 if s==85 else 3)
 assert all(e['inside']==e['inside_quality_zero'] for e in c['events'])
 assert [e['inside_quality_zero'] for e in c['events']]==([26,25] if s==85 else [26,26,26])
 assert [e['outside_quality_zero'] for e in c['events']]==([103,104] if s==85 else [102,57,103])
 q=Path(f'results/spoc-pixels-317713012-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-317713012-s86-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacks and all five individual maps inspected. S85 positive field-wide background with off-target feature; S86 event2 negative field, events3/4 mixed target-adjacent residuals. No consistent isolated source.','limits':'Background/source-systematics concern, exact cause and host unresolved. Passing raw flags not clean-background assurance. Processed exact-product404 not nondetection or proof all alternative products absent. Same epochs as QLP; no Gaia attribution from unreliable moments.'})
print('Source provenance, coverage and failures verified.')
