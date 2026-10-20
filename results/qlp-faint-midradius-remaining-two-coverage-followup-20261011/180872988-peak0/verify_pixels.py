from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (2,3):
 p=Path(f'results/tesscut-180872988-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-180872988-20261011/neighbors.json')) and a['n_events']==2
 assert [e['inside_quality_zero'] for e in c['events']]==([5,7] if s==2 else [0,8,8])
 q=Path(f'results/spoc-pixels-180872988-s{s}-20261011');assert read(q/'status.json')['exit_code']==1
 if s==2:assert '404 Client Error' in (q/'stderr.txt').read_text()
 else:
  assert 'Fewer than two image events' in (q/'stderr.txt').read_text()
  pc=read(q/'coverage.json');assert pc['script_sha256']==sha(q/'audit_coverage.py') and pc['raw_sha256']==sha(Path('data/pixels/180872988-s0003.fits')) and pc['frozen_sha256']==sha(out/'frozen.json')
  assert [e['quality_counts'] for e in pc['events']]==[{'128':8},{'4096':8},{'0':8}]
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'coverage_sha256':sha(p/'coverage.json'),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-180872988-s3-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacks and all four individual maps inspected. S2 weak mixed residuals; S3 event3 positive field offset and event4 weak mixed, no consistent isolated source.','limits':'Background/source-systematics concern, exact cause and host unresolved. Passing raw flags not clean-background assurance. S2 processed exact-product404 and S3 flagged event windows are not nondetections. Same epochs as QLP; no Gaia attribution from unreliable moments.'})
print('Source provenance, coverage and failures verified.')
