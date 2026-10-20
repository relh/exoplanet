"""Reconcile terminal Sector 35 discovery and both follow-up policies."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json, sha, now

out = Path(__file__).parent
def read(p):
    return json.loads(p.read_text())

plan = read(out/'plan.json')
terminal = read(out/'results.json')
expected = {t['tic']: t for t in plan['targets']}
assert len(expected) == len(terminal) == 213
assert {r['tic'] for r in terminal} == set(expected)
assert len({r['tic'] for r in terminal}) == len(terminal)
assert sha(Path(plan['source'])) == plan['source_sha256']
for name,digest in plan['source_hashes'].items():
    assert sha(Path('src/exoplanet')/name)==digest
inventory = []
rows = []
recoveries = []
for summary in terminal:
    path = out/'targets'/f"{summary['tic']}.json"
    row = read(path)
    assert row['target'] == expected[row['tic']]
    assert row['finished_utc'] and row['started_utc'] >= plan['utc']
    assert all(summary.get(k) == row.get(k) for k in ['status', 'error', 'disposition'])
    if row['status'] == 'error':
        assert row['tic']==183408181
        recovery=Path('results/qlp-faint-sector35-recovery-20261010/183408181')
        rp=read(recovery/'plan.json');rr=read(recovery/'targets/183408181.json')
        assert rp['original_sha256']==sha(path) and sha(Path(rp['failed_raw']))==rp['failed_raw_sha256']
        assert rp['counts']['usable_flux']==0
        assert rr['target']==rp['target'] and rr['target']['training_sectors']==[34]
        assert rr['status']=='screened' and rr['disposition']=='below_screen_threshold'
        assert rr['started_utc']>=rp['utc'] and rr['finished_utc']
        for ev in rr['data']:assert sha(Path(f"data/qlp/183408181-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
        for sector in rr['target']['heldout_sectors']:assert not Path(f'data/qlp/183408181-s{sector:04d}.fits').exists()
        assert (recovery/'ASSESSMENT.md').is_file()
        recoveries.append({'tic':183408181,'status':'screened','disposition':rr['disposition'],'sector':34,'result_sha256':sha(recovery/'targets/183408181.json'),'assessment_sha256':sha(recovery/'ASSESSMENT.md')})
    else:
        assert row['status'] == 'screened'
    for ev in row.get('data', []):
        raw = Path(f"data/qlp/{row['tic']}-s{ev['sector']:04d}.fits")
        assert sha(raw) == ev['source']['sha256']
    inventory.append({'path': str(path), 'sha256': sha(path)})
    rows.append(row)

pilot = Path('results/qlp-faint-sector35-pilot-20261010')
pilot_plan = read(pilot/'plan.json')
assert len(read(pilot/'results.json')) == len(pilot_plan['targets']) == 100
assert not set(expected) & {t['tic'] for t in pilot_plan['targets']}
pilot_rows = [read(pilot/'targets'/f"{t['tic']}.json") for t in pilot_plan['targets']]
for target,row in zip(pilot_plan['targets'],pilot_rows):
    assert row['target']==target and row['finished_utc']
    assert row['status']==('error' if row['tic']==178826943 else 'screened')
    for ev in row.get('data', []):
        raw=Path(f"data/qlp/{row['tic']}-s{ev['sector']:04d}.fits")
        assert sha(raw)==ev['source']['sha256']
assert sha(pilot/'audit.json')==plan['pilot_audit_sha256']
assert sha(pilot/'reconciliation.json')==plan['pilot_reconciliation_sha256']
assert sha(Path('results/qlp-faint-sector35-pilot-20261010/ASSESSMENT.md'))==plan['pilot_assessment_sha256']
for path,digest in read(pilot/'reconciliation.json')['artifacts'].items():assert sha(Path(path))==digest
policies = {
    'pilot_original': Path('results/qlp-faint-sector35-pilot-followup-20261010'),
    'pilot_coverage_diagnostic': Path('results/qlp-faint-sector35-pilot-coverage-followup-20261010'),
    'original': Path('results/qlp-faint-sector35-followup-20261010'),
    'coverage_diagnostic': Path('results/qlp-faint-sector35-coverage-followup-20261010'),
}
eligible = {key: set() for key in policies}
base = {'crowding_or_missing_crowding', 'alternative_detrending_prefers_other_period'}
coverage = {'secondary_unmeasurable', 'fewer_than_3_supported_events'}
for row in rows + pilot_rows:
    for i, peak in enumerate(row.get('screened_peaks', [])):
        flags = set(peak['flags'])
        key = (row['tic'], i)
        if flags <= base:
            eligible['original' if row['tic'] in expected else 'pilot_original'].add(key)
        elif flags <= base | coverage and flags & coverage and peak['diagnostics']['supported_events'] >= 2:
            eligible['coverage_diagnostic' if row['tic'] in expected else 'pilot_coverage_diagnostic'].add(key)

# Expansion watcher excludes pilot; both reviewed inventories remain explicit.
followups = []
terminal_hashes = {str(out/'results.json'): sha(out/'results.json')}
for policy, folder in policies.items():
    result = read(folder/'terminal.json')
    assert result['status'] == 'complete'
    records = result['records']
    actual = {(r['tic'], r['peak_index']) for r in records}
    assert len(actual) == len(records) and actual == eligible[policy]
    terminal_hashes[str(folder/'terminal.json')] = sha(folder/'terminal.json')
    for rec in records:
        assert rec['status'] == 'complete' and rec['finished_utc']
        assert sha(Path(rec['discovery_path'])) == rec['discovery_sha256']
        if policy.endswith('coverage_diagnostic'):
            assert rec['diagnostic_only']
        dest = folder/f"{rec['tic']}-peak{rec['peak_index']}"
        artifacts = ['frozen.json', 'heldout.json', 'secondary.json', 'discovery.png', 'ASSESSMENT.md']
        for name in artifacts:
            assert (dest/name).is_file(), f'Missing follow-up review artifact: {dest/name}'
        frozen = read(dest/'frozen.json')
        assert frozen['discovery_sha256'] == rec['discovery_sha256']
        held = read(dest/'heldout.json')
        assert {h['sector'] for h in held} == set(frozen['heldout_sectors'])
        assert all(h['started_utc'] >= frozen['utc'] for h in held)
        followups.append({'policy': policy, 'tic': rec['tic'], 'peak_index': rec['peak_index'],
                          'diagnostic_only': rec['diagnostic_only'],
                          'artifacts': {name: sha(dest/name) for name in artifacts}})

save_json(out/'reconciliation.json', {'utc': now(), 'script_sha256': sha(Path(__file__)),
    'n_expansion_completed': len(rows), 'n_pilot_completed': len(pilot_rows),
    'counts': dict(Counter(r.get('disposition') or r['status'] for r in rows)),
    'recoveries': recoveries,
    'n_distinct_usable_after_recovery': sum(r['status']=='screened' for r in rows)+sum(r['status']=='screened' for r in recoveries),
    'n_distinct_reviewed_peaks':len({(f['tic'],f['peak_index']) for f in followups}), 'n_distinct_reviewed_stars':len({f['tic'] for f in followups}), 'followups': followups, 'terminal_hashes': terminal_hashes, 'inventory': inventory,
    'interpretation': 'Terminal inventories and artifact integrity reconciled. Assessments are required but their existence is not scientific validation. No automatic candidate promotion, completeness, novelty or host-attribution claim.'})
print('Reconciled', len(rows), 'expansion targets and', len(followups), 'follow-ups')
