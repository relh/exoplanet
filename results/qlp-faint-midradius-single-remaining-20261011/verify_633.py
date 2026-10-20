from pathlib import Path
import json
from collections import Counter
from astropy.io import fits
import numpy as np
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());c=read(out/'checkpoint-633.json');errors=read(out/'checkpoint-633-errors.json');plan=read(out/'plan.json');expected={t['tic']:t for t in plan['targets']};counts=Counter()
assert c['n_completed']==633 and c['plan_sha256']==sha(out/'plan.json')
for item in c['inventory']:
 p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p);assert r['target']==expected[r['tic']];counts[r.get('disposition') or r['status']]+=1
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
assert dict(counts)==c['counts'] and len({r['tic'] for r in c['inventory']})==633
assert {r['tic'] for r in errors['rows']}=={r['tic'] for r in c['inventory'] if r['status']=='error'}
for r in errors['rows']:
 p=Path(f"data/qlp/{r['tic']}-s{r['sector']:04d}.fits");assert sha(p)==r['raw_sha256'];assert sha(out/'targets'/f"{r['tic']}.json")==r['result_sha256']
 with fits.open(p) as h:
  assert h[0].header['TICID']==r['tic'] and h[0].header['SECTOR']==r['sector']
  assert np.isfinite(h[1].data[r['flux_column']]).sum()==r['finite_selected_flux']==0
  assert np.isfinite(h[1].data[r['error_column']]).sum()==r['finite_selected_errors']==0
assert c['eligible']==[]
save_json(out/'checkpoint-633-verification.json',{'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(out/'checkpoint-633.json'),'errors_sha256':sha(out/'checkpoint-633-errors.json'),'counts':dict(counts),'status':'633 target/result/raw identities verified; all eight failed inputs independently inspected with zero finite selected flux/errors. Search not terminal; no candidate or completeness claim.'})
print(dict(counts),'eight unusable inputs verified')
