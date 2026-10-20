"""Check all completed scenario files without executing TRICERATOPS."""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
from scipy.special import logsumexp

R = Path('results/triceratops-20261013')
OUT = Path('results/triceratops-review-20261013')
checks = []
summaries = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


base_families = {'TP', 'EB', 'EBx2P', 'PTP', 'PEB', 'PEBx2P', 'STP',
                 'SEB', 'SEBx2P', 'DTP', 'DEB', 'DEBx2P', 'BTP', 'BEB', 'BEBx2P'}
planet_families = {'TP', 'PTP', 'DTP', 'STP', 'BTP', 'NTP'}
summary = json.loads((R / 'summary.json').read_text())
adopted = summary['adopted_run_files']
all_records = sorted(p.name for p in R.glob('*-N*-seed*-noise*-*.json'))
check('terminal summary', summary['status'] == 'complete')
check('bounded 17 completed records', len(all_records) == 17 == summary['completed_runs'])
expected_identities = {(tic, n, seed, noise, control) for tic in [80387959, 402358350]
            for n, seed, noise, control in [(100000, 13, 1, 'none'), (100000, 29, 1, 'none'),
                (100000, 47, 1, 'none'), (1000000, 13, 1, 'none'),
                (100000, 13, 1.5, 'none'), (100000, 13, 2, 'none'),
                (100000, 13, 1, 'flat'), (100000, 13, 1, 'inverted')]}
expected_identities.add((137151335, 100000, 13, 1, 'none'))
identities = set()
for record in all_records:
    check(record + ': adopted current catalog only', '/' not in record and '\\' not in record)
    file = R / record.replace('.json', '-scenarios.csv')
    name = file.name.removesuffix('-scenarios.csv')
    status = json.loads((R / (name + '.json')).read_text())
    check(name + ': file identity', name.startswith(str(status['tic']) + '-'))
    identities.add(tuple(status[k] for k in ['tic', 'draws', 'seed', 'noise', 'control']))
    required_hashes = {str(R / f'{status["tic"]}-{suffix}') for suffix in ['stars.csv', 'input.npz', 'input.json']}
    required_hashes.add(str(R / ('control-plan.json' if status['tic'] == 137151335 else 'plan.json')))
    check(name + ': recorded core input hashes', required_hashes <= set(status.get('input_hashes', {})))
    for input_path, digest in status['input_hashes'].items():
        check(name + ': input hash ' + input_path, hashlib.sha256(Path(input_path).read_bytes()).hexdigest() == digest)
    with file.open() as stream:
        rows = list(csv.DictReader(stream))
    with (R / f'{status["tic"]}-stars.csv').open() as stream:
        stars = list(csv.DictReader(stream))
    eligible_ids = {int(row['ID']) for row in stars if float(row['tdepth']) > 0}
    check(name + ': completed nondegenerate', status['status'] == 'completed' and not status['degenerate'])
    check(name + ': expected scenario count', len(rows) == 15 + 3*(len(eligible_ids)-1) == status['scenario_count'])
    check(name + ': complete target families', {row['scenario'] for row in rows[:15]} == base_families)
    check(name + ': every eligible host included', {int(row['ID']) for row in rows} == eligible_ids)
    for host in eligible_ids - {status['tic']}:
        check(name + f': complete nearby families {host}',
              {row['scenario'] for row in rows if int(row['ID']) == host} == {'NTP', 'NEB', 'NEBx2P'})
    logz = np.array([float(row['lnZ']) for row in rows])
    prob = np.array([float(row['prob']) for row in rows])
    check(name + ': no invalid evidence', not np.any(np.isnan(logz) | np.isposinf(logz)))
    check(name + ': finite evidence count', int(np.isfinite(logz).sum()) == status['finite_evidences'])
    expected_probabilities = np.exp(logz - logsumexp(logz))
    check(name + ': normalized evidence weights', np.allclose(prob, expected_probabilities, atol=2e-13, rtol=1e-11))
    check(name + ': total probability', abs(prob.sum()-1) < 2e-13)
    target_planet = sum(float(row['prob']) for row in rows if row['scenario'] in {'TP','PTP','DTP'})
    any_planet = sum(float(row['prob']) for row in rows if row['scenario'] in planet_families)
    nearby = sum(float(row['prob']) for row in rows if row['scenario'] in {'NTP','NEB','NEBx2P'})
    for key, value in [('target_planet', target_planet), ('FPP', 1-target_planet),
                       ('NFPP', nearby), ('any_host_planet', any_planet)]:
        check(name + ': ' + key, abs(value-status[key]) < 2e-13)
    background = json.loads((R / f'{status["tic"]}-background.json').read_text())
    check(name + ': background hash', hashlib.sha256(Path(background['path']).read_bytes()).hexdigest() == background['sha256'])
    summaries.append({**{k:status[k] for k in ['tic','draws','seed','noise','control','target_planet','FPP','NFPP','any_host_planet','elapsed_seconds','warnings']},
                      'path':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})

check('bounded run identities', identities == expected_identities)
nominal = {p for p in all_records if (d := json.loads((R/p).read_text()))['tic'] != 137151335
           and d['noise'] == 1 and d['control'] == 'none'}
check('adopted nominal mapping', set(adopted) == nominal and len(adopted) == 8)
for target in summary['targets']:
    rows = [d for d in summaries if d['tic'] == target['tic'] and d['noise'] == 1 and d['control'] == 'none']
    low = [d for d in rows if d['draws'] == 100000]
    high = [d for d in rows if d['draws'] == 1000000]
    check(str(target['tic']) + ': seeds', sorted(d['seed'] for d in low) == [13,29,47] and [d['seed'] for d in high] == [13])
    for metric in ['target_planet', 'FPP', 'NFPP', 'any_host_planet']:
        vals = [d[metric] for d in low]
        actual = target['metrics'][metric]
        for key, expected_value in [('range_100k', [min(vals), max(vals)]), ('median_100k', np.median(vals)),
                                    ('value_1m', high[0][metric]), ('delta_1m_from_100k_median', high[0][metric]-np.median(vals))]:
            check(f'{target["tic"]}: summary {metric} {key}', np.allclose(actual[key], expected_value, rtol=0, atol=2e-13))
    threshold = target['threshold_comparison']
    check(str(target['tic']) + ': threshold arithmetic',
          threshold['FPP_below_0_015'] == (high[0]['FPP'] < .015)
          and threshold['NFPP_below_0_001'] == (high[0]['NFPP'] < .001)
          and threshold['original_numerical_validation_thresholds_met'] == (high[0]['FPP'] < .015 and high[0]['NFPP'] < .001))
    check(str(target['tic']) + ': no convergence claim', target['status'] == 'exploratory_not_converged')
for original in sorted((R / 'provenance-replay').glob('*-N*-seed*-noise*-*.json')):
    previous = json.loads(original.read_text())
    replayed = json.loads((R / original.name).read_text())
    for metric in ['target_planet', 'FPP', 'NFPP', 'any_host_planet']:
        check(original.name + ': deterministic replay ' + metric, previous[metric] == replayed[metric])
    table_name = original.name.replace('.json', '-scenarios.csv')
    check(original.name + ': deterministic scenario table replay',
          (original.parent / table_name).read_bytes() == (R / table_name).read_bytes())
groups = []
for tic in [80387959, 402358350]:
    for draws in sorted({s['draws'] for s in summaries if s['tic'] == tic}):
        group = [s for s in summaries if s['tic']==tic and s['draws']==draws and s['noise']==1 and s['control']=='none']
        if not group:
            continue
        values = np.array([s['target_planet'] for s in group])
        groups.append(dict(tic=tic, draws=draws, completed_seeds=[s['seed'] for s in group],
                           target_planet_mean=values.mean(), target_planet_min=values.min(),
                           target_planet_max=values.max(),
                           target_planet_sample_std=values.std(ddof=1) if len(values)>1 else None))
output = dict(passed=len(checks), completed_runs=len(summaries), summaries=summaries,
              repeated_seed_groups=groups,
              limitation='Normalization and scenario accounting checks do not establish Monte Carlo convergence or astrophysical model validity.')
(OUT / 'output-verification.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(dict(passed=len(checks), completed_runs=len(summaries), repeated_seed_groups=groups), indent=2))
