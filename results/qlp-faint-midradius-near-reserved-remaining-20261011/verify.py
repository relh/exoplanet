from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');sel=read(out/'selection.json')
assert sha(Path(sel['parent']))==sel['parent_sha256']
assert read(Path(sel['parent']))[16:139]==plan['targets']==read(out/'selected.json')
assert sha(out/'selected.json')==sel['selected_sha256']==plan['source_sha256']
assert sha(out/'run.py')==plan['script_sha256']
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
expected={t['tic']:t for t in plan['targets']};counts=Counter();inventory=[];eligible={'followup':set(),'coverage-followup':set()}
for p in sorted((out/'targets').glob('*.json')):
 r=read(p);assert r['target']==expected[r['tic']];counts[r.get('disposition') or r['status']]+=1
 inventory.append({'tic':r['tic'],'path':str(p),'sha256':sha(p),'status':r['status'],'error':r.get('error')})
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
 for i,v in enumerate(r.get('screened_peaks',[])):
  flags=set(v['flags']);base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'};extra={'secondary_unmeasurable','fewer_than_3_supported_events'}
  if flags<=base:eligible['followup'].add((r['tic'],i))
  if flags<=base|extra and flags&extra and v['diagnostics']['supported_events']>=2:eligible['coverage-followup'].add((r['tic'],i))
terminal=(out/'results.json').exists()
if terminal:
 rows=read(out/'results.json');assert len(rows)==len(inventory)==len(expected)==123
 assert {r['tic'] for r in rows}==set(expected)
 for r in rows:
  actual=read(out/'targets'/f"{r['tic']}.json");assert all(v==actual.get(k) for k,v in r.items())
follow={}
for suffix,keys in eligible.items():
 root=Path(f'results/qlp-faint-midradius-near-reserved-remaining-{suffix}-20261011');p=root/'terminal.json'
 if p.exists():
  d=read(p);assert d['status']=='complete' and {(r['tic'],r['peak_index']) for r in d['records']}==keys
  for r in d['records']:assert sha(Path(r['discovery_path']))==r['discovery_sha256']
  follow[suffix]=d
 else:follow[suffix]={'status':'not_terminal','eligible':sorted(keys)}
for tic,t in expected.items():
 if not any(tic==x[0] for keys in eligible.values() for x in keys):
  assert all(not Path(f'data/qlp/{tic}-s{s:04d}.fits').exists() for s in t['heldout_sectors'])
n=len(inventory)
save_json(out/f'checkpoint-{n}-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'n_completed':n,'terminal_results_present':terminal,'counts':dict(counts),'inventory':inventory,'followup':follow,'limits':'File reconciliation is not process liveness or source inspection. Eligible fits need plot/source review. Unusable inputs are not nondetections.'})
print(n,dict(counts),{k:sorted(v) for k,v in eligible.items()})
