from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json')
assert p['script_sha256']==sha(out/'run.py')
for name,h in p['inputs'].items():assert sha(Path(name))==h
assert r['plot_sha256']==sha(out/'folds.png')
for row in r['rows']:
 for data in row['data']:assert data['source']['sha256']==sha(Path(f"data/qlp/169785835-s{data['sector']:04d}.fits"))
assert [r['sector'] for r in r['rows']]==[11,37,99,100]
assert [r['fits']['Half Gaia period']['supported_events'] for r in r['rows']]==[0,1,0,2]
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'results_sha256':sha(out/'results.json'),'status':'passed provenance and recorded event counts; not astrophysical validation'})
print('Verified fixed-period comparison provenance.')
