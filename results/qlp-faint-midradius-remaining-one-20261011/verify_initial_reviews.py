from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());cp=out/'checkpoint-0297.json';c=read(cp);assert len(c['inventory'])==c['n_completed']==297
for item in c['inventory']:assert sha(Path(item['path']))==item['sha256']
paths=[Path('results/qlp-faint-midradius-one-pilot-coverage-followup-20261011/458778313-peak1')]+[Path(f'results/qlp-faint-midradius-remaining-one-coverage-followup-20261011/{name}') for name in ['320351354-peak2','1693886-peak0','1693886-peak1']];rows=[]
for path in paths:
 r=read(path/'review.json');f=read(path/'frozen.json');h=read(path/'heldout.json');assert r['discovery_sha256']==f['discovery_sha256']
 for name,digest in r['artifacts'].items():assert sha(path/name)==digest
 for evidence in f['training_data']+[d for x in h for d in x.get('data',[])]:
  raw=Path(f"data/qlp/{f['tic']}-s{evidence['sector']:04d}.fits");assert sha(raw)==evidence['source']['sha256']
 rows.append({'path':str(path),'review_sha256':sha(path/'review.json'),'source_checks_pending':r['source_checks_pending']})
save_json(out/'initial-reviews.json',{'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(cp),'reviews':rows,'status':'297-result snapshot and4 initial plot reviews verified; ongoing workers and pending source checks are not completion or planet validation.'})
print('Verified snapshot and four initial reviews.')
