"""Frozen all 16 metadata-ranked single faint midradius pilot targets; no reserved epochs available."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target, SETTINGS
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
source = Path('results/qlp-faint-midradius-single-pilot-20261011/selected.json')
assert not (out/'plan.json').exists()
targets = json.loads(source.read_text())
assert len(targets) == len({t['tic'] for t in targets}) == 16
assert all(1 <= len(t['training_sectors']) <= 4 and len(t['heldout_sectors']) == 0 for t in targets)
save_json(out/'plan.json', {
    'utc': now(), 'targets': targets, 'source': str(source),
    'source_sha256': sha(source), 'script_sha256': sha(Path(__file__)),
    'source_hashes': {p.name: sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'settings': {**SETTINGS, 'bin_minutes': 10, 'max_training_baseline_days': 120},
    'policy': 'All 16 of the frozen metadata selection in existing radius/noise order. Search single faint midradius pilot only, with unchanged pipeline and gates. Keep all top-three peaks and failures. No reserved sectors available; no independent-sector timing validation possible. Audit the complete selection and sensitivity; remaining frozen pool not searched in this pilot. No novelty or completeness claim.'})
(out/'targets').mkdir(exist_ok=True)
rows = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(process_target, t, Path('data'), out, load_qlp, 120) for t in targets]
    for future in as_completed(futures):
        r = future.result()
        rows.append({k: r.get(k) for k in ['tic', 'status', 'error', 'disposition']})
        save_json(out/'progress.json', {'utc': now(), 'n_done': len(rows), 'n_total': len(targets), 'rows': rows})
save_json(out/'results.json', rows)
