"""Freeze the remaining three-sector tier after the reviewed 16-star pilot."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
source=Path('results/qlp-faint-midradius-coverage-20261011/selected-three.json')
prior=Path('results/qlp-faint-midradius-three-pilot-20261011/selected.json')
four=Path('results/qlp-faint-midradius-coverage-20261011/selected-four.json')
read=lambda p:json.loads(p.read_text())
alltargets=read(source);targets=alltargets[16:]
assert len(alltargets)==1509 and len(targets)==1493 and read(prior)==alltargets[:16]
assert len({t['tic'] for t in alltargets})==1509
assert not {t['tic'] for t in alltargets}&{t['tic'] for t in read(four)}
assert not (out/'selected.json').exists()
for t in targets:
    assert len(t['training_sectors'])==3 and len(t['heldout_sectors'])>=2
    assert not set(t['training_sectors'])&set(t['heldout_sectors'])
    assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets)
save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'source_sha256':sha(source),'prior_pilot_sha256':sha(prior),'four_sector_selection_sha256':sha(four),
    'selected_sha256':sha(out/'selected.json'),'n_selected':1493,'slice_start':16,'slice_stop':1509,
    'cache_absent_at_freeze':True,'policy':'All remaining three-sector metadata targets after the first16. Disjoint from the entire four-sector tier. Unchanged discovery gates; reserved epochs untouched until separately frozen eligible follow-up. Original failures retained. Not whole TESS, proof of novelty or completeness.'})
print('Frozen remaining',len(targets),'three-sector targets')
