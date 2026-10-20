from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
np=Path('results/neighbors-80571902-20261011/neighbors.json')
for s in (71,72):
 p=Path(f'results/tesscut-80571902-s{s}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(np) and a['script_sha256']==sha(p/'analyze.py')
 q=Path(f'results/spoc-pixels-80571902-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt'),'events':a['event_numbers']})
p=Path('results/tesscut-80571902-s72-20261011');a=read(p/'individual-events.json')
for n,h in a['inputs'].items():assert sha(Path(n))==h
assert a['plot_sha256']==sha(p/'individual-events.png') and a['script_sha256']==sha(p/'plot_events.py')
other=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/80571902-peak1/frozen.json')
a=read(out/'frozen.json')['training_measurement']['events'];b=read(other)['training_measurement']['events'];overlap=[{'original_event':x['event'],'coverage_event':y['event'],'separation_seconds':abs(x['center_btjd']-y['center_btjd'])*86400} for x in a for y in b if abs(x['center_btjd']-y['center_btjd'])<.02]
assert len(overlap)==1 and overlap[0]['original_event']==4 and overlap[0]['coverage_event']==2
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'other_frozen_sha256':sha(other),'rows':rows,'shared_event':overlap,'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'Both stacked images and all four event panels inspected. S71event0 and S72events3/4 have compact displaced positive features near80571910/715946563. S71event1 is field-wide negative and invalidates the combined moment as host estimator. S72 nearest moment source80571910 at0.133px; target1.044px. Exact host unresolved.','limits':'Likely neighboring-source contamination, no unique attribution or calibrated PRF confidence; same photons. Processed exact-product404 is not nondetection or all-product absence. Competing period fits share one dip, not independent planet evidence.'})
print('Source provenance and shared event verified.')
