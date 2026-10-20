from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');m=read(out/'models.json');r=read(out/'fits.json');c=read(out/'controls.json');cp=read(out/'controls-plan.json')
assert p['script_sha256']==sha(out/'analyze.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py')) and m['script_sha256']==sha(out/'download_models.py')
for n,h in p['inputs'].items():assert sha(Path(n))==h
for s in m['sectors']:
 assert sha(Path(s['pixel_path']))==s['pixel_sha256']
 for f in s['models']:assert sha(Path(f['path']))==f['source']['sha256']
assert r['plot_sha256']==sha(out/'comparison.png') and r['images_sha256']==sha(out/'images.npz')
assert len(r['controls'])==6 and all(i['max_amplitude_error']<1e-6 for i in r['controls'])
assert cp['script_sha256']==sha(out/'controls.py') and cp['images_sha256']==sha(out/'images.npz') and cp['fits_sha256']==sha(out/'fits.json')
assert c['plan_sha256']==sha(out/'controls-plan.json') and len(c['rows'])==10 and sum(i['status']=='measured' for i in c['rows'])==4
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'fits_sha256':sha(out/'fits.json'),'controls_sha256':sha(out/'controls.json'),'status':'provenance and matched-model controls passed; physical source attribution incomplete'})
print('Verified mission grids, fits and controls.')
