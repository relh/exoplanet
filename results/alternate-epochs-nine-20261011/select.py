from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());a=Path('results/unused-other-products-20261011/audit.json');old=read(Path('results/qlp-faint-midradius-one-reserved-pilot-20261011/selection.json'));pool=Path(old['pool_path']);assert sha(pool)==old['pool_sha256'];stars={t['tic']:t for t in read(pool)};obs={}
for src in old['coverage_sources']:
 p=Path(src['path']);assert sha(p)==src['sha256']
 for r in read(p)['data']:obs.setdefault(int(r['target_name']),{})[int(r['sequence_number'])]=r
rows=[]
for r in read(a)['rows']:
 if r['category']!='additional_sector_metadata':continue
 tic=r['tic'];train=r['sectors'] or [106];held=r['additional_sectors'] if r['sectors'] else [107]
 t=dict(stars[tic],training_sectors=train,heldout_sectors=held,estimate_missing_errors=True,discovery_collection='QLP' if r['sectors'] else 'SPOC',qlp_products={str(s):obs[tic][s] for s in r['sectors']},other_products=r['observations'])
 rows.append(t)
assert len(rows)==9 and not (out/'selected.json').exists()
save_json(out/'selected.json',rows);save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_hashes':{str(a):sha(a),str(pool):sha(pool)},'selected_sha256':sha(out/'selected.json'),'policy':'All nine metadata opportunities. Use sole QLP sector for discovery where available; otherwise SPOC106 discovery107 reserve. All newly identified epochs held for QLP targets. Sector1751 special short epoch, no integer chronological interpretation. Same scientific gates; no photometry-driven selection.'})
print([(t['tic'],t['training_sectors'],t['heldout_sectors']) for t in rows])
