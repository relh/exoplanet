"""Blind multi-sector discovery search with later sectors reserved for validation."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import importlib.metadata
import shutil
import subprocess
from pathlib import Path

import numpy as np
from astropy.timeseries import BoxLeastSquares
from .pipeline import fetch, read_curve, save_json, sha, now
from .search import flatten, diagnostics, triage
from .vetting import extended_vetting

DURATIONS = [.04, .06, .09, .13, .18]
SETTINGS = {'period_min_days': .5, 'period_max_days': 20, 'durations_days': DURATIONS,
    'frequency_factor': 2, 'windows_days': [1.5, 2.5], 'max_training_baseline_days': 100,
    'max_peaks_per_target': 3, 'minimum_screen_snr': 7,
    'vetting_version': 2, 'correlated_noise_snr_min': 7, 'event_consistency_p_min': .001,
    'holdout_policy': 'Do not open/download held-out sectors during discovery'}


def lightcurve_url(tic, sector):
    tid = f'{tic:016d}'
    path = '/'.join(tid[i:i+4] for i in range(0,16,4))
    return ('https://mast.stsci.edu/api/v0.1/Download/file/?uri=mast:HLSP/tess-spoc/'
        f's{sector:04d}/target/{path}/hlsp_tess-spoc_tess_phot_{tid}-s{sector:04d}_tess_v1_lc.fits')


def joint_scan(t, y, dy):
    if np.ptp(t) > SETTINGS['max_training_baseline_days']:
        raise ValueError('Training baseline exceeds configured dense-search limit')
    maximum = min(20, np.ptp(t) / 2.5)
    bls = BoxLeastSquares(t, y, dy)
    result = bls.autopower(DURATIONS, minimum_period=.5, maximum_period=maximum,
        frequency_factor=2, objective='likelihood')
    i = int(np.argmax(result.power))
    return bls, result, peak_at(result, i)


def peak_at(result, i):
    return {k: float(result[k][i]) for k in
        ('period','duration','transit_time','depth','depth_err','depth_snr','power')}


def distinct_peaks(result, limit=3):
    """Keep separated peaks; retain harmonics for later explicit vetting."""
    peaks = []
    for i in np.argsort(result.power)[::-1]:
        p = float(result.period[i])
        if all(abs(p / b['period'] - 1) > .02 for b in peaks):
            peaks.append(peak_at(result, i))
        if len(peaks) == limit:
            break
    return peaks


def load_training(target, root, window=1.5):
    curves, evidence = [], []
    for sector in target['training_sectors']:
        path = root / 'lightcurves' / f's{sector:04d}-{target["tic"]}.fits'
        source = fetch(lightcurve_url(target['tic'], sector), path)
        t, f, e, star = read_curve(path)
        if int(star['ticid']) != target['tic'] or int(star['sector']) != sector:
            raise ValueError('FITS target/sector mismatch')
        if any(h['checksum'] != 'verified' for h in star['fits_integrity']):
            raise ValueError('Missing FITS checksum')
        clean = flatten(t, f, e, window=window)
        curves.append(clean)
        evidence.append({'sector':sector,'source':source,'star':star,
                         'n_raw_quality_points':len(t),'n_clean_points':len(clean[0])})
    t, y, dy = (np.concatenate([c[i] for c in curves]) for i in range(3))
    order = np.argsort(t)
    t, y, dy = t[order], y[order], dy[order]
    if np.any(np.diff(t) <= 0):
        raise ValueError('Overlapping or duplicate sector timestamps')
    return t, y, dy, evidence


def process_target(target, root, output):
    tic = target['tic']
    row = {'tic':tic,'target':target,'started_utc':now(),'status':'error'}
    try:
        t, y, dy, evidence = load_training(target, root)
        row['data'] = evidence
        row['clean_baseline_days'] = float(np.ptp(t))
        row['median_scatter_floor_ppm'] = float(np.median(dy) * 1e6)
        _, power, best = joint_scan(t, y, dy)
        row['n_trial_periods'] = len(power.period)
        row['peaks'] = distinct_peaks(power)
        row['best'] = best
        promising = [b for b in row['peaks'] if b['depth_snr'] >= 7]
        row['screened_peaks'] = []
        if promising:
            t2, y2, dy2, _ = load_training(target, root, window=2.5)
            alternative = joint_scan(t2, y2, dy2)[2]
            # Inverted/sinusoid diagnostics are the same for all peaks; compute
            # once then use the same null maximum for each peak's comparison.
            shared = None
            for b in promising:
                diag = diagnostics(t, y, dy, b, searcher=joint_scan, shared=shared)
                shared = {'inverted':diag['inverted'],'sinusoid':diag['sinusoid']}
                flags = triage(b, diag)
                extended = extended_vetting(t,y,dy,b,diag)
                flags += extended['flags']
                if abs(alternative['period'] / b['period'] - 1) > .02:
                    flags.append('alternative_detrending_prefers_other_period')
                if any(d['star']['crowdsap'] is None or d['star']['crowdsap'] < .8 for d in evidence):
                    flags.append('crowding_or_missing_crowding')
                radius = float(np.sqrt(b['depth']) * target['star']['rad'] * 109.076)
                row['screened_peaks'].append({'best':b,'diagnostics':diag,'flags':flags,
                    'radius_earth_if_on_target':radius,'alternative_window_best':alternative,
                    'extended_vetting':extended})
        row['status'] = 'screened'
        row['disposition'] = ('followup_priority' if any(not p['flags'] for p in row['screened_peaks'])
                              else 'flagged' if promising else 'below_screen_threshold')
    except Exception as exc:
        row['error'] = f'{type(exc).__name__}: {exc}'
    row['finished_utc'] = now()
    save_json(output / 'targets' / f'{tic}.json',row)
    print(f'TIC {tic}: {row.get("disposition", "error")} '
          f'SNR={row.get("best", {}).get("depth_snr", 0):.2f} {row.get("error", "")}',flush=True)
    return row


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--data',type=Path,default=Path('data'))
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--limit',type=int,default=300)
    parser.add_argument('--offset',type=int,default=0)
    args=parser.parse_args()
    if not 1 <= args.workers <= 8 or not 1 <= args.limit <= 1000 or args.offset<0:
        parser.error('workers must be 1..8; limit 1..1000')
    targets=json.loads(args.selection.read_text())[args.offset:args.offset+args.limit]
    if not targets: parser.error('Selection is empty')
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'targets').mkdir()
    (args.output/'source').mkdir()
    for source in Path(__file__).parent.glob('*.py'):
        shutil.copyfile(source,args.output/'source'/source.name)
    for name in ['uv.lock','pyproject.toml']:
        shutil.copyfile(name,args.output/'source'/name)
    run={'started_utc':now(),'settings':SETTINGS,'selection_sha256':sha(args.selection),
        'selection_path':str(args.selection),'selection_offset':args.offset,
        'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'target_tics':[t['tic'] for t in targets],
        'source_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},
        'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','astropy']},
        'status':'running','n_selected':len(targets)}
    save_json(args.output/'run.json',run)
    results=[]
    with ThreadPoolExecutor(args.workers) as pool:
        futures=[pool.submit(process_target,t,args.data,args.output) for t in targets]
        for future in as_completed(futures):
            results.append(future.result())
            save_json(args.output/'progress.json',{'updated_utc':now(),'completed':len(results),
                'total':len(targets),'errors':sum(r['status']=='error' for r in results)})
    run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in results),
        n_followup=sum(r.get('disposition')=='followup_priority' for r in results))
    save_json(args.output/'run.json',run)
    ranking=sorted([r for r in results if r['status']=='screened'],key=lambda r:r['best']['depth_snr'],reverse=True)
    save_json(args.output/'ranking.json',[{'tic':r['tic'],'best':r['best'],'disposition':r['disposition'],
        'flags':[p['flags'] for p in r['screened_peaks']]} for r in ranking])
    print(json.dumps(run),flush=True)

if __name__=='__main__':
    main()
