"""Save an immutable inventory of completed results during the live search."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha, save_json, now

out = Path(__file__).parent
plan = json.loads((out/'plan.json').read_text())
targets = {t['tic']: t for t in plan['targets']}
for name, digest in plan['source_hashes'].items():
    assert sha(Path('src/exoplanet')/name) == digest
assert sha(Path(plan['source'])) == plan['source_sha256']
rows = []
counts = Counter()
review = []
for path in sorted((out/'targets').glob('*.json')):
    try:
        row = json.loads(path.read_text())
    except json.JSONDecodeError:
        continue  # An in-flight write is not a completed result.
    tic = row['tic']
    assert row['target'] == targets[tic] and row['finished_utc']
    for evidence in row.get('data', []):
        raw = Path(f"data/qlp/{tic}-s{evidence['sector']:04d}.fits")
        assert sha(raw) == evidence['source']['sha256']
        assert raw.stat().st_size == evidence['source']['bytes']
    reserved_cached = [s for s in targets[tic]['heldout_sectors']
                       if Path(f'data/qlp/{tic}-s{s:04d}.fits').exists()]
    categories = []
    for i, peak in enumerate(row.get('screened_peaks', [])):
        flags = set(peak['flags'])
        base = {'crowding_or_missing_crowding', 'alternative_detrending_prefers_other_period'}
        coverage = {'secondary_unmeasurable', 'fewer_than_3_supported_events'}
        category = None
        if flags <= base:
            category = 'detrending_diagnostic' if 'alternative_detrending_prefers_other_period' in flags else 'original_screen'
        elif flags <= base | coverage and flags & coverage and peak['diagnostics']['supported_events'] >= 2:
            category = 'coverage_diagnostic'
        if category:
            item = {'tic': tic, 'screened_peak_index': i, 'category': category, 'flags': peak['flags']}
            categories.append(item); review.append(item)
    if not categories:
        assert not reserved_cached, f'Unexpected opened reserved data for TIC {tic}'
    counts[row.get('disposition', row['status'])] += 1
    rows.append({'tic': tic, 'path': str(path), 'sha256': sha(path),
                 'status': row['status'], 'disposition': row.get('disposition'),
                 'reserved_qlp_cached': reserved_cached})
assert len({r['tic'] for r in rows}) == len(rows)
dest = out/f'checkpoint-{len(rows):04d}.json'
assert not dest.exists()
save_json(dest, {'utc': now(), 'plan_sha256': sha(out/'plan.json'),
    'script_sha256': sha(Path(__file__)), 'n_completed': len(rows),
    'n_planned': len(targets), 'counts': dict(counts), 'review': review, 'inventory': rows,
    'interpretation': 'Completed-file snapshot only, not terminal process evidence. Raw file hashes and sizes checked; discovery inputs match frozen targets. Both follow-up policies inventoried independently. Reserved QLP cache absence checked for targets without eligible peaks. No completeness, novelty, host attribution or planet claim.'})
print(dest, dict(counts), 'eligible peaks', len(review))
