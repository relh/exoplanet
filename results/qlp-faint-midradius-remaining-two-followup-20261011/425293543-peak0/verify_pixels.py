from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s,n in ((80,12),(81,10)):
 p=Path(f'results/tesscut-425293543-s{s}-20261011');a=read(p/'analysis.json');c=read(p/'coverage.json')
 assert a['source']['sha256']==sha(Path(a['source']['path']))==c['raw_sha256']
 assert a['fit_sha256']==c['frozen_sha256']==sha(out/'frozen.json') and a['n_events']==n
 assert a['script_sha256']==sha(p/'analyze.py') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-425293543-20261011/neighbors.json'))
 i=read(p/'individual-events.json')
 for path,h in i['inputs'].items():assert sha(Path(path))==h
 assert i['plot_sha256']==sha(p/'individual-events.png') and i['script_sha256']==sha(p/'plot_events.py')
 q=Path(f'results/spoc-pixels-425293543-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'coverage_sha256':sha(p/'coverage.json'),'stack_plot_sha256':sha(p/'difference.png'),'individual_plot_sha256':sha(p/'individual-events.png'),'processed_error_sha256':sha(q/'stderr.txt')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'Both stacks and all22individual images inspected. Recurring compact target-region feature, offsets .194/.086pixels; several S80events have large positive or negative background offsets but relative target feature persists. Faint close blends unresolved.','limits':'Target-region eclipsing signal, not secure unique host or planet; deep rounded eclipses and failed reserved-sector validation retained. Same photons as discovery. No calibrated PRF confidence, Gaia nonmatches not exclusion. Held-sector raw images not yet checked.'})
print('Training image provenance and coverage verified.')
