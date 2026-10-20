from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
sector=97
inventory=Path('results/qlp-faint-one-reserved-after78-20261010/coverage.json')
d=json.loads(inventory.read_text())
selected=out/'selected.json';a=json.loads(selected.read_text())
prior=set()
for name,digest in d['prior_selections'].items():
 p=Path(name);assert sha(p)==digest
 prior.update(r['tic'] for r in json.loads(p.read_text()))
actual={r['tic'] for r in a}
expected=set(next(r['tics'] for r in d['ranked_sectors'] if r['sector']==sector))
assert len(actual)==len(a) and actual==expected and not actual&prior
save_json(out/'full-inventory-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory_sha256':sha(inventory),'selected_sha256':sha(selected),'n_selected':len(a),'n_complete_prior':len(prior),'prior_overlap':[],'exact_expected_set':True,'limitation':'Original selection script copied sector text into historical exclusion paths. Its exclusion-count provenance is defective. Full authoritative inventory independently verifies the exact selected set and zero prior overlap; original artifacts retained. Use authoritative prior paths for future selections.'})
