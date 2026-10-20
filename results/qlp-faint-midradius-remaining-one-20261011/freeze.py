"""Freeze the remaining single-sector tier after the reviewed 16-star pilot."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
source=Path('results/qlp-faint-midradius-coverage-20261011/selected-one.json')
prior=Path('results/qlp-faint-midradius-one-pilot-20261011/selected.json')
four=Path('results/qlp-faint-midradius-coverage-20261011/selected-four.json')
three=Path('results/qlp-faint-midradius-coverage-20261011/selected-three.json')
read=lambda p:json.loads(p.read_text())
alltargets=read(source);targets=alltargets[16:]
assert len(alltargets)==5732 and len(targets)==5716 and read(prior)==alltargets[:16]
assert len({t['tic'] for t in alltargets})==5732
assert not {t['tic'] for t in alltargets}&{t['tic'] for t in read(four)}
assert not {t['tic'] for t in alltargets}&{t['tic'] for t in read(three)}
two=Path('results/qlp-faint-midradius-coverage-20261011/selected-two.json')
assert not {t['tic'] for t in alltargets}&{t['tic'] for t in read(two)}
assert not (out/'selected.json').exists()
for t in targets:
    assert len(t['training_sectors'])==1 and len(t['heldout_sectors'])>=2
    assert not set(t['training_sectors'])&set(t['heldout_sectors'])
    assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets)
save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'source_sha256':sha(source),'prior_pilot_sha256':sha(prior),'four_sector_selection_sha256':sha(four),'three_sector_selection_sha256':sha(three),
    'two_sector_selection_sha256':sha(two),'selected_sha256':sha(out/'selected.json'),'n_selected':5716,'slice_start':16,'slice_stop':5732,
    'cache_absent_at_freeze':True,'policy':'All remaining single-sector metadata targets after the first16. Disjoint from the entire four-, three- and two-sector tiers. Unchanged discovery gates; reserved epochs untouched until separately frozen eligible follow-up. Original failures retained. Not whole TESS, proof of novelty or completeness.'})
print('Frozen remaining',len(targets),'single-sector targets')
