"""Conditional circular transit fits; not validation or a false-positive model.

Uses batman with exposure integration and fixed quadratic limb darkening.
Local slopes/intercepts are profiled out in fixed event windows. Stellar-density
agreement depends on circular orbits, dilution, stellar parameters and the model.
https://lkreidberg.github.io/batman/docs/html/tutorial.html
"""
import numpy as np
import batman
from scipy.optimize import least_squares
from .transit_model import exposure_times


def transit_flux(t, period, epoch, radius_ratio, scaled_axis, impact, exposure,
                 limb=(.4,.2), supersample=11):
    t=np.asarray(t,float);exp=np.broadcast_to(exposure,t.shape)
    p=batman.TransitParams();p.t0=epoch;p.per=period;p.rp=radius_ratio;p.a=scaled_axis
    p.inc=np.degrees(np.arccos(impact/scaled_axis));p.ecc=0.;p.w=90.
    p.u=list(limb);p.limb_dark='quadratic';result=np.empty(len(t))
    for duration in np.unique(np.round(exp,6)):
        keep=np.round(exp,6)==duration
        model=batman.TransitModel(p,t[keep],supersample_factor=supersample,exp_time=float(duration))
        result[keep]=model.light_curve(p)
    return result


def fit_circular(t,y,dy,seed,axis_guess,beta=1,limb=(.4,.2),axis_log_prior_sigma=None):
    t,y,dy=map(lambda a:np.asarray(a,float),(t,y,dy))
    p0=seed['period'];d0=seed['duration'];baseline=np.ptp(t)
    e0=seed['transit_time']+round((np.median(t)-seed['transit_time'])/p0)*p0
    labels0=np.rint((t-e0)/p0).astype(int);dt=t-(e0+labels0*p0)
    take=abs(dt)<min(4*d0,.45*p0)
    labels,counts=np.unique(labels0[take],return_counts=True)
    take &= np.isin(labels0,labels[counts>=8])
    exposure=exposure_times(t)[take];tt=t[take]-e0;yy=y[take];ee=dy[take]*beta
    labels,inverse=np.unique(labels0[take],return_inverse=True)
    if len(labels)<3:raise ValueError('Fewer than three event windows')
    w=1/ee**2;sw=np.bincount(inverse,weights=w)
    x=tt-np.bincount(inverse,weights=w*tt)[inverse]/sw[inverse]
    sx2=np.bincount(inverse,weights=w*x*x)
    if np.any(sx2<=0):raise ValueError('Degenerate local baseline')
    def project(z):
        means=np.bincount(inverse,weights=w*z)/sw
        slopes=np.bincount(inverse,weights=w*x*z)/sx2
        return z-means[inverse]-slopes[inverse]*x
    cycles=max(baseline/p0,1.)
    def unpack(z):
        k,a=np.exp(z[:2]);impact=z[2]*(1+k)
        return k,a,impact,z[3],p0+z[4]/cycles
    def residual(z,prior=True):
        k,a,impact,epoch,period=unpack(z)
        model=transit_flux(tt,period,epoch,k,a,impact,exposure,limb=limb)
        r=project(yy-model)/ee
        if prior and axis_log_prior_sigma is not None:
            r=np.r_[r,(np.log(a)-np.log(axis_guess))/axis_log_prior_sigma]
        return r
    low=[np.log(.001),np.log(2.),0.,-d0,-2*d0]
    high=[np.log(.5),np.log(60.),.999,d0,2*d0]
    starts=[]
    for impact_fraction in [.1,.5,.85]:
        initial=[np.log(np.clip(np.sqrt(seed['depth']),.002,.3)),np.log(axis_guess),impact_fraction,0.,0.]
        fit=least_squares(residual,initial,bounds=(low,high),
                          x_scale=[.2,.2,.3,d0,d0],diff_step=1e-4,max_nfev=300)
        starts.append(fit)
    fit=min(starts,key=lambda z:np.sum(z.fun**2));k,a,impact,epoch,period=unpack(fit.x)
    argument=np.sqrt(max(0,(1+k)**2-impact**2))/np.sqrt(a*a-impact*impact)
    duration=period/np.pi*np.arcsin(np.clip(argument,0,1))
    # Newtonian circular transit density, ignoring companion mass.
    density=3*np.pi*a**3/(6.67430e-11*(period*86400)**2)/1000
    return {'best':{'period':float(period),'transit_time':float(e0+epoch),
                    'radius_ratio':float(k),'scaled_axis':float(a),'impact':float(impact),
                    'duration_days':float(duration),'circular_density_g_cm3':float(density)},
            'optimization_success':bool(fit.success),'boundary_hit':bool(np.any(fit.active_mask)),
            'conditional_data_chi2':float(np.sum(residual(fit.x,prior=False)**2)),
            'conditional_total_chi2':float(np.sum(fit.fun**2)),
            'start_objectives':[float(np.sum(s.fun**2)) for s in starts],
            'n_points':len(tt),'n_event_windows':len(labels),'n_free_transit_parameters':5,
            'n_profiled_baseline_parameters':2*len(labels),'beta':beta,
            'limb_darkening':list(limb),'supersample_factor':11,
            'axis_log_prior_sigma':axis_log_prior_sigma,'axis_guess':axis_guess,
            'limitations':__doc__}
