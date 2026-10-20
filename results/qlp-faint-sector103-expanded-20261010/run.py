"""Remaining 109 metadata-ranked Sector 103 targets; reserve other epochs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target, SETTINGS
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
source = Path('results/qlp-faint-sector103-selection-20261010/selected.json')
assert not (out/'plan.json').exists()
pilot = Path('results/qlp-faint-sector103-pilot-20261010/audit.json')
audit = json.loads(pilot.read_text())
assert audit['terminal_results_present'] and audit['n_completed_files'] == 100
pilot_followup = Path('results/qlp-faint-sector103-pilot-followup-20261010')
records = json.loads((pilot_followup/'terminal.json').read_text())['records']
assert {(r['tic'],r['peak_index']) for r in records} == {(144325909,0)}
assert all(r['status']=='complete' for r in records)
assert (pilot_followup/'144325909-peak0/ASSESSMENT.md').is_file()
assert json.loads(Path('results/qlp-faint-sector103-pilot-coverage-followup-20261010/terminal.json').read_text())['records'] == []
assert json.loads(Path('results/qlp-faint-sector103-injections-20261010/audit.json').read_text())['terminal']
verification=Path('results/qlp-faint-sector103-pilot-20261010/verification.json')
assert json.loads(verification.read_text())['n_distinct_usable_after_recovery']==100
targets = json.loads(source.read_text())[100:]
assert len(targets) == len({t['tic'] for t in targets}) == 109
assert all(t['training_sectors'] == [103] and len(t['heldout_sectors']) >= 2 for t in targets)
save_json(out/'plan.json', {
    'utc': now(), 'targets': targets, 'source': str(source),
    'source_sha256': sha(source), 'pilot_verification_sha256':sha(verification), 'pilot_audit_sha256': sha(pilot), 'pilot_followup_sha256':sha(pilot_followup/'terminal.json'), 'pilot_assessment_sha256':sha(pilot_followup/'144325909-peak0/ASSESSMENT.md'), 'injection_audit_sha256': sha(Path('results/qlp-faint-sector103-injections-20261010/audit.json')), 'script_sha256': sha(Path(__file__)),
    'source_hashes': {p.name: sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'settings': {**SETTINGS, 'bin_minutes': 10, 'max_training_baseline_days': 120},
    'policy': 'Remaining 109 of the frozen 209-star metadata selection in existing radius/noise order. Search Sector 103 only, with unchanged pipeline and gates. Keep all top-three peaks and failures. Reserved sectors remain unopened. Completed pilot lead144325909 has unresolved off-target contamination; in-grid controls recovered8/12periods, four passed non-crowding gates; all twelve control periods lie within their actual search ranges. These controls do not calibrate completeness. No novelty or completeness claim.'})
(out/'targets').mkdir(exist_ok=True)
rows = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(process_target, t, Path('data'), out, load_qlp, 120) for t in targets]
    for future in as_completed(futures):
        r = future.result()
        rows.append({k: r.get(k) for k in ['tic', 'status', 'error', 'disposition']})
        save_json(out/'progress.json', {'utc': now(), 'n_done': len(rows), 'n_total': len(targets), 'rows': rows})
save_json(out/'results.json', rows)
