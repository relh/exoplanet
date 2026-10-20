"""Freeze a bounded first pilot in the unchanged metadata ranking."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-coverage-20261011/selected-three.json');alltargets=json.loads(source.read_text());targets=alltargets[:16]
assert len(targets)==16 and not (out/'selected.json').exists()
assert all(len(t['training_sectors'])==3 and len(t['heldout_sectors'])>=2 for t in targets)
for t in targets:
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets)
save_json(out/'selection.json',{'utc':now(),'source_sha256':sha(source),'selected_sha256':sha(out/'selected.json'),'script_sha256':sha(Path(__file__)),'n_pool_three':len(alltargets),'n_pilot':len(targets),'policy':'First16in original radius/brightness metadata order, before target photometry. Three discovery sectors; all distant reserved sectors held out. Initial pilot, not whole selected pool or completeness. Existing gates unchanged; validate controls and followups before expanding.'})
print('Frozen16 of',len(alltargets))
