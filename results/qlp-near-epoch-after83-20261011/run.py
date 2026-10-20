"""Metadata-only near-epoch tier, excluding every previous selected or cached target."""
from pathlib import Path
from collections import Counter
import json,re
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
assert not (out/'inventory.json').exists()
base=Path('results/qlp-faint-pool-coverage-20261010')
previous=Path('results/qlp-faint-one-reserved-after35-20261010/coverage.json')
prior_inventory=json.loads(previous.read_text());prior=set()
for name,h in prior_inventory['prior_selections'].items():
 p=Path(name);assert sha(p)==h
 prior.update(t['tic'] for t in json.loads(p.read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector43-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector46-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector71-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector51-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector92-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector16-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector79-selection-20261011/selected.json').read_text()))
prior.update(t['tic'] for t in json.loads(Path('results/qlp-near-epoch-sector83-selection-20261011/selected.json').read_text()))
run=json.loads((base/'run.json').read_text());poolp=Path(run['pool_path'])
assert sha(poolp)==run['pool_sha256']
pool=json.loads(poolp.read_text());cached=set()
for folder,pattern in [('data/qlp',r'(\d+)-s.*\.fits'),('data/lightcurves',r's.*-(\d+)\.fits')]:
 for p in Path(folder).glob('*.fits'):
  m=re.fullmatch(pattern,p.name)
  if m:cached.add(int(m[1]))
obs={};sources=[]
for q in json.loads((base/'queries.json').read_text()):
 assert q['status']=='complete'
 p=Path(f"data/qlp-coverage-faint-20261010/chunk-{q['offset']}.json")
 assert sha(p)==q['evidence']['sha256']
 r=json.loads(p.read_text());assert len(r['data'])==r['paging']['rowsFiltered']
 sources.append({'path':str(p),'sha256':sha(p)})
 for row in r['data']:obs.setdefault(int(row['target_name']),{}).setdefault(int(row['sequence_number']),[]).append(row)
counts=Counter();eligible=[];by_sector={}
for target in pool:
 tic=target['tic'];products=obs.get(tic,{})
 if tic in prior:counts['previously_selected']+=1;continue
 if tic in cached:counts['cached_photometry']+=1;continue
 if not products:counts['no_products']+=1;continue
 if any(len({r['dataURL'] for r in rs})!=1 for rs in products.values()):counts['ambiguous_products']+=1;continue
 if len(products)<2:counts['only_one_sector']+=1;continue
 assert max(products)-min(products)<8,'Distant-reserved tier not exhausted'
 row=dict(target,sectors=sorted(products),qlp_products={str(s):rs[0] for s,rs in products.items()},estimate_missing_errors=True)
 eligible.append(row)
 for s in products:by_sector.setdefault(s,[]).append(tic)
ranked=[{'sector':s,'n_targets':len(ids),'tics':ids} for s,ids in sorted(by_sector.items(),key=lambda x:(-len(x[1]),-x[0]))]
save_json(out/'eligible.json',eligible)
save_json(out/'inventory.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_sha256':sha(poolp),'previous_inventory_sha256':sha(previous),'additional_prior_selections':{'results/qlp-near-epoch-sector43-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector43-selection-20261011/selected.json')),'results/qlp-near-epoch-sector46-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector46-selection-20261011/selected.json')),'results/qlp-near-epoch-sector71-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector71-selection-20261011/selected.json')),'results/qlp-near-epoch-sector51-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector51-selection-20261011/selected.json')),'results/qlp-near-epoch-sector92-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector92-selection-20261011/selected.json')),'results/qlp-near-epoch-sector16-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector16-selection-20261011/selected.json')),'results/qlp-near-epoch-sector79-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector79-selection-20261011/selected.json')),'results/qlp-near-epoch-sector83-selection-20261011/selected.json':sha(Path('results/qlp-near-epoch-sector83-selection-20261011/selected.json'))},'n_pool':len(pool),'n_prior_distinct':len(prior),'n_eligible':len(eligible),'exclusions':dict(counts),'sources':sources,'ranked_sectors':ranked,'eligible_sha256':sha(out/'eligible.json'),'policy':'Separate near-epoch exploratory tier: at least2 distinct observing sectors but none8sector numbers apart. Exclude all previous selections and cached target photometry. Existing transit gates unchanged. Different cadences are not independent long-term replication; shared seasonal/instrumental systematics may persist. No photometry opened, novelty or completeness claim.'})
print('eligible',len(eligible),'exclusions',dict(counts),'ranked',[(r['sector'],r['n_targets']) for r in ranked[:10]])
