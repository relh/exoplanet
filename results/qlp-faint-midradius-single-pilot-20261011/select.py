from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());inv=Path('results/qlp-faint-midradius-unused-coverage-audit-20261011/inventory.json');used=Path('results/alternate-epochs-nine-20261011/selected.json');excluded={t['tic'] for t in read(used)};old=read(Path('results/qlp-faint-midradius-one-reserved-pilot-20261011/selection.json'));pool=Path(old['pool_path']);assert sha(pool)==old['pool_sha256'];stars={t['tic']:t for t in read(pool)};obs={}
for src in old['coverage_sources']:
 p=Path(src['path']);assert sha(p)==src['sha256']
 for r in read(p)['data']:obs.setdefault(int(r['target_name']),{})[int(r['sequence_number'])]=r
rows=[]
for r in read(inv):
 if r['category']!='single_sector_only' or r['tic'] in excluded:continue
 tic=r['tic'];sectors=r['sectors'];assert len(sectors)==1
 assert not Path(f'data/qlp/{tic}-s{sectors[0]:04d}.fits').exists()
 rows.append(dict(stars[tic],sectors=sectors,training_sectors=sectors,heldout_sectors=[],estimate_missing_errors=True,qlp_products={str(s):obs[tic][s] for s in sectors}))
assert len(rows)==1477 and not (out/'selected.json').exists()
save_json(out/'eligible.json',rows);save_json(out/'selected.json',rows[:16]);save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inputs':{str(inv):sha(inv),str(used):sha(used),str(pool):sha(pool)},'eligible_sha256':sha(out/'eligible.json'),'selected_sha256':sha(out/'selected.json'),'policy':'First16 of1477 remaining single-sector targets in original metadata order. No held sectors available in queried products. Controls first3 without replacement. No independent-sector validation possible; candidate screening only, followed by catalog/pixel review if eligible.'})
print([(t['tic'],t['sectors']) for t in rows[:16]])
