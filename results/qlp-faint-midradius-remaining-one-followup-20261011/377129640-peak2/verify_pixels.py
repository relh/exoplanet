from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());raw=Path('results/tesscut-377129640-s72-20261011');proc=Path('results/spoc-pixels-377129640-s72-20261011');nr=Path('results/neighbors-377129640-20261011');gaia=Path('results/gaia-377129640-scene-20261011')
f=read(raw/'files.json')[0];assert sha(Path(f['path']))==f['sha256'];assert sha(Path('data/pixels/tesscut-377129640-s72.zip'))==read(raw/'source.json')['sha256'];assert read(raw/'status.json')['exit_code']==read(proc/'status.json')['exit_code']==0
ra=read(raw/'analysis.json');pa=read(proc/'analysis/localization.json');assert ra['event_numbers']==list(range(9)) and pa['event_numbers']==[0,1,2,3,5,6,7,8]
assert ra['fit_sha256']==pa['frozen_sha256']==sha(out/'frozen.json');assert ra['neighbor_sha256']==sha(nr/'neighbors.json');assert sha(Path('data/pixels/377129640-s0072.fits'))==pa['source']['sha256']
for folder in [raw,proc]:
 c=read(folder/'coverage.json');assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(folder/'audit_coverage.py')
ip=read(raw/'event-plots.json');assert ip['script_sha256']==sha(raw/'plot_events.py')
for path,h in ip['inputs'].items():assert sha(Path(path))==h
for name,h in ip['plots'].items():assert sha(raw/name)==h
assert len(read(nr/'neighbors.json'))==22
assert sha(Path('data/catalogs/neighbors-377129640-20261011.json'))==read(nr/'source.json')['sha256']
gp=read(gaia/'plan.json');assert gp['script_sha256']==sha(gaia/'query.py') and gp['neighbors_sha256']==sha(nr/'neighbors.json')
for path,h in gp['image_analysis_hashes'].items():assert sha(Path(path))==h
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
 assert sha(Path(f'data/catalogs/gaia-377129640-scene-{table}-20261011.csv'))==read(gaia/f'{table}-source.json')['sha256']
assert read(gaia/'results.json')['status']=='complete' and len(read(gaia/'gaia_source.json'))==4 and len(read(gaia/'vari_eclipsing_binary.json'))==0
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for folder in [raw,proc,nr,gaia] for p in sorted(folder.rglob('*')) if p.is_file()},'status':'Raw9 and processed8 event diagnostics, input hashes,22 neighbors and4 Gaia sources verified. Catalog nonmatches not exclusions. No source probability or planet validation.'})
print('Verified image and catalog diagnostics.')
