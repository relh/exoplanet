"""Exploratory off-phase eclipse diagnostic; not a calibrated detection test.

Run as a companion after discovery. Search outside the primary eclipse and its
local background, and retain both dips and brightenings as selected controls.
"""
import numpy as np
from .search import depth_measure
from .followup import fixed_measure


def scan_secondary(t,y,dy,best):
    period=best['period'];epoch=best['transit_time'];primary=best['duration']
    durations=np.unique(np.minimum(np.array([.5,1,1.5])*primary,.1*period))
    # At least four phase samples across the shortest trial duration.
    n=int(np.ceil(4*period/durations.min()))
    if n>20000:raise ValueError('Secondary phase grid exceeds 20000-point bound')
    phase=(t-epoch)%period
    primary_distance=np.minimum(phase,period-phase)
    outside_primary=primary_distance>2*primary
    trials=[]
    for duration in durations:
        for fraction in np.arange(n)/n:
            # Keep the candidate center/background separate from the primary.
            if min(fraction,1-fraction)*period <= 2*primary+3*duration:continue
            distance=abs((phase-fraction*period+period/2)%period-period/2)
            m=depth_measure(y,dy,(distance<duration/2)&outside_primary,
                            (distance>duration)&(distance<3*duration)&outside_primary)
            if m is not None:trials.append({'phase':float(fraction),'duration':float(duration),**m})
    if not trials:return {'status':'insufficient_phase_coverage','n_trials':0}
    dip=max(trials,key=lambda v:v['snr']);bright=min(trials,key=lambda v:v['snr'])
    # Event support is evaluated only for the selected maximum, not all trials.
    measured=fixed_measure(t[outside_primary],y[outside_primary],dy[outside_primary],
        period,epoch+dip['phase']*period,dip['duration'])
    return {'status':'measured','n_trials':len(trials),'best_dip':dip,
            'best_brightening':bright,'selected_dip_events':measured,
            'depth_ratio_to_primary':dip['depth']/best['depth'],
            'interpretation':'Exploratory maximum over phase/duration; SNR is selected and uncalibrated. Primary and nearby phases excluded. A dip requires inspection and independent-sector/reduction checks; not an automatic binary or planet classification.'}
