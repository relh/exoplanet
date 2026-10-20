from pathlib import Path
import json,collections
from exoplanet.pipeline import sha,save_json,now
p=Path('results/solar-radius-remaining-queue-20261011');plan=json.loads((p/'plan.json').read_text());batch=next(b for b in plan['batches'] if b['start']==3920);out=Path(batch['output']);src=Path(batch['selection']);selected=json.loads(src.read_text())
run=json.loads((out/'run.json').read_text());rows=[json.loads(f.read_text()) for f in (out/'targets').glob('*.json')];assert run['status']=='complete' and len(rows)==batch['n'];assert {r['tic'] for r in rows}=={r['tic'] for r in selected};assert run['selection_sha256']==sha(src)
for name,digest in run['source_sha256'].items():assert sha(out/'source'/name)==digest
raw=0;lookup={r['tic']:r for r in selected};leads=[]
for r in rows:
 assert r['target']==lookup[r['tic']]
 for d in r.get('data',[]):
  assert sha(Path(f"data/lightcurves/s{d['sector']:04d}-{r['tic']}.fits"))==d['source']['sha256'];assert d['star']['ticid']==r['tic'] and d['star']['sector']==d['sector'];raw+=1
 for sector in r['target']['heldout_sectors']:
  path=Path(f"data/lightcurves/s{sector:04d}-{r['tic']}.fits")
  if path.exists():
   assert (r['tic'],sector)==(5546257,62)
   f=Path('results/followup-5546257-20261011');held=json.loads((f/'heldout.json').read_text())[0];frozen=json.loads((f/'frozen.json').read_text());assert json.loads((f/'verification.json').read_text())['status']=='passed';assert sha(path)==held['source']['sha256'] and frozen['frozen_utc']<held['source']['retrieved_utc']
 for i,peak in enumerate(r.get('screened_peaks',[])):
  if not peak['flags']:leads.append(dict(tic=r['tic'],peak_index=i,best=peak['best']))
assert run['n_errors']==sum(r['status']=='error' for r in rows);assert run['n_followup']==sum(r.get('disposition')=='followup_priority' for r in rows)
audit=dict(status='passed',verified_utc=now(),counts=dict(collections.Counter(r.get('disposition',r['status']) for r in rows)),raw_products_checked=raw,reserved_cache_absent=False,verified_followup_exception=dict(tic=5546257,sector=62),eligible_peaks=leads,queue_plan_sha256=sha(p/'plan.json'),verifier_sha256=sha(Path(__file__)));save_json(out/'verification.json',audit)
