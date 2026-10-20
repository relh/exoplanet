from pathlib import Path
import json
from collections import Counter
from astropy.timeseries import BoxLeastSquares
from exoplanet.campaign import DURATIONS
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());s=read(out/'selection.json');eligible=read(out/'eligible.json');pilot=read(out/'selected.json');plan=read(out/'plan.json');a=read(out/'audit.json');exclude=set(s['excluded_ids']);obs={}
assert s['script_sha256']==sha(out/'select.py') and sha(Path(s['pool_path']))==s['pool_sha256']
for source in s['prior_selection_sources']:assert sha(Path(source['path']))==source['sha256']
for source in s['coverage_sources']:
 p=Path(source['path']);assert sha(p)==source['sha256']
 for r in read(p)['data']:obs.setdefault(int(r['target_name']),{}).setdefault(int(r['sequence_number']),[]).append(r)
reconstructed=[]
for t in read(Path(s['pool_path'])):
 if t['tic'] in exclude:continue
 products=obs.get(t['tic'],{});sectors=sorted(products)
 if any(len({r['dataURL'] for r in v})!=1 for v in products.values()):continue
 options=[]
 for n in range(1,5):
  for start in sectors:
   train=list(range(start,start+n));held=[h for h in sectors if min(abs(h-x) for x in train)>=8]
   if set(train)<=set(sectors) and held:options.append((n,start,train,held))
 if not options:continue
 _,_,train,held=max(options);reconstructed.append(dict(t,sectors=sectors,training_sectors=train,heldout_sectors=held,estimate_missing_errors=True,qlp_products={str(k):v[0] for k,v in products.items()}))
assert reconstructed==eligible and len(eligible)==s['n_eligible']==2826
assert eligible[:16]==pilot==plan['targets'];assert sha(out/'selected.json')==s['selected_sha256']==plan['source_sha256']
assert sha(out/'eligible.json')==s['eligible_sha256'] and sha(out/'run.py')==plan['script_sha256']
for n,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/n)==h
rows=read(out/'results.json');assert len(rows)==16 and {r['tic'] for r in rows}=={t['tic'] for t in pilot};counts=Counter();coverage_eligible=[]
for item in a['inventory']:
 p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p);counts[r.get('disposition') or r['status']]+=1
 assert r['target']==next(t for t in pilot if t['tic']==r['tic'])
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
 for i,peak in enumerate(r.get('screened_peaks',[])):
  flags=set(peak['flags'])
  if flags<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period','secondary_unmeasurable','fewer_than_3_supported_events'} and flags&{'secondary_unmeasurable','fewer_than_3_supported_events'} and peak['diagnostics']['supported_events']>=2:coverage_eligible.append((r['tic'],i))
assert dict(counts)==a['counts'] and not a['review'] and not coverage_eligible
for t in pilot:
 for h in t['heldout_sectors']:assert not Path(f"data/qlp/{t['tic']}-s{h:04d}.fits").exists()
controls=[]
for name in ['qlp-faint-midradius-one-reserved-injections-20261011','qlp-faint-midradius-one-reserved-larger-injections-20261011']:
 root=Path('results')/name;cp=read(root/'plan.json');ca=read(root/'audit.json');rr=read(root/'results.json');assert len(rr)==12 and ca['terminal'] and ca['input_sha256']==sha(root/'results.json') and cp['script_sha256']==sha(root/'run.py');bounds=[]
 for target in cp['targets']:
  e=read(root/f"{target['tic']}-baseline-equivalence.json");assert e['exact_arrays_equal'] and e['discovery_sha256']==sha(out/'targets'/f"{target['tic']}.json")
 for row in ca['rows']:
  p=Path(row['path']);assert sha(p)==row['source_sha256'];d=read(p);baseline=d['clean_baseline_days'];grid=BoxLeastSquares([0,baseline],[1,1]).autoperiod(DURATIONS,minimum_period=.5,maximum_period=min(20,baseline/2.5),frequency_factor=2);bounds.append({'tic':row['tic'],'period':row['period'],'radius':row['radius_earth'],'in_grid':bool(min(grid)<=row['period']<=max(grid))})
 save_json(root/'bounds.json',bounds);controls.append({'name':name,'n':len(rr),'period_recovered':ca['n_top3_period_recovered'],'screen_pass':ca['n_noncrowding_pass'],'in_grid':sum(b['in_grid'] for b in bounds)})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'selection_sha256':sha(out/'selection.json'),'audit_sha256':sha(out/'audit.json'),'counts':dict(counts),'coverage_eligible':coverage_eligible,'controls':controls,'status':'All2826 metadata choices reconstructed,16 terminal searches/raw hashes reconciled, both follow-up policies empty, reserved caches absent,24 injections/loader equality/grid bounds verified. No completeness or candidate validation.'});print(dict(counts),controls)
