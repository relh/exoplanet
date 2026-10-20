from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
np=Path('results/neighbors-303599188-20261011/neighbors.json');rows=[]
for sector in [43,44]:
 rawdir=Path(f'results/tesscut-303599188-s{sector}-20261011');raw=read(rawdir/'analysis.json');assert sha(Path(raw['source']['path']))==raw['source']['sha256']
 assert raw['fit_sha256']==sha(out/'frozen.json') and raw['neighbor_sha256']==sha(np) and raw['script_sha256']==sha(rawdir/'analyze.py')
 procdir=Path(f'results/spoc-pixels-303599188-s{sector}-20261011');a=read(procdir/'analysis/localization.json');assert read(procdir/'status.json')['exit_code']==0
 assert sha(Path(f'data/pixels/303599188-s{sector:04d}.fits'))==a['source']['sha256']
 assert a['frozen_sha256']==sha(out/'frozen.json')
 assert a['neighbors_by_distance'][0]['tic']==({43:303599200,44:303599200}[sector])
 rows.append({'sector':sector,'raw_analysis_sha256':sha(rawdir/'analysis.json'),'raw_plot_sha256':sha(rawdir/'difference.png'),'processed_analysis_sha256':sha(procdir/'analysis/localization.json'),'processed_plot_sha256':sha(procdir/'analysis/difference.png'),'processed_target_offset_pixels':a['offset_from_header_target_pixels'],'nearest_neighbor':a['neighbors_by_distance'][0],'visual_review':'Raw and processed maps both show a compact off-target dip near TIC303599200/303599195 in both sectors.'})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'neighbors_sha256':sha(np),'rows':rows,'limits':'Four plots inspected. Processed source displacement favors contamination, not a uniquely identified host. Same photons across reductions; no PRF confidence or proper-motion correction. Different reductions share photons; moments do not resolve close companions. Gaia review pending.'})
print('Verified raw and processed source checks in both sectors')
