"""Freeze a native QLP training ephemeris before reading reserved QLP sectors."""
import json
from pathlib import Path
import numpy as np
from .qlp_campaign import load_qlp
from .followup import refine_training,fixed_measure,prediction_spread
from .pipeline import save_json,sha,now


def follow_qlp(discovery,output,root=Path('data'),peak_index=0,max_sectors=2):
    row=json.loads(discovery.read_text());target=row['target']
    training=list(target['training_sectors']);held=list(target['heldout_sectors'][:max_sectors])
    if max_sectors<1 or not held or set(training)&set(held):
        raise ValueError('Nonempty disjoint training and held-out sectors required')
    if len(set(held))!=len(held):raise ValueError('Duplicate held-out sectors')
    seed=row['screened_peaks'][peak_index]['best']
    output.mkdir(parents=True,exist_ok=False)
    t,y,e,data=load_qlp(target,root,bin_minutes=0)
    best,ranges=refine_training(t,y,e,seed,seed_baseline=row['clean_baseline_days'])
    frozen={'utc':now(),'tic':target['tic'],'collection':'QLP','discovery_sha256':sha(discovery),
            'peak_index':peak_index,'seed':seed,'best':best,'timing_ranges':ranges,
            'training_sectors':training,'training_data':data,'heldout_sectors':held,
            'heldout_previously_cached':{str(s):(root/'qlp'/f'{target["tic"]}-s{s:04d}.fits').exists() for s in held},
            'training_measurement':fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']),
            'source_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},
            'policy':'Native-cadence QLP refinement, then unchanged primary follow-up thresholds. Record cache presence; previously opened data cannot be described as blind validation. Missing-error fallback only if explicitly enabled on discovery target; per-sector error models retained. No planet/source-attribution or novelty conclusion.'}
    save_json(output/'frozen.json',frozen)
    checks=[]
    for s in held:
        check={'sector':s,'started_utc':now(),'status':'error'}
        try:
            single=dict(target,training_sectors=[s]);tt,yy,ee,evidence=load_qlp(single,root,bin_minutes=0)
            check['data']=evidence
            measured=fixed_measure(tt,yy,ee,best['period'],best['transit_time'],best['duration'])
            spread=prediction_spread(tt,best,ranges)
            precise=spread<best['duration']/2 and not ranges['search_boundary_hit'] and frozen['training_measurement']['supported_events']>=3
            controls=[]
            for shift in np.arange(1,50)*best['period']/50:
                if min(shift,best['period']-shift)<2*best['duration']:continue
                c=fixed_measure(tt,yy,ee,best['period'],best['transit_time']+shift,best['duration'])['total']
                if c is not None:controls.append(c['snr'])
            total=measured['total'];expected=None if total is None else best['depth']/total['error']
            if not precise:conclusion='timing_prediction_inconclusive'
            elif total is None:conclusion='insufficient_coverage'
            elif total['snr']>=5 and measured['supported_events']>=2:conclusion='recovered_at_frozen_ephemeris_requires_further_vetting'
            elif expected>=5 and total['snr']<2:conclusion='not_recovered_despite_expected_sensitivity'
            else:conclusion='insufficient_evidence'
            check.update(status='measured',measurement=measured,timing_spread_days=spread,timing_precise=precise,
                         expected_formal_snr=expected,phase_control_snrs=controls,conclusion=conclusion,
                         phase_control_note='Dependent phase controls, not a survey false-alarm probability')
        except Exception as exc:check['error']=f'{type(exc).__name__}: {exc}'
        checks.append(check);save_json(output/'heldout.json',checks)
    return checks
