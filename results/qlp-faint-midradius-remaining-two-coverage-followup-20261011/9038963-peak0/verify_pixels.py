from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (23,24):
 p=Path(f'results/tesscut-9038963-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-9038963-20261011/neighbors.json')) and a['n_events']==2
 assert [e['inside_quality_zero'] for e in c['events']]==[9,9]
 assert [e['outside_quality_zero'] for e in c['events']]==([35,36] if s==23 else [36,35])
 req=read(p/'request.json')['params'];assert req['ra']==222.105939873631 and req['dec']==29.9979955655275 and req['sector']==s
 q=Path(f'results/spoc-pixels-9038963-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and 'Fewer than two image events' in (q/'stderr.txt').read_text()
 pc=read(q/'coverage.json');pp=Path(f'data/pixels/9038963-s{s:04d}.fits')
 assert pc['raw_sha256']==sha(pp) and pc['frozen_sha256']==sha(out/'frozen.json') and pc['script_sha256']==sha(q/'audit_coverage.py')
 assert [e['quality_counts'] for e in pc['events']]==([{'128':1,'4096':8},{'4096':9}] if s==23 else [{'0':9},{'32768':9}])
 assert [e['inside_quality_zero'] for e in pc['events']]==([0,0] if s==23 else [9,0]) and [e['outside_quality_zero'] for e in pc['events']]==([3,0] if s==23 else [36,35])
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_coverage_sha256':sha(q/'coverage.json'),'processed_file_sha256':sha(pp),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-9038963-s24-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacks and four individual images inspected. S23 event-1 negative field/event0 positive column structure; both S24 events negative field with column structure. No consistent isolated source.','limits':'Background/quality concerns, exact cause and host unresolved. Three processed windows fully flagged. No usable coverage is not nondetection. Initial incorrect-coordinate requests excluded and preserved; corrected request coordinates verified. No Gaia attribution; alternate fit pending.'})
print('Source provenance, coverage and failures verified.')
