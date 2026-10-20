from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/qlp-faint-midradius-one-reserved-pilot-20261011');read=lambda p:json.loads(p.read_text());alltargets=read(base/'eligible.json');prior=read(base/'selected.json');targets=alltargets[16:]
assert len(alltargets)==2826 and len(targets)==2810 and alltargets[:16]==prior
assert len({t['tic'] for t in alltargets})==2826 and not (out/'selected.json').exists()
for t in targets:
 assert 1<=len(t['training_sectors'])<=4 and len(t['heldout_sectors'])>=1
 assert all(min(abs(h-s) for s in t['training_sectors'])>=8 for h in t['heldout_sectors'])
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'selected.json',targets);save_json(out/'selection.json',{'utc':now(),'source_sha256':sha(base/'eligible.json'),'pilot_sha256':sha(base/'selected.json'),'pilot_verification_sha256':sha(base/'verification.json'),'selected_sha256':sha(out/'selected.json'),'script_sha256':sha(Path(__file__)),'n_selected':len(targets),'training_lengths':dict(Counter(len(t['training_sectors']) for t in targets)),'reserved_lengths':dict(Counter(len(t['heldout_sectors']) for t in targets)),'cache_absent_at_freeze':True,'policy':'Entire remaining frozen metadata sample after16pilot; no outcome-based reselection. Original gates/baseline120days retained. One distant reserved epoch is weaker replication; errors retained without substitution. Sensitivity limited to pilot3stars/24trials, not completeness.'});print(len(targets),Counter(len(t['training_sectors']) for t in targets),Counter(len(t['heldout_sectors']) for t in targets))
