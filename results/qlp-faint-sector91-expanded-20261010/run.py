"""Remaining 266 metadata-ranked Sector 91 targets; reserve other epochs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target, SETTINGS
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
source = Path('results/qlp-faint-sector91-selection-20261010/selected.json')
assert not (out/'plan.json').exists()
pilot = Path('results/qlp-faint-sector91-pilot-20261010/audit.json')
audit = json.loads(pilot.read_text())
assert audit['terminal_results_present'] and audit['n_completed_files']==100
pilot_followup=Path('results/qlp-faint-sector91-pilot-coverage-followup-20261010')
records=json.loads((pilot_followup/'terminal.json').read_text())['records']
assert [(x['tic'],x['peak_index'],x['status']) for x in records]==[(386739254,0,'complete'),(386739254,1,'complete')]
review=Path('results/qlp-faint-sector91-pilot-20261010/ASSESSMENT.md')
reconciled=Path('results/qlp-faint-sector91-pilot-20261010/reconciliation.json')
r=json.loads(reconciled.read_text());assert r['n_reviewed_leads']==2
for folder,artifacts in r['followup_artifacts'].items():
 for name,digest in artifacts.items():assert sha(Path(folder)/name)==digest
assert json.loads(Path('results/qlp-faint-sector91-pilot-followup-20261010/terminal.json').read_text())['records']==[]
assert json.loads(Path('results/qlp-faint-sector91-injections-20261010/audit.json').read_text())['terminal']
long_audit=Path('results/qlp-faint-sector91-long-injections-20261010/audit.json')
assert json.loads(long_audit.read_text())['terminal']
targets = json.loads(source.read_text())[100:]
assert len(targets) == len({t['tic'] for t in targets}) == 266
assert all(t['training_sectors'] == [91] and len(t['heldout_sectors']) >= 2 for t in targets)
save_json(out/'plan.json', {
    'utc': now(), 'targets': targets, 'source': str(source),
    'source_sha256': sha(source), 'long_injection_audit_sha256':sha(long_audit), 'pilot_audit_sha256': sha(pilot), 'injection_audit_sha256': sha(Path('results/qlp-faint-sector91-injections-20261010/audit.json')), 'script_sha256': sha(Path(__file__)),
    'source_hashes': {p.name: sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'pilot_review_sha256':sha(review), 'pilot_reconciliation_sha256':sha(reconciled),
    'settings': {**SETTINGS, 'bin_minutes': 10, 'max_training_baseline_days': 120},
    'policy': 'Remaining266 frozen targets after complete100pilot with two reviewed unresolved peaks on one star, retained in final inventory. Unchanged gates. Short8period+phase recoveries and5passes; long9period+phase and2passes. All injections in-grid, sparse uneven sensitivity retained; no completeness claim.'})
(out/'targets').mkdir(exist_ok=True)
rows = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(process_target, t, Path('data'), out, load_qlp, 120) for t in targets]
    for future in as_completed(futures):
        r = future.result()
        rows.append({k: r.get(k) for k in ['tic', 'status', 'error', 'disposition']})
        save_json(out/'progress.json', {'utc': now(), 'n_done': len(rows), 'n_total': len(targets), 'rows': rows})
save_json(out/'results.json', rows)
