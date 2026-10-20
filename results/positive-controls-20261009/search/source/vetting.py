"""Additional heuristic diagnostics for correlated noise and inconsistent events.

These metrics are screening diagnostics, not calibrated false-alarm probabilities.
"""
import numpy as np
from scipy.stats import chi2


def correlated_noise(t, y, dy, best):
    """Compare duration-binned out-of-transit scatter with formal bin errors.

    Split across gaps; reject bins with <50% expected coverage. Use robust MAD
    to limit flare sensitivity. White-noise-normalized beta has a floor of one.
    """
    period, epoch, duration = best['period'], best['transit_time'], best['duration']
    outside = abs((t-epoch+period/2)%period-period/2) > duration
    means, variances = [], []
    segments = np.split(np.arange(len(t)), np.flatnonzero(np.diff(t)>.3)+1)
    for idx in segments:
        if len(idx)<10: continue
        cadence = np.median(np.diff(t[idx]))
        bins = np.floor((t[idx]-t[idx[0]])/duration).astype(int)
        for b in np.unique(bins):
            use = idx[(bins==b)&outside[idx]]
            if len(use)<max(3, .5*duration/cadence): continue
            w = 1/dy[use]**2
            means.append(float(np.average(y[use], weights=w)))
            variances.append(float(1/w.sum()))
    if len(means)<15:
        return {'status':'insufficient_bins','n_bins':len(means),'beta':None,'adjusted_snr':None}
    means=np.asarray(means)
    scatter=1.4826*np.median(abs(means-np.median(means)))
    expected=np.sqrt(np.median(variances))
    beta=float(max(1,scatter/expected))
    return {'status':'measured','n_bins':len(means),'bin_duration_days':duration,
        'binned_scatter_ppm':float(scatter*1e6),'expected_white_scatter_ppm':float(expected*1e6),
        'beta':beta,'adjusted_snr':float(best['depth_snr']/beta),
        'interpretation':'Duration-binned robust scatter ratio; conditional heuristic, not calibrated significance'}


def event_consistency(events, beta=1):
    if len(events)<2:
        return {'status':'insufficient_events','n_events':len(events)}
    depths=np.array([e['depth'] for e in events]);errors=np.array([e['error'] for e in events])*beta
    mean=np.average(depths,weights=1/errors**2)
    statistic=float(np.sum(((depths-mean)/errors)**2))
    contributions=np.maximum(depths/errors,0)**2
    return {'status':'measured','n_events':len(events),'weighted_depth':float(mean),
        'chi2':statistic,'dof':len(events)-1,'conditional_chi2_sf':float(chi2.sf(statistic,len(events)-1)),
        'max_positive_event_snr2_fraction':float(contributions.max()/contributions.sum()) if contributions.sum()>0 else None,
        'error_inflation_beta':beta,
        'interpretation':'Independent Gaussian event errors inflated by binned beta; not a planet probability'}


def extended_vetting(t,y,dy,best,diag):
    noise=correlated_noise(t,y,dy,best)
    consistency=event_consistency(diag['events'],noise['beta'] or 1)
    edges=np.r_[t[0],t[-1],t[:-1][np.diff(t)>.3],t[1:][np.diff(t)>.3]]
    supported=[e for e in diag['events'] if e['snr']>=2]
    distances=[float(np.min(abs(edges-e['time']))) for e in supported]
    flags=[]
    if noise['status']!='measured':flags.append('correlated_noise_unmeasurable')
    elif noise['adjusted_snr']<7:flags.append('low_correlated_noise_adjusted_snr')
    if consistency['status']=='measured':
        if consistency['conditional_chi2_sf']<.001:flags.append('inconsistent_event_depths')
        fraction=consistency['max_positive_event_snr2_fraction']
        if fraction is not None and fraction>.75:flags.append('single_event_dominates')
    else:flags.append('event_consistency_unmeasurable')
    if distances and np.mean(np.array(distances)<max(.15,best['duration']))>.5:
        flags.append('events_near_clean_segment_edges')
    return {'noise':noise,'event_consistency':consistency,
        'supported_event_edge_distances_days':distances,'flags':flags}
