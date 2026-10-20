"""Remaining 781 metadata-ranked Sector 28 targets; reserve other epochs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target, SETTINGS
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
source = Path('results/qlp-faint-sector28-selection-20261010/selected.json')
assert not (out/'plan.json').exists()
pilot = Path('results/qlp-faint-sector28-pilot-20261010/audit.json')
audit = json.loads(pilot.read_text())
assert audit['terminal_results_present'] and audit['n_completed_files'] == 100 and {r['tic'] for r in audit['review']} == {183494855}
assert [(r['tic'],r['status']) for r in json.loads(Path('results/qlp-faint-sector28-pilot-followup-20261010/terminal.json').read_text())['records']] == [(183494855,'complete')]
assert Path('results/qlp-faint-sector28-pilot-followup-20261010/183494855-peak0/ASSESSMENT.md').exists()
assert json.loads(Path('results/qlp-faint-sector28-pilot-coverage-followup-20261010/terminal.json').read_text())['records'] == []
assert json.loads(Path('results/qlp-faint-sector28-injections-20261010/audit.json').read_text())['terminal']
long_audit=Path('results/qlp-faint-sector28-long-injections-20261010/audit.json')
assert json.loads(long_audit.read_text())['terminal']
targets = json.loads(source.read_text())[100:]
assert len(targets) == len({t['tic'] for t in targets}) == 781
assert all(t['training_sectors'] == [28] and len(t['heldout_sectors']) >= 2 for t in targets)
save_json(out/'plan.json', {
    'utc': now(), 'targets': targets, 'source': str(source),
    'source_sha256': sha(source), 'pilot_followup_assessment_sha256':sha(Path('results/qlp-faint-sector28-pilot-followup-20261010/183494855-peak0/ASSESSMENT.md')), 'long_injection_audit_sha256':sha(long_audit), 'pilot_audit_sha256': sha(pilot), 'injection_audit_sha256': sha(Path('results/qlp-faint-sector28-injections-20261010/audit.json')), 'script_sha256': sha(Path(__file__)),
    'source_hashes': {p.name: sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'settings': {**SETTINGS, 'bin_minutes': 10, 'max_training_baseline_days': 120},
    'policy': 'Remaining781 frozen metadata-ranked targets after complete100pilot with one reviewed off-target lead and no product errors. Unchanged gates. Short controls6/12period and checked-phase recoveries,5noncrowdingpasses; only1/6one-Earth-radius controls recovered. Long10/12period and phase recoveries,5passes. All injected periods inside actual search bounds. Preserve failures; sparse controls do not establish completeness.'})
(out/'targets').mkdir(exist_ok=True)
rows = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(process_target, t, Path('data'), out, load_qlp, 120) for t in targets]
    for future in as_completed(futures):
        r = future.result()
        rows.append({k: r.get(k) for k in ['tic', 'status', 'error', 'disposition']})
        save_json(out/'progress.json', {'utc': now(), 'n_done': len(rows), 'n_total': len(targets), 'rows': rows})
save_json(out/'results.json', rows)
