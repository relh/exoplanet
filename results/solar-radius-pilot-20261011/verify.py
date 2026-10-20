from pathlib import Path
import json,collections
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());selected=json.loads(Path(run['selection_path']).read_text());assert sha(Path(run['selection_path']))==run['selection_sha256'];rows=[json.loads(q.read_text()) for q in (p/'targets').glob('*.json')];assert run['status']=='complete' and len(rows)==16 and {r['tic'] for r in rows}=={r['tic'] for r in selected}
raw=0
for r in rows:
 assert r['status']=='screened';assert r['target']==next(t for t in selected if t['tic']==r['tic'])
 for d in r['data']:
  path=Path(f"data/lightcurves/s{d['sector']:04d}-{r['tic']}.fits");assert sha(path)==d['source']['sha256'];assert int(d['star']['ticid'])==r['tic'];assert int(d['star']['sector'])==d['sector'];raw+=1
 for s in r['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{r['tic']}.fits").exists()
 for peak in r['screened_peaks']:assert peak['flags']
counts=dict(collections.Counter(r['disposition'] for r in rows));save_json(p/'verification.json',dict(status='passed',counts=counts,raw_products_checked=raw,reserved_cache_absent=True,n_errors=0,n_eligible=0));print(counts,raw)
