from pathlib import Path
import json
from collections import Counter
from astropy.timeseries import BoxLeastSquares
from exoplanet.campaign import DURATIONS
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());coverage=Path('results/qlp-faint-midradius-coverage-20261011');selection=read(coverage/'selection-one.json');targets=read(coverage/'selected-one.json');p=read(out/'plan.json');pilot=read(out/'selected.json');a=read(out/'audit.json')
assert selection['script_sha256']==sha(coverage/'select_one.py') and selection['selected_sha256']==sha(coverage/'selected-one.json')
assert len(targets)==selection['n_selected']==5732 and len({t['tic'] for t in targets})==5732
prior={t['tic'] for n in ['four','three','two'] for t in read(coverage/f'selected-{n}.json')};assert not prior&{t['tic'] for t in targets}
for source in selection['sources']:assert sha(Path(source['path']))==source['sha256']
for t in targets:
 assert len(t['training_sectors'])==1 and len(t['heldout_sectors'])>=2
 assert not set(t['training_sectors'])&set(t['heldout_sectors'])
 options=[s for s in t['sectors'] if sum(abs(h-s)>=8 for h in t['sectors'])>=2]
 assert t['training_sectors']==[max(options)]
 assert t['heldout_sectors']==[s for s in t['sectors'] if abs(s-t['training_sectors'][0])>=8]
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['heldout_sectors'])
assert pilot==targets[:16]==p['targets'];assert p['source_sha256']==sha(out/'selected.json') and p['script_sha256']==sha(out/'run.py')
for name,h in p['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==h
rows=read(out/'results.json');assert len(rows)==16 and {r['tic'] for r in rows}=={t['tic'] for t in pilot};counts=Counter()
for item in a['inventory']:
 path=Path(item['path']);assert sha(path)==item['sha256'];r=read(path);counts[r.get('disposition',r['status'])]+=1
 assert r['target']==next(t for t in pilot if t['tic']==r['tic'])
 for data in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{data['sector']:04d}.fits"))==data['source']['sha256']
assert dict(counts)==a['counts'] and not a['review']
controls=[]
for name in ['qlp-faint-midradius-one-injections-20261011','qlp-faint-midradius-one-larger-injections-20261011']:
 root=Path('results')/name;plan=read(root/'plan.json');audit=read(root/'audit.json');rr=read(root/'results.json');assert plan['script_sha256']==sha(root/'run.py') and audit['input_sha256']==sha(root/'results.json');assert len(rr)==12 and audit['terminal']
 for target in plan['targets']:
  equiv=read(root/f"{target['tic']}-baseline-equivalence.json");assert equiv['exact_arrays_equal'] and equiv['discovery_sha256']==sha(out/'targets'/f"{target['tic']}.json")
 bounds=[]
 for row in audit['rows']:
  path=Path(row['path']);assert sha(path)==row['source_sha256'];d=read(path);baseline=d['clean_baseline_days'];grid=BoxLeastSquares([0,baseline],[1,1]).autoperiod(DURATIONS,minimum_period=.5,maximum_period=min(20,baseline/2.5),frequency_factor=2)
  bounds.append({'tic':row['tic'],'period':row['period'],'radius_earth':row['radius_earth'],'grid_min':float(min(grid)),'grid_max':float(max(grid)),'in_grid':bool(min(grid)<=row['period']<=max(grid))})
 save_json(root/'bounds.json',{'audit_sha256':sha(root/'audit.json'),'rows':bounds})
 controls.append({'directory':name,'n':len(rr),'period_recovered':audit['n_top3_period_recovered'],'screen_pass':audit['n_noncrowding_pass'],'in_grid':sum(x['in_grid'] for x in bounds),'phase_consistent_matches':sum(any(m['within_half_injected_duration_at_three_times'] for m in x['matches']) for x in audit['rows'])})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'selection_sha256':sha(coverage/'selection-one.json'),'audit_sha256':sha(out/'audit.json'),'counts':dict(counts),'controls':controls,'status':'Frozen coverage, disjoint tiers, terminal16 targets, raw input hashes, retained failures, reserved cache absence and injection bounds verified. No completeness or candidate validation.'})
print(dict(counts),controls)
