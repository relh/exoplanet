"""Freeze a training ephemeris before opening later-sector photometry.

These tests rank follow-up work. They do not validate planets or establish novelty.
Timing ranges below assume the fitted box and white errors; they are not a full
physical posterior or a red-noise-calibrated confidence interval.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from astropy.timeseries import BoxLeastSquares
from .campaign import load_training, lightcurve_url, peak_at
from .pipeline import fetch, read_curve, save_json, now, sha
from .search import flatten, depth_measure


def fixed_measure(t, y, dy, period, epoch, duration):
    phase=(t-epoch+period/2)%period-period/2
    event=np.rint((t-epoch)/period).astype(int)
    inside=abs(phase)<duration/2
    outside=(abs(phase)>duration)&(abs(phase)<min(3*duration,period/2))
    total=depth_measure(y,dy,inside,outside)
    events=[]
    for n in np.unique(event[inside]):
        d=depth_measure(y,dy,inside&(event==n),outside&(event==n))
        if d is not None: events.append({'event':int(n),'center_btjd':float(epoch+n*period),**d})
    # Empirical scatter of event depths reveals variability hidden by formal errors.
    empirical_error=None
    if len(events)>1:
        empirical_error=float(np.std([d['depth'] for d in events],ddof=1)/len(events)**.5)
    return {'total':total,'events':events,'supported_events':sum(d['snr']>=2 for d in events),
        'event_scatter_error':empirical_error}


def refine_training(t,y,dy,seed):
    bls=BoxLeastSquares(t,y,dy)
    width=3*seed['duration']*seed['period']/np.ptp(t)
    periods=np.linspace(max(.25,seed['period']-width),seed['period']+width,2049)
    durations=np.array([.8,1,1.2])*seed['duration']
    result=bls.power(periods,durations,objective='likelihood',oversample=50)
    best=peak_at(result,int(np.argmax(result.power)))
    good=result.power>=best['power']-4.5
    selected=np.flatnonzero(good)
    ranges={'period_min':float(result.period[good].min()),'period_max':float(result.period[good].max()),
        'profile_timing_pairs':[[float(result.period[i]),float(result.transit_time[i])] for i in selected],
        'search_boundary_hit':bool(good[0] or good[-1]),
        'period_grid_spacing':float(periods[1]-periods[0]),
        'conditional_epoch_floor_days':float(max(best['duration']/50,
                best['duration']/max(best['depth_snr'],1))),
        'interpretation':'Delta log likelihood <=4.5 period profile; epoch floor heuristic; ignores red noise and model mismatch'}
    return best,ranges


def prediction_spread(t,best,ranges):
    p,epoch=best['period'],best['transit_time']
    epochs=np.rint((np.array([t.min(),t.max()])-epoch)/p)
    offsets=[]
    for p2,e2 in ranges['profile_timing_pairs']:
        # Align reference epochs to the same cycle before propagating.
        e2 += round((epoch-e2)/p2)*p2
        offsets.extend(abs((e2-epoch)+epochs*(p2-p)))
    return float(max(offsets,default=0)+3*ranges['conditional_epoch_floor_days'])


def follow_target(discovery,output,root=Path('data'),peak_index=0,max_sectors=3):
    row=json.loads(discovery.read_text())
    target=row['target']
    seed=row['screened_peaks'][peak_index]['best']
    output.mkdir(parents=True,exist_ok=False)
    t,y,dy,evidence=load_training(target,root)
    best,ranges=refine_training(t,y,dy,seed)
    # This immutable record is written BEFORE any held-out light curve is loaded.
    frozen={'frozen_utc':now(),'discovery_sha256':sha(discovery),'tic':target['tic'],
        'training_data':evidence,'seed':seed,'best':best,'timing_ranges':ranges,
        'training_measurement':fixed_measure(t,y,dy,best['period'],best['transit_time'],best['duration']),
        'heldout_sectors':target['heldout_sectors'][:max_sectors],
        'source_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')}}
    save_json(output/'frozen.json',frozen)
    checks=[]
    for sector in frozen['heldout_sectors']:
        check={'sector':sector,'started_utc':now(),'status':'error'}
        try:
            path=root/'lightcurves'/f's{sector:04d}-{target["tic"]}.fits'
            check['source']=fetch(lightcurve_url(target['tic'],sector),path)
            t2,f2,e2,meta=read_curve(path)
            if meta['ticid']!=target['tic'] or meta['sector']!=sector:
                raise ValueError('Held-out FITS identity mismatch')
            check['star']=meta
            t2,y2,dy2=flatten(t2,f2,e2)
            measured=fixed_measure(t2,y2,dy2,best['period'],best['transit_time'],best['duration'])
            spread=prediction_spread(t2,best,ranges)
            precise=(spread<best['duration']/2 and not ranges['search_boundary_hit']
                and frozen['training_measurement']['supported_events']>=3)
            phase_controls=[]
            for shift in np.arange(1,50)*best['period']/50:
                if min(shift,best['period']-shift)<2*best['duration']: continue
                control=fixed_measure(t2,y2,dy2,best['period'],best['transit_time']+shift,best['duration'])['total']
                if control is not None: phase_controls.append(control['snr'])
            total=measured['total']
            expected=None if total is None else best['depth']/total['error']
            check.update(status='measured',measurement=measured,timing_spread_days=spread,
                timing_precise=precise,expected_formal_snr=expected,
                phase_control_snrs=phase_controls,
                phase_control_note='Fixed-period phase offsets are dependent controls, not a survey false-alarm probability')
            if not precise: conclusion='timing_prediction_inconclusive'
            elif total is None: conclusion='insufficient_coverage'
            elif total['snr']>=5 and measured['supported_events']>=2:
                conclusion='recovered_at_frozen_ephemeris_requires_further_vetting'
            elif expected>=5 and total['snr']<2: conclusion='not_recovered_despite_expected_sensitivity'
            else: conclusion='insufficient_evidence'
            check['conclusion']=conclusion
        except Exception as exc:
            check['error']=f'{type(exc).__name__}: {exc}'
        checks.append(check)
        save_json(output/'heldout.json',checks)
    return checks


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--discovery',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--data',type=Path,default=Path('data'))
    p.add_argument('--peak-index',type=int,default=0)
    p.add_argument('--max-sectors',type=int,default=3)
    a=p.parse_args()
    if a.peak_index<0 or a.max_sectors<1:p.error('Nonnegative peak index and positive sector count required')
    checks=follow_target(a.discovery,a.output,a.data,a.peak_index,a.max_sectors)
    print(json.dumps([{'sector':r['sector'],'result':r.get('conclusion',r.get('error'))} for r in checks]))

if __name__=='__main__':
    main()
