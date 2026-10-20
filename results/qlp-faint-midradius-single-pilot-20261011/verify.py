from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());sel=read(out/'selection.json');plan=read(out/'plan.json');alltargets=read(out/'eligible.json');pilot=read(out/'selected.json');assert len(alltargets)==1477 and pilot==alltargets[:16]==plan['targets']
assert sha(out/'eligible.json')==sel['eligible_sha256'] and sha(out/'selected.json')==sel['selected_sha256']==plan['source_sha256']
for p,h in sel['inputs'].items():assert sha(Path(p))==h
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
assert sha(out/'run.py')==plan['script_sha256']
inv=read(Path('results/qlp-faint-midradius-unused-coverage-audit-20261011/inventory.json'));used={t['tic'] for t in read(Path('results/alternate-epochs-nine-20261011/selected.json'))};expected=[r for r in inv if r['category']=='single_sector_only' and r['tic'] not in used];assert [t['tic'] for t in alltargets]==[r['tic'] for r in expected]
for t,r in zip(alltargets,expected):
 assert t['training_sectors']==r['sectors'] and t['heldout_sectors']==[]
 if t not in pilot:assert not Path(f"data/qlp/{t['tic']}-s{t['training_sectors'][0]:04d}.fits").exists()
counts=Counter();eligible=[];results=read(out/'results.json');assert len(results)==16
for t in pilot:
 r=read(out/'targets'/f"{t['tic']}.json");assert r['target']==t;counts[r.get('disposition') or r['status']]+=1
 summary=next(x for x in results if x['tic']==t['tic']);assert all(r.get(k)==v for k,v in summary.items())
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{t['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
 for i,v in enumerate(r.get('screened_peaks',[])):
  flags=set(v['flags']);base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'};extra={'secondary_unmeasurable','fewer_than_3_supported_events'}
  if flags<=base or (flags<=base|extra and flags&extra and v['diagnostics']['supported_events']>=2):eligible.append((t['tic'],i))
assert eligible==[]
controls=[]
for suffix in ['injections','larger-injections']:
 root=Path(f'results/qlp-faint-midradius-single-{suffix}-20261011');p=read(root/'plan.json');assert p['targets']==pilot[:3] and p['parent_sha256']==sha(out/'plan.json')
 audit=read(root/'audit.json');assert audit['terminal'] and audit['n_completed']==12 and audit['input_sha256']==sha(root/'results.json')
 for row in audit['rows']:
  path=Path(row['path']);assert sha(path)==row['source_sha256'];d=read(path);assert row['status']==d['status']=='screened' and row['error'] is None
  assert .5<=row['period']<=min(20,d['clean_baseline_days']/2.5)
  controls.append(row)
 for t in p['targets']:assert read(root/f"{t['tic']}-baseline-equivalence.json")['exact_arrays_equal']
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'counts':dict(counts),'eligible':eligible,'n_controls':len(controls),'status':'Frozen1477 order,16 target/raw hashes,empty follow-up eligibility and24 control hashes/grid bounds checked. No independent observing epoch available; no completeness claim.'})
print(dict(counts),len(controls),'controls')
