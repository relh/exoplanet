"""Exposure-averaged box fitting with local linear event baselines.

This is a diagnostic transit approximation, not a limb-darkened physical fit.
All uncertainty measures are conditional on the ephemeris and supplied errors.
"""
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2


def integrated_box(t, period, epoch, duration, exposure):
    exposure=np.asarray(exposure)
    if duration<=0 or np.any(exposure<=0) or np.any(duration+exposure>=period):
        raise ValueError('Invalid transit/exposure geometry')
    phase=(t-epoch+period/2)%period-period/2
    left=np.maximum(phase-exposure/2,-duration/2)
    right=np.minimum(phase+exposure/2,duration/2)
    return np.clip((right-left)/exposure,0,1)


def exposure_times(t):
    exposure=np.empty(len(t))
    for idx in np.split(np.arange(len(t)),np.flatnonzero(np.diff(t)>.3)+1):
        if len(idx)<2:raise ValueError('Cannot infer exposure from isolated cadence')
        exposure[idx]=np.median(np.diff(t[idx]))
    return exposure


def fit_events(t,y,dy,seed,beta=1):
    """Refine one discovery peak, profiling out a slope/intercept per event.

    Fixed windows are selected from the seed; optimization never adds/removes
    points as the trial model moves. Both odd and even events share the same
    timing/shape fit; amplitudes are subsequently measured separately.
    """
    t,y,dy=map(np.asarray,(t,y,dy))
    p0=seed['period'];d0=seed['duration'];baseline=np.ptp(t)
    e0=seed['transit_time']+round((np.median(t)-seed['transit_time'])/p0)*p0
    event=np.rint((t-e0)/p0).astype(int);dt=t-(e0+event*p0)
    halfwindow=min(4*d0,.45*p0)
    take=abs(dt)<halfwindow
    # Ignore tiny windows truncated by gaps; they cannot constrain a baseline.
    labels0,counts=np.unique(event[take],return_counts=True)
    retained=labels0[counts>=8]
    take &= np.isin(event,retained)
    exposure=exposure_times(t)[take]
    tt,yy,ee,events=t[take],y[take],dy[take],event[take]
    labels,inverse=np.unique(events,return_inverse=True)
    if len(labels)<3:raise ValueError('Fewer than three event windows')
    w=1/ee**2;sw=np.bincount(inverse,weights=w)
    local_t=tt-np.bincount(inverse,weights=w*tt)[inverse]/sw[inverse]
    st2=np.bincount(inverse,weights=w*local_t**2)
    if np.any(st2<=0):raise ValueError('Degenerate local event window')
    def project(z):
        mean=np.bincount(inverse,weights=w*z)/sw
        slope=np.bincount(inverse,weights=w*local_t*z)/st2
        return z-mean[inverse]-slope[inverse]*local_t
    py=project(yy)
    cycles=max(baseline/p0,1)
    def evaluate(parameters):
        offset,drift,duration=parameters
        period=p0+drift/cycles;epoch=e0+offset
        shape=integrated_box(tt,period,epoch,duration,exposure)
        pq=project(shape);information=np.sum(w*pq**2)
        if information<=0:return np.zeros(len(tt)),0,shape,pq
        depth=-np.sum(w*py*pq)/information
        return (py+depth*pq)/ee,depth,shape,pq
    bounds=([-d0,-2*d0,max(.005,.4*d0)],[d0,2*d0,min(1.8*d0,.3*p0)])
    initial=[0,0,d0]
    fit=least_squares(lambda x:evaluate(x)[0],initial,bounds=bounds,
        x_scale=[d0,d0,d0],diff_step=1e-4,max_nfev=200)
    residual,depth,shape,pq=evaluate(fit.x)
    information=np.sum(w*pq**2);error=beta/np.sqrt(information)
    event_information=np.bincount(inverse,weights=w*pq**2)
    event_depth=np.divide(-np.bincount(inverse,weights=w*py*pq),event_information,
        out=np.zeros(len(labels)),where=event_information>0)
    rows=[]
    for i,label in enumerate(labels):
        idx=inverse==i
        if np.sum(idx&(shape>0))<2 or np.sum(idx&(shape==0))<5 or event_information[i]<=0:continue
        err=beta/np.sqrt(event_information[i])
        rows.append({'event':int(label),'depth':float(event_depth[i]),'error':float(err),
                     'snr':float(event_depth[i]/err)})
    def combine(parity):
        selected=[r for r in rows if r['event']%2==parity]
        if not selected:return None
        ww=np.array([1/r['error']**2 for r in selected])
        return {'depth':float(np.average([r['depth'] for r in selected],weights=ww)),
                'error':float(1/np.sqrt(ww.sum()))}
    odd,even=combine(1),combine(0)
    mismatch=None if odd is None or even is None else abs(odd['depth']-even['depth'])/np.hypot(odd['error'],even['error'])
    consistency=None
    if len(rows)>1:
        dd=np.array([r['depth'] for r in rows]);er=np.array([r['error'] for r in rows]);mean=np.average(dd,weights=1/er**2)
        statistic=np.sum(((dd-mean)/er)**2)
        consistency={'chi2':float(statistic),'dof':len(rows)-1,'conditional_chi2_sf':float(chi2.sf(statistic,len(rows)-1))}
    best={'period':float(p0+fit.x[1]/cycles),'transit_time':float(e0+fit.x[0]),'duration':float(fit.x[2]),
          'depth':float(depth),'depth_err':float(error),'depth_snr':float(depth/error)}
    return {'best':best,'optimization_success':bool(fit.success),'boundary_hit':bool(np.any(fit.active_mask)),
        'n_points':len(tt),'n_events':len(rows),'events':rows,'odd':odd,'even':even,
        'odd_even_sigma':None if mismatch is None else float(mismatch),'event_consistency':consistency,
        'beta':beta,'conditional_chi2':float(np.sum(residual**2)),
        'limitations':__doc__,'model':'Exposure-integrated box with one linear baseline per fixed event window'}
