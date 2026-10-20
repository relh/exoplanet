from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
np=Path('results/neighbors-142396584-20261011/neighbors.json');rows=[]
for sector in [75,76]:
 rawdir=Path(f'results/tesscut-142396584-s{sector}-20261011');raw=read(rawdir/'analysis.json');assert sha(Path(raw['source']['path']))==raw['source']['sha256']
 assert raw['fit_sha256']==sha(out/'frozen.json') and raw['neighbor_sha256']==sha(np) and raw['script_sha256']==sha(rawdir/'analyze.py')
 procdir=Path(f'results/spoc-pixels-142396584-s{sector}-20261011');a=read(procdir/'analysis/localization.json');assert read(procdir/'status.json')['exit_code']==0
 assert sha(Path(f'data/pixels/142396584-s{sector:04d}.fits'))==a['source']['sha256']
 assert a['frozen_sha256']==sha(out/'frozen.json')
 rows.append({'sector':sector,'raw_analysis_sha256':sha(rawdir/'analysis.json'),'raw_plot_sha256':sha(rawdir/'difference.png'),'processed_analysis_sha256':sha(procdir/'analysis/localization.json'),'processed_plot_sha256':sha(procdir/'analysis/difference.png'),'processed_target_offset_pixels':a['offset_from_header_target_pixels'],'nearest_neighbor':a['neighbors_by_distance'][0],'visual_review':'Both raw plots inspected: field-wide positive backgrounds. Both processed plots inspected: S75edge maximum and mixed target-region structure; S76weak mixed map. No reliable repeated-source localization.'})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'neighbors_sha256':sha(np),'rows':rows,'limits':'Four plots inspected. Raw background and processed edge/mixed maps raise artifact concerns; moment positions are not reliable host locations. Same photons across reductions; no PRF confidence or proper-motion correction. Different reductions share photons; moments do not resolve close companions. No Gaia source inference from invalid moments.'})
print('Verified raw and processed source checks in both sectors')
