"""Freeze the next bounded batch in the unchanged metadata ranking."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-coverage-20261011/selected-four.json');alltargets=json.loads(source.read_text());targets=alltargets[16:48]
assert len(targets)==32 and not (out/'selected.json').exists()
previous=Path('results/qlp-faint-midradius-four-pilot-20261011/selected.json')
assert json.loads(previous.read_text())==alltargets[:16]
assert not {t['tic'] for t in targets}&{t['tic'] for t in alltargets[:16]}
assert all(len(t['training_sectors'])==4 and len(t['heldout_sectors'])>=2 for t in targets)
for t in targets:
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets)
save_json(out/'selection.json',{'utc':now(),'source_sha256':sha(source),'previous_selection_sha256':sha(previous),'slice_start':16,'slice_stop':48,'selected_sha256':sha(out/'selected.json'),'script_sha256':sha(Path(__file__)),'n_pool_four':len(alltargets),'n_batch':len(targets),'policy':'Next 32 after the original 16 in original radius/brightness metadata order, before target photometry. Four discovery sectors; all distant reserved sectors held out. Metadata expansion after reviewing the first 16 and their recovery controls. Not whole selected pool or completeness; existing gates unchanged.'})
print('Frozen next32 of',len(alltargets))
