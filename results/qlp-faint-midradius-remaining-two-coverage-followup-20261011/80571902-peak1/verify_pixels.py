from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=Path('results/tesscut-80571902-s72-coverage-20261011');a=read(p/'analysis.json');plan=read(p/'plan.json')
assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')==plan['script_sha256']
assert a['neighbor_sha256']==sha(Path('results/neighbors-80571902-20261011/neighbors.json'))
assert sha(Path(a['source']['path']))==a['source']['sha256']
assert sha(p/'files.json')==plan['original_files_sha256']
assert read(p/'status.json')['exit_code']==0 and a['event_numbers']==[1,2]
i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert sha(p/'plot_events.py')==i['script_sha256'] and sha(p/'individual-events.png')==i['plot_sha256']
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'analysis_sha256':sha(p/'analysis.json'),'individual_plot_sha256':sha(p/'individual-events.png'),'stacked_plot_sha256':sha(p/'difference.png'),'event_numbers':a['event_numbers'],'offset_pixels':a['offset_pixels'],'nearest_neighbors':a['neighbors'][:3],'visual_review':'Stacked plot and both individual event panels inspected. Both show compact displaced positive structure near80571910/715946563, similar to original-fit supported events. First event has additional field structure; no background correction or unique source attribution.','limits':'Likely neighboring-source contamination of both competing fits. Shared photons and one shared event; not independent planet evidence. Moment is not calibrated PRF confidence. True variable, physical cause, and true period unresolved.'})
print('Coverage source checks verified; nearest',a['neighbors'][0])
