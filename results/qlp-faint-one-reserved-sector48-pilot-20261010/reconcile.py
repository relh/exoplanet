"""Reconcile terminal Sector 48 one-reserved tier discovery and both follow-up policies."""
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
assert len(expected) == len(terminal) == len(read(Path(plan['source'])))
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
        assert row['tic'] in {82285714,99762185,9001789,138756809,407590044,165223479}
        recovery = Path('results/qlp-faint-one-reserved-sector48-recovery-20261010')/str(row['tic'])
        rp = read(recovery/'plan.json'); rr = read(recovery/'result.json')
        assert rp['original_sha256'] == sha(path) == rr['original_sha256']
        assert rp['counts']['usable_flux'] == 0
        assert sha(Path(rp['failed_raw'])) == rp['failed_raw_sha256']
        recovered = read(Path(rr['path']))
        assert rr['status'] == recovered['status'] == 'error' and '404' in recovered['error']
        assert recovered['target'] == row['target'] and recovered['finished_utc']
        assert row['target']['heldout_sectors'] == {82285714:[22],99762185:[21],9001789:[22],138756809:[22],407590044:[21],165223479:[21]}[row['tic']]
        for sector in row['target']['heldout_sectors']:
            assert not Path(f"data/qlp/{row['tic']}-s{sector:04d}.fits").exists()
        recoveries.append({'tic': row['tic'], 'status': 'error',
                          'artifacts': {str(q): sha(q) for q in [recovery/'plan.json', recovery/'result.json', Path(rr['path'])]}})
    else:
        assert row['status'] == 'screened'
    for ev in row.get('data', []):
        raw = Path(f"data/qlp/{row['tic']}-s{ev['sector']:04d}.fits")
        assert sha(raw) == ev['source']['sha256']
    inventory.append({'path': str(path), 'sha256': sha(path)})
    rows.append(row)

policies = {
    'original': Path('results/qlp-faint-one-reserved-sector48-pilot-followup-20261010'),
    'coverage_diagnostic': Path('results/qlp-faint-one-reserved-sector48-pilot-coverage-followup-20261010'),
}
eligible = {key: set() for key in policies}
base = {'crowding_or_missing_crowding', 'alternative_detrending_prefers_other_period'}
coverage = {'secondary_unmeasurable', 'fewer_than_3_supported_events'}
for row in rows:
    for i, peak in enumerate(row.get('screened_peaks', [])):
        flags = set(peak['flags'])
        key = (row['tic'], i)
        if flags <= base:
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
    'n_completed': len(rows),
    'counts': dict(Counter(r.get('disposition') or r['status'] for r in rows)),
    'recoveries': recoveries,
    'n_distinct_usable_after_recovery': sum(r['status']=='screened' for r in rows)+sum(r['status']=='screened' for r in recoveries),
    'followups': followups, 'terminal_hashes': terminal_hashes, 'inventory': inventory,
    'interpretation': 'Terminal inventories and artifact integrity reconciled. Assessments are required but their existence is not scientific validation. No automatic candidate promotion, completeness, novelty or host-attribution claim.'})
print('Reconciled', len(rows), 'selected targets and', len(followups), 'follow-ups')
