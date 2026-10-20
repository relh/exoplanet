"""Retrospective, seed-conditional season omission; cached products only."""
import json
from pathlib import Path
import numpy as np
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure,prediction_spread
from exoplanet.pipeline import sha,now,save_json
O=Path(__file__).parent
SOURCE=Path('results/weak-seed-ranks8-32-20261011/targets/469309982.json')
SECTORS=[9,10,36,37,63,64]
def load(sectors,window):
    for s in sectors:
        p=Path(f'data/lightcurves/s{s:04d}-469309982.fits')
        assert p.exists() and p.with_suffix('.fits.json').exists(), 'Cached raw and metadata required; downloading forbidden'
    return load_training({'tic':469309982,'training_sectors':sectors},Path('data'),window=window)
def classify(measure,best,spread,ranges,train):
    total=measure['total'];precise=spread<best['duration']/2 and not ranges['search_boundary_hit'] and train['supported_events']>=3
    expected=None if total is None else best['depth']/total['error']
    if not precise: result='timing_prediction_inconclusive'
    elif total is None: result='insufficient_coverage'
    elif total['snr']>=5 and measure['supported_events']>=2:result='conditional_recovery_requires_further_vetting'
    elif expected>=5 and total['snr']<2:result='not_recovered_despite_expected_sensitivity'
    else:result='insufficient_evidence'
    return dict(conclusion=result,timing_precise=precise,expected_formal_snr=expected)
def main():
    assert not (O/'plan.json').exists(), 'No overwriting frozen run'
    x=json.loads(SOURCE.read_text());sel=x['selection'];groups=[[9,10],[36,37],[63,64]]
    raw={}
    for s in SECTORS:
        p=Path(f'data/lightcurves/s{s:04d}-469309982.fits');m=json.loads(p.with_suffix('.fits.json').read_text());assert sha(p)==m['sha256'];raw[str(p)]=m
    plan=dict(created_utc=now(),source_path=str(SOURCE),source_sha256=sha(SOURCE),seed=sel['seed'],seed_baseline=sel['original_baseline_days'],groups=groups,windows=[1.5,2.5],raw=raw,source_hashes={str(p):sha(p) for p in [Path(__file__),*Path('src/exoplanet').glob('*.py')]},policy='All six sectors previously opened. Retrospective conditional robustness, not independent holdouts. Original seed selected from9/10 informs local period window in every fold. Fit only other seasons; no excluded-flux timing optimization or profile maximum. Sector-local detrending uses each own sector. Two windows and all three folds reported. Formal errors/profile are not red-noise-calibrated; folds overlap and do not yield independent probabilities.')
    save_json(O/'plan.json',plan);rows=[]
    for window in plan['windows']:
        for excluded in groups:
            name=f'w{window}-omit{excluded[0]}';training=[s for s in SECTORS if s not in excluded];row=dict(name=name,window=window,excluded=excluded,training=training,status='error')
            try:
                t,y,e,evidence=load(training,window);best,ranges=refine_training(t,y,e,plan['seed'],seed_baseline=plan['seed_baseline']);train=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration'])
                frozen=dict(created_utc=now(),training=training,excluded=excluded,window=window,best=best,ranges=ranges,measurement=train,data=evidence,plan_sha256=sha(O/'plan.json'))
                save_json(O/f'{name}-training.json',frozen)
                tt,yy,ee,held_evidence=load(excluded,window);measured=fixed_measure(tt,yy,ee,best['period'],best['transit_time'],best['duration']);spread=prediction_spread(tt,best,ranges)
                seed=plan['seed'];reference=fixed_measure(tt,yy,ee,seed['period'],seed['transit_time'],seed['duration'])
                np.savez_compressed(O/f'{name}.npz',t=t,y=y,e=e,tt=tt,yy=yy,ee=ee)
                row.update(status='measured',scored_utc=now(),best=best,timing_spread_days=spread,measurement=measured,seed_reference=reference,excluded_data=held_evidence,training_sha256=sha(O/f'{name}-training.json'),**classify(measured,best,spread,ranges,train))
            except Exception as exc:row['error']=f'{type(exc).__name__}: {exc}'
            rows.append(row);save_json(O/'results.json',dict(plan_sha256=sha(O/'plan.json'),rows=rows))
            print(name,row.get('conclusion',row.get('error')),flush=True)
if __name__=='__main__':main()
