from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;read=lambda q:json.loads(q.read_text());plan=read(p/'plan.json');eligible=read(p/'eligible.json');selected=read(p/'selected.json');excluded=read(p/'exclusions.json')
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
assert sha(p/'select.py')==plan['selection_script_sha256']
assert len(eligible)+len(excluded)==plan['n_input']==16581
assert len(eligible)==len({r['tic'] for r in eligible})==7004
assert {r['tic'] for r in eligible}.isdisjoint(r['tic'] for r in excluded)
assert selected==sorted(eligible,key=lambda r:(r['priority_noise_proxy'],r['tic']))[:16]
for r in selected:
 assert 2<=len(r['training_sectors'])<=3
 assert all(b-a==1 for a,b in zip(r['training_sectors'],r['training_sectors'][1:]))
 assert max(r['training_sectors'])<=55<min(r['heldout_sectors'])
 for s in r['heldout_sectors']:assert not Path(f'data/lightcurves/s{s:04d}-{r["tic"]}.fits').exists()
save_json(p/'verification.json',dict(status='passed',selected=16,eligible=7004,partition_reconciled=True,reserved_cache_absent=True,selection_sha256=sha(p/'selected.json')))
