from pathlib import Path
import json,collections
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());src=Path(run['selection_path']);selected=json.loads(src.read_text());assert sha(src)==run['selection_sha256'];rows=[json.loads(q.read_text()) for q in (p/'targets').glob('*.json')];assert run['status']=='complete' and len(rows)==512 and {r['tic'] for r in rows}=={r['tic'] for r in selected}
plan=json.loads(Path('results/solar-radius-ranks848-1360-selection-20261011/plan.json').read_text());assert sha(Path(plan['source']))==plan['source_sha256'];assert selected==json.loads(Path(plan['source']).read_text())[848:1360]
for name,digest in run['source_sha256'].items():assert sha(p/'source'/name)==digest
assert sha(src)==plan['selection_sha256']
assert run['n_selected']==512 and set(run['target_tics'])=={r['tic'] for r in rows}
raw=0;eligible=[]
for r in rows:
 assert r['target']==next(t for t in selected if t['tic']==r['tic'])
 for d in r.get('data',[]):
  f=Path(f"data/lightcurves/s{d['sector']:04d}-{r['tic']}.fits");assert sha(f)==d['source']['sha256'];assert int(d['star']['ticid'])==r['tic'] and int(d['star']['sector'])==d['sector'];raw+=1
 for s in r['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{r['tic']}.fits").exists()
 for i,peak in enumerate(r.get('screened_peaks',[])):
  if not peak['flags']:eligible.append(dict(tic=r['tic'],peak_index=i,best=peak['best']))
assert run['n_errors']==sum(r['status']=='error' for r in rows)
assert run['n_followup']==sum(r.get('disposition')=='followup_priority' for r in rows)
save_json(p/'verification.json',dict(status='passed',counts=dict(collections.Counter(r.get('disposition',r['status']) for r in rows)),raw_products_checked=raw,reserved_cache_absent=True,eligible_peaks=eligible));print((p/'verification.json').read_text())
