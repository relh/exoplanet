"""Freeze the remaining scoped four-sector pool before its photometry is opened."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json, sha, now

out=Path(__file__).parent
source=Path('results/qlp-faint-midradius-coverage-20261011/selected-four.json')
read=lambda p:json.loads(p.read_text())
alltargets=read(source)
prior=[Path('results/qlp-faint-midradius-four-pilot-20261011/selected.json'),
       Path('results/qlp-faint-midradius-next32-20261011/selected.json')]
assert read(prior[0])+read(prior[1])==alltargets[:48]
targets=alltargets[48:]
assert len(alltargets)==1073 and len(targets)==1025
assert len({t['tic'] for t in alltargets})==len(alltargets)
assert not (out/'selected.json').exists()
assert all(len(t['training_sectors'])==4 and len(t['heldout_sectors'])>=2 for t in targets)
for t in targets:
    assert not set(t['training_sectors'])&set(t['heldout_sectors'])
    assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets)
save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'source':str(source),'source_sha256':sha(source),'prior_selection_hashes':{str(p):sha(p) for p in prior},
    'selected_sha256':sha(out/'selected.json'),'slice_start':48,'slice_stop':1073,
    'n_selected':len(targets),'cache_absent_at_freeze':True,
    'policy':'All remaining 1025 of the dated metadata-ranked four-sector midradius selection. Four training sectors and at least two distant reserved sectors per star. Unchanged screening and baseline limits; keep failures. Scope is not all TESS, not demonstrated novelty or underexploration by others, and not survey completeness.'})
print('Frozen remaining',len(targets),'targets')
