"""Reconcile terminal Sector 51 discovery and both follow-up policies."""
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
assert len(expected) == len(terminal) == 115
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
        assert row['tic'] in {307911852,368290359,258044364}
        folder=Path('results/qlp-faint-sector51-recovery-20261010')/str(row['tic'])
        rp=read(folder/'plan.json');rr=read(folder/'result.json');recovered=read(Path(rr['path']))
        assert sha(path)==rp['original_sha256']==rr['original_sha256']
        assert sha(Path(rp['failed_raw']))==rp['failed_raw_sha256']
        assert rp['counts']['usable_flux']==0
        assert recovered['target']==row['target'] and recovered['status']=='error' and '404' in recovered['error']
        assert rr['status']=='error' and recovered['finished_utc']
        assert all(not Path(f"data/qlp/{row['tic']}-s{x:04d}.fits").exists() for x in row['target']['heldout_sectors'])
        assert (folder/'ASSESSMENT.md').exists()
        terminal_recovery_artifacts={name:sha(folder/name) for name in ['plan.json','result.json','ASSESSMENT.md']}
        inventory.append({'recovery_tic':row['tic'],'artifacts':terminal_recovery_artifacts})
    else:
        assert row['status'] == 'screened'
    for ev in row.get('data', []):
        raw = Path(f"data/qlp/{row['tic']}-s{ev['sector']:04d}.fits")
        assert sha(raw) == ev['source']['sha256']
    inventory.append({'path': str(path), 'sha256': sha(path)})
    rows.append(row)

pilot = Path('results/qlp-faint-sector51-pilot-20261010')
pilot_plan = read(pilot/'plan.json')
assert len(read(pilot/'results.json')) == len(pilot_plan['targets']) == 100
assert not set(expected) & {t['tic'] for t in pilot_plan['targets']}
pilot_rows = [read(pilot/'targets'/f"{t['tic']}.json") for t in pilot_plan['targets']]
for target,row in zip(pilot_plan['targets'],pilot_rows):
    assert row['target']==target and row['finished_utc']
    if row['status']=='error':
        assert row['tic']==258035987
        folder=Path('results/qlp-faint-sector51-recovery-20261010/258035987')
        rp=read(folder/'plan.json'); rr=read(folder/'result.json'); result=read(Path(rr['path']))
        assert sha(pilot/'targets'/'258035987.json')==rp['original_sha256']==rr['original_sha256']
        assert sha(Path(rp['failed_raw']))==rp['failed_raw_sha256']
        assert result['target']==target and result['status']=='error' and '404' in result['error']
        assert result['finished_utc'] and rr['status']=='error'
        assert all(not Path(f'data/qlp/258035987-s{x:04d}.fits').exists() for x in target['heldout_sectors'])
        for name,digest in plan['pilot_recovery_hashes'].items():assert sha(folder/name)==digest
    else:
        assert row['status']=='screened'
    for ev in row.get('data',[]):
        raw=Path(f"data/qlp/{row['tic']}-s{ev['sector']:04d}.fits")
        assert sha(raw)==ev['source']['sha256']
assert sha(pilot/'audit.json')==plan['pilot_audit_sha256']
policies = {
    'original': Path('results/qlp-faint-sector51-followup-20261010'),
    'coverage_diagnostic': Path('results/qlp-faint-sector51-coverage-followup-20261010'),
}
eligible = {key: set() for key in policies}
base = {'crowding_or_missing_crowding', 'alternative_detrending_prefers_other_period'}
coverage = {'secondary_unmeasurable', 'fewer_than_3_supported_events'}
for row in rows + pilot_rows:
    for i, peak in enumerate(row.get('screened_peaks', [])):
        flags = set(peak['flags'])
        key = (row['tic'], i)
        if flags <= base:
            assert row['tic'] in expected, 'Unexpected original-policy pilot lead requires review'
            eligible['original'].add(key)
        elif flags <= base | coverage and flags & coverage and peak['diagnostics']['supported_events'] >= 2:
            eligible['coverage_diagnostic'].add(key)

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
        if policy == 'coverage_diagnostic':
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
    'followups': followups, 'terminal_hashes': terminal_hashes, 'inventory': inventory,
    'interpretation': 'Terminal inventories and artifact integrity reconciled. Assessments are required but their existence is not scientific validation. No automatic candidate promotion, completeness, novelty or host-attribution claim.'})
print('Reconciled', len(rows), 'expansion targets and', len(followups), 'follow-ups')
