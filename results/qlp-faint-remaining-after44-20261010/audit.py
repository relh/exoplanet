"""Inventory remaining viable metadata after excluding the full Sector 21 selection."""
from pathlib import Path
from collections import Counter
import json,re
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/qlp-faint-pool-coverage-20261010')
assert not (out/'coverage.json').exists()
run=json.loads((base/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0
poolp=Path(run['pool_path']);assert sha(poolp)==run['pool_sha256']
pool=json.loads(poolp.read_text())
prior_paths=[base/'selected-four.json',Path('results/qlp-faint-sector98-selection-20261010/selected.json'),Path('results/qlp-faint-sector104-selection-20261010/selected.json'),Path('results/qlp-faint-sector100-selection-20261010/selected.json'),Path('results/qlp-faint-sector99-selection-20261010/selected.json'),Path('results/qlp-faint-sector101-selection-20261010/selected.json'),Path('results/qlp-faint-sector102-selection-20261010/selected.json'),Path('results/qlp-faint-sector103-selection-20261010/selected.json'),Path('results/qlp-faint-sector97-selection-20261010/selected.json')]
prior_paths.append(Path('results/qlp-faint-sector70-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector72-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector52-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector76-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector60-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector17-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector28-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector7-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector86-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector75-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector50-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector69-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector27-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector58-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector55-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector87-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector91-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector40-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector35-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector56-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector11-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector51-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector71-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector31-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector90-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector92-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector21-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector73-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector61-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector37-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector57-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector53-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector93-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector22-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector5-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector41-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector95-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector3-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector30-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector23-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector13-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector29-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector9-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector81-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector80-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector74-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector49-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector44-selection-20261010/selected.json'))
prior=set()
for p in prior_paths:prior.update(r['tic'] for r in json.loads(p.read_text()))
cached=set()
for folder,pattern in [('data/qlp',r'(\d+)-s.*\.fits'),('data/lightcurves',r's.*-(\d+)\.fits')]:
    for p in Path(folder).glob('*.fits'):
        m=re.fullmatch(pattern,p.name)
        if m:cached.add(int(m[1]))
obs={};sources=[]
for q in json.loads((base/'queries.json').read_text()):
    assert q['status']=='complete'
    p=Path(f"data/qlp-coverage-faint-20261010/chunk-{q['offset']}.json")
    assert sha(p)==q['evidence']['sha256'];r=json.loads(p.read_text())
    assert len(r['data'])==r['paging']['rowsFiltered']
    sources.append({'path':str(p),'sha256':sha(p)})
    for row in r['data']:obs.setdefault(int(row['target_name']),{}).setdefault(int(row['sequence_number']),[]).append(row)
counts=Counter(); by_sector={}; remaining=[]
for target in pool:
    tic=target['tic'];products=obs.get(tic,{})
    if tic in prior:counts['prior_selection']+=1;continue
    if tic in cached:counts['cached_photometry']+=1;continue
    if not products:counts['no_products']+=1;continue
    if any(len({r['dataURL'] for r in rs})!=1 for rs in products.values()):counts['ambiguous_products']+=1;continue
    viable=[s for s in products if sum(abs(other-s)>=8 for other in products)>=2]
    if not viable:counts['no_sector_with_two_reserved_epochs']+=1;continue
    remaining.append({'tic':tic,'sectors':sorted(products),'viable_training_sectors':sorted(viable)})
    for s in viable:by_sector.setdefault(s,[]).append(tic)
ranked=[{'sector':s,'n_targets':len(ids),'tics':ids} for s,ids in sorted(by_sector.items(),key=lambda x:(-len(x[1]),-x[0]))]
save_json(out/'coverage.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_sha256':sha(poolp),'n_pool':len(pool),'n_prior_distinct':len(prior),'n_cached_tics':len(cached),'prior_selections':{str(p):sha(p) for p in prior_paths},'sources':sources,'n_remaining_distinct':len(remaining),'exclusions':dict(counts),'ranked_sectors':ranked,'remaining':remaining,'policy':'Metadata-only inventory across every sector in the archived complete coverage query. Excludes every previous selection through the full Sector44 sample and cached target photometry. Requires two reserved epochs at least8sector numbers away. Counts overlap between sectors; not summed as distinct stars. No photometry opened, no novelty or completeness claim; archive snapshot limits apply.'})
print('remaining distinct',len(remaining),'top sectors',[(r['sector'],r['n_targets']) for r in ranked[:20]])
