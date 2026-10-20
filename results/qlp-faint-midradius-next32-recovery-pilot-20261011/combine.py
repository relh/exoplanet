"""Reconcile alternate-window attempts with original distinct-star inventory."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha, save_json, now
out = Path(__file__).parent
original = Path('results/qlp-faint-midradius-next32-20261011')
read = lambda p: json.loads(p.read_text())
old = {r['tic']: r for r in read(original/'results.json')}
new = {r['tic']: r for r in read(out/'results.json')}
assert set(new) == {tic for tic,r in old.items() if r['status']=='error'}
assert len(old)==32 and len(new)==5
inventory=[]
for tic in old:
    op = original/'targets'/f'{tic}.json'
    a=read(op)
    if tic in new:
        np = out/'targets'/f'{tic}.json'
        b=read(np)
        assert b['status']=='screened'
        assert b['target']['training_sectors']==([95,96,97] if tic==32036415 else [97,98])
        assert b['target']['heldout_sectors']==a['target']['heldout_sectors']
        assert set(b['target']['training_sectors'])<=set(a['target']['training_sectors'])
        inventory.append({'tic':tic,'original_path':str(op),'original_sha256':sha(op),'usable_path':str(np),'usable_sha256':sha(np),'disposition':b['disposition']})
    else:
        assert a['status']=='screened'
        inventory.append({'tic':tic,'original_path':str(op),'original_sha256':sha(op),'usable_path':str(op),'usable_sha256':sha(op),'disposition':a['disposition']})
save_json(out/'combined.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'n_distinct_stars':len(inventory),'n_original_baseline_failures':len(new),
    'n_reduced_window_usable':len(new),'counts':dict(Counter(r['disposition'] for r in inventory)),
    'inventory':inventory,'limits':'Five original four-sector failures remain failures. Alternate reduced-window attempts add usable windows, not distinct stars or repaired four-sector searches. No completeness or planet claim.'})
print('Distinct usable:',len(inventory),'counts:',dict(Counter(r['disposition'] for r in inventory)))
