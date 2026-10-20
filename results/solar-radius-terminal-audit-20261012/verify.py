from pathlib import Path
import json,collections
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;root=Path('results/solar-radius-remaining-resume4432-20261011');plan=json.loads((root/'plan.json').read_text());state=json.loads((root/'execution.json').read_text());assert state['status']=='complete' and state['active'] is None
assert state['plan_sha256']==sha(root/'plan.json');assert sha(Path(plan['source']))==plan['source_sha256'];eligible=json.loads(Path(plan['source']).read_text());rows=[];counts=collections.Counter();seen=set()
for batch in plan['batches']:
 p=Path(batch['output']);r=json.loads((p/'run.json').read_text());v=json.loads((p/'verification.json').read_text());sel=json.loads(Path(batch['selection']).read_text());assert sel==eligible[batch['start']:batch['end']];assert r['status']=='complete' and v['status']=='passed';assert r['selection_sha256']==sha(Path(batch['selection']));targets=[json.loads(f.read_text()) for f in (p/'targets').glob('*.json')];assert len(targets)==batch['n'];assert {x['tic'] for x in targets}=={x['tic'] for x in sel};assert not seen&{x['tic'] for x in targets};seen.update(x['tic'] for x in targets);c=collections.Counter(x.get('disposition',x['status']) for x in targets);assert dict(c)==v['counts'];counts.update(c);raw=0
 for x in targets:
  assert x['target']==next(s for s in sel if s['tic']==x['tic'])
  for d in x.get('data',[]):
   assert sha(Path(f"data/lightcurves/s{d['sector']:04d}-{x['tic']}.fits"))==d['source']['sha256'];raw+=1
 for name,h in r['source_sha256'].items():assert sha(p/'source'/name)==h
 assert raw==v['raw_products_checked']
 rows.append(dict(batch=str(p),counts=dict(c),raw_products_checked=raw,terminal_verification_sha256=sha(p/'verification.json'),terminal_verified_utc=v['verified_utc']))
assert len(seen)==7004-4432
save_json(out/'verification.json',dict(status='passed',verified_utc=now(),script_sha256=sha(Path(__file__)),queue_state_sha256=sha(root/'execution.json'),n_resumed_targets=len(seen),counts=dict(counts),batches=rows,limits='Independent terminal membership/count/source/raw audit of resumed4432:7004. Historical reserved-cache absence is retained from per-batch terminal verifications, not reasserted after follow-up. Scientific pass reviews remain separate.'))
print(len(seen),dict(counts))
