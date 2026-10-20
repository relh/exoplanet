from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
case=Path(__file__).parent;read=lambda p:json.loads(p.read_text());raw=Path('results/tesscut-268685988-s97-20261011');proc=Path('results/spoc-pixels-268685988-s97-20261011');nr=Path('results/neighbors-268685988-20261011');files=read(raw/'files.json');a=read(raw/'analysis.json');c=read(raw/'coverage.json');ip=read(raw/'individual-events.json')
assert len(files)==1 and sha(Path(files[0]['path']))==files[0]['sha256']
assert sha(Path('data/pixels/tesscut-268685988-s97.zip'))==read(raw/'source.json')['sha256']
assert read(raw/'status.json')['exit_code']==0
assert a['script_sha256']==sha(raw/'analyze.py') and a['fit_sha256']==sha(case/'frozen.json') and a['neighbor_sha256']==sha(nr/'neighbors.json')
assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(case/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
assert a['event_numbers']==[0,1,2] and a['n_events']==3
assert [(r['event'],r['inside_quality_zero'],r['outside_quality_zero']) for r in c['events']]==[(-1,0,187),(0,93,372),(1,93,373),(2,93,373)]
assert ip['script_sha256']==sha(raw/'plot_events.py') and ip['plot_sha256']==sha(raw/'individual-events.png')
for path,h in ip['inputs'].items():assert sha(Path(path))==h
assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
assert read(proc/'plan.json')['script_sha256']==sha(proc/'run.py')
assert sha(Path('data/catalogs/neighbors-268685988-20261011.json'))==read(nr/'source.json')['sha256']
assert len(read(nr/'neighbors.json'))==21
save_json(case/'source_review.json',{'script_sha256':sha(Path(__file__)),'raw_events':[0,1,2],'neighbor_rows':21,'processed_outcome':'Exact requested product HTTP404; not universal product absence or nondetection','artifacts':{str(p):sha(p) for folder in [raw,proc,nr] for p in sorted(folder.iterdir()) if p.is_file()},'plot_review':'Raw stack and all3 individual maps inspected: positive field-wide offsets/gradients, target-relative central deficit and changing surrounding structure. No consistently isolated dimming source. Formal pixel statistic and moment not host confidence.','limits':'Initial source diagnostic only. QLP/raw same photons, raw background not modeled. No unique host, Gaia assignment, independent confirmation or planet validation.'})
print('Verified raw source diagnostics, flags, neighbor query and retained processed404.')
