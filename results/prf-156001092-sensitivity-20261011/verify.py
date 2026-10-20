from pathlib import Path
import json,itertools,numpy as np
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json');s=read(out/'summary.json')
assert p['script_sha256']==sha(out/'run.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for n,h in p['inputs'].items():assert sha(Path(n))==h
assert len(r['rows'])==36
assert {(x['mapping'],x['dx'],x['dy'],x['width']) for x in r['rows']}==set(itertools.product(range(2),[-.1,0.,.1],[-.1,0.,.1],[0.,.4]))
assert s['results_sha256']==sha(out/'results.json') and s['script_sha256']==sha(out/'plot.py') and s['plot_sha256']==sha(out/'sensitivity.png')
for n in [2,3]:
 es=[e for row in r['rows'] for e in row['events'] if e['event']==n];assert len(es)==36 and all(np.isfinite(e['target_amplitude']) for e in es)
 report=next(x for x in s['rows'] if x['event']==n);assert report['target_range']==[min(e['target_amplitude'] for e in es),max(e['target_amplitude'] for e in es)]
 for e in es:assert {i['source'] for i in e['injections']}=={'156001092','156001090'}
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'summary_sha256':sha(out/'summary.json'),'status':'complete planned grid and provenance verified, not host probabilities'})
print('Verified all36 variants and144 injection fits.')
