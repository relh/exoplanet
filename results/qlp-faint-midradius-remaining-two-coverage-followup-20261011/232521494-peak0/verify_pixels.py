from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (74,75):
 p=Path(f'results/tesscut-232521494-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-232521494-20261011/neighbors.json')) and a['n_events']==2
 assert [e['inside_quality_zero'] for e in c['events']]==([63,62] if s==74 else [62,2])
 assert [e['outside_quality_zero'] for e in c['events']]==([248,249] if s==74 else [136,124])
 if s==75:assert c['events'][1]['quality_counts']=={'0':2,'2048':61}
 q=Path(f'results/spoc-pixels-232521494-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and 'Fewer than two image events' in (q/'stderr.txt').read_text()
 pc=read(q/'coverage.json');pp=Path(f'data/pixels/232521494-s{s:04d}.fits')
 assert pc['raw_sha256']==sha(pp) and pc['frozen_sha256']==sha(out/'frozen.json') and pc['script_sha256']==sha(q/'audit_coverage.py')
 assert [e['quality_counts'] for e in pc['events']]==([{'4096':63},{'4096':62}] if s==74 else [{'4096':62},{'4096':63}])
 assert all(e['inside_quality_zero']==e['outside_quality_zero']==0 for e in pc['events'])
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_coverage_sha256':sha(q/'coverage.json'),'processed_file_sha256':sha(pp),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-232521494-s75-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacks and all four individual images inspected. S74 event0 negative field, event1 positive gradient; both S75 events negative across field. No consistent isolated source.','limits':'Background/quality and sparse coverage concerns, exact cause and host unresolved. All 250 processed inside exposures carry flag4096; no usable coverage is not nondetection. Raw event3 has only two quality-zero inside exposures. Same photons as QLP, not independent validation; no Gaia attribution from unreliable moments.'})
print('Source provenance, coverage and failures verified.')
