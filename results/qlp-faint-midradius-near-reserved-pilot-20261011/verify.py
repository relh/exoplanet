from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());selection=read(out/'selection.json');targets=read(out/'eligible.json');pilot=read(out/'selected.json');plan=read(out/'plan.json');assert len(targets)==139 and pilot==targets[:16]==plan['targets']
assert sha(out/'eligible.json')==selection['eligible_sha256'] and sha(out/'selected.json')==selection['selected_sha256']
for path,h in selection['inputs'].items():assert sha(Path(path))==h
inv=read(Path('results/qlp-faint-midradius-unused-coverage-audit-20261011/inventory.json'));expected=[r for r in inv if r['category']=='multiple_sectors_without_distant_reserve'];assert [t['tic'] for t in targets]==[r['tic'] for r in expected]
for t,r in zip(targets,expected):
 assert t['sectors']==r['sectors']
 candidates=[]
 for n in range(1,4):
  for start in t['sectors']:
   block=list(range(start,start+n));remaining=set(t['sectors'])-set(block)
   if set(block)<=set(t['sectors']) and remaining:candidates.append((n,start,block))
 _,_,best=max(candidates);assert t['training_sectors']==best
 reserved=sorted(set(t['sectors'])-set(best),key=lambda s:(-min(abs(s-x) for x in best),s));assert reserved==t['heldout_sectors']
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in reserved)
 if t not in pilot:assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
results=read(out/'results.json');assert len(results)==16;counts=Counter()
for t in pilot:
 p=out/'targets'/f"{t['tic']}.json";r=read(p);assert r['target']==t;counts[r.get('disposition') or r['status']]+=1
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{t['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
for suffix in ['followup','coverage-followup']:
 p=Path(f'results/qlp-faint-midradius-near-reserved-pilot-{suffix}-20261011/terminal.json');r=read(p);assert r['status']=='complete' and r['records']==[]
controls=[]
for suffix in ['injections','larger-injections']:
 root=Path(f'results/qlp-faint-midradius-near-reserved-{suffix}-20261011');p=read(root/'plan.json');assert [t['tic'] for t in p['targets']]==[t['tic'] for t in pilot[:3]] and p['parent_sha256']==sha(out/'plan.json')
 audit=read(root/'audit.json');assert audit['terminal'] and audit['n_completed']==12
 for row in audit['rows']:
  path=Path(row['path']);assert sha(path)==row['source_sha256'];d=read(path);assert row['status']==d['status']=='screened' and row['error'] is None
  assert .5<=row['period']<=min(30,d['clean_baseline_days']/2)
  controls.append(row)
 for t in p['targets']:assert read(root/f"{t['tic']}-baseline-equivalence.json")['exact_arrays_equal']
assert len(controls)==24
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'selection_sha256':sha(out/'selection.json'),'plan_sha256':sha(out/'plan.json'),'counts':dict(counts),'n_controls':len(controls),'status':'139 metadata splits independently reconstructed;16 discovery identities/raw hashes;empty follow-up policies;reserved cache absence;24 control hashes and grid bounds checked. Three control stars all use single discovery sectors; this does not calibrate multi-sector or all-survey sensitivity.'})
print(dict(counts),'24controls verified')
