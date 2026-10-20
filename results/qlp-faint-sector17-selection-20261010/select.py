"""Freeze untouched Sector 17 targets using metadata and prior access only."""
from pathlib import Path
from collections import Counter
import json,re
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/qlp-faint-pool-coverage-20261010')
assert not (out/'selected.json').exists()
run=json.loads((base/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0
poolp=Path(run['pool_path']);assert sha(poolp)==run['pool_sha256']
pool=json.loads(poolp.read_text())
prior_paths=[base/'selected-four.json',Path('results/qlp-faint-sector98-selection-20261010/selected.json'),Path('results/qlp-faint-sector104-selection-20261010/selected.json'),Path('results/qlp-faint-sector100-selection-20261010/selected.json'),Path('results/qlp-faint-sector99-selection-20261010/selected.json'),Path('results/qlp-faint-sector101-selection-20261010/selected.json'),Path('results/qlp-faint-sector102-selection-20261010/selected.json'),Path('results/qlp-faint-sector103-selection-20261010/selected.json')]
prior_paths.append(Path('results/qlp-faint-sector97-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector70-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector72-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector52-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector76-selection-20261010/selected.json'))
prior_paths.append(Path('results/qlp-faint-sector60-selection-20261010/selected.json'))
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
selected=[];counts=Counter()
for target in pool:
    tic=target['tic'];products=obs.get(tic,{})
    if tic in prior:counts['prior_selections']+=1;continue
    if 17 not in products:counts['no_sector17']+=1;continue
    if any(len({r['dataURL'] for r in rs})!=1 for rs in products.values()):counts['ambiguous_product']+=1;continue
    held=sorted(s for s in products if abs(s-17)>=8)
    if len(held)<2:counts['fewer_than_two_reserved_sectors']+=1;continue
    if tic in cached:counts['previous_photometry_cache']+=1;continue
    selected.append(dict(target,sectors=sorted(products),training_sectors=[17],heldout_sectors=held,
                         qlp_products={str(s):rs[0] for s,rs in products.items()},estimate_missing_errors=True))
save_json(out/'selected.json',selected)
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_sha256':sha(poolp),
    'prior_selections':{str(p):sha(p) for p in prior_paths},'n_prior_distinct':len(prior),
    'n_cached_tics':len(cached),'n_pool':len(pool),'n_selected':len(selected),
    'exclusions':dict(counts),'sources':sources,'selected_sha256':sha(out/'selected.json'),
    'policy':'Metadata-only Sector17 selection, preserving existing radius/noise ranking and dated catalog exclusions. Exclude all previous four-sector, Sector98, Sector104, Sector100, Sector99, Sector101, Sector102, Sector103, Sector97, Sector70, Sector72 Sector52, Sector76 and Sector60 selections and any cached QLP/SPOC target photometry. Require two reserved sectors at least eight sector numbers away. No photometry opened. New to this search is not evidence of novelty or underexploration.'})
print('selected',len(selected),'excluded',dict(counts))
