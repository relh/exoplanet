"""Remaining 213 metadata-ranked Sector 35 targets; reserve other epochs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target, SETTINGS
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
source = Path('results/qlp-faint-sector35-selection-20261010/selected.json')
assert not (out/'plan.json').exists()
pilot = Path('results/qlp-faint-sector35-pilot-20261010/audit.json')
audit = json.loads(pilot.read_text())
assert audit['terminal_results_present'] and audit['n_completed_files'] == 100 and not audit['review']
assert json.loads(Path('results/qlp-faint-sector35-pilot-followup-20261010/terminal.json').read_text())['records'] == []
records=json.loads(Path('results/qlp-faint-sector35-pilot-coverage-followup-20261010/terminal.json').read_text())['records']
assert [(r['tic'],r['peak_index'],r['status']) for r in records]==[(141301608,0,'complete')]
reconciled=Path('results/qlp-faint-sector35-pilot-20261010/reconciliation.json');r=json.loads(reconciled.read_text())
assert r['n_usable']==99 and r['n_incomplete']==1 and r['n_reviewed_peaks']==1
for path,digest in r['artifacts'].items():assert sha(Path(path))==digest
assert json.loads(Path('results/qlp-faint-sector35-injections-20261010/audit.json').read_text())['terminal']
long_audit=Path('results/qlp-faint-sector35-long-injections-20261010/audit.json')
assert json.loads(long_audit.read_text())['terminal']
targets = json.loads(source.read_text())[100:]
assert len(targets) == len({t['tic'] for t in targets}) == 213
assert all(t['training_sectors'] == [35] and len(t['heldout_sectors']) >= 2 for t in targets)
save_json(out/'plan.json', {
    'utc': now(), 'targets': targets, 'source': str(source),
    'source_sha256': sha(source), 'long_injection_audit_sha256':sha(long_audit), 'pilot_audit_sha256': sha(pilot), 'injection_audit_sha256': sha(Path('results/qlp-faint-sector35-injections-20261010/audit.json')), 'script_sha256': sha(Path(__file__)),
    'source_hashes': {p.name: sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'pilot_reconciliation_sha256':sha(reconciled), 'pilot_assessment_sha256':sha(Path('results/qlp-faint-sector35-pilot-20261010/ASSESSMENT.md')),
    'settings': {**SETTINGS, 'bin_minutes': 10, 'max_training_baseline_days': 120},
    'policy': 'Remaining213 frozen targets after reviewed100pilot:99usable,one unrecoverable error,one unresolved coverage-only lead retained in final inventory. Unchanged gates. Short8period+phase4passes; long11period+phase5passes. All in-grid, but no Earth-radius or8.37day screening passes. No completeness claim.'})
(out/'targets').mkdir(exist_ok=True)
rows = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(process_target, t, Path('data'), out, load_qlp, 120) for t in targets]
    for future in as_completed(futures):
        r = future.result()
        rows.append({k: r.get(k) for k in ['tic', 'status', 'error', 'disposition']})
        save_json(out/'progress.json', {'utc': now(), 'n_done': len(rows), 'n_total': len(targets), 'rows': rows})
save_json(out/'results.json', rows)
