"""RV screening with profiled instrumental offsets and a linear trend.

Sinusoidal screens are circular-orbit diagnostics, not planet validation.
"""
import numpy as np
from scipy.optimize import least_squares


def design(t, groups, periods, epoch, trend=True):
    t=np.asarray(t,float)
    cols=[(np.asarray(groups)==g).astype(float) for g in np.unique(groups)]
    if trend:cols.append((t-epoch)/365.25)
    for p in periods:
        angle=2*np.pi*(t-epoch)/p
        cols.extend([np.sin(angle),np.cos(angle)])
    return np.array(cols).T


def fit(t,y,error,groups,periods,epoch=None,trend=True):
    if epoch is None:epoch=float(np.mean(t))
    x=design(t,groups,periods,epoch,trend);a=x/np.asarray(error)[:,None]
    c=np.linalg.lstsq(a,np.asarray(y)/error,rcond=None)[0]
    residual=(y-x@c)/error
    return dict(periods=np.array(periods),epoch=epoch,coefficients=c,model=x@c,
                residual=residual,chi2=float(residual@residual),
                amplitudes=np.hypot(c[-2*len(periods)::2],c[-2*len(periods)+1::2]) if len(periods) else np.array([]))


def scan(t,y,error,groups,frequencies,known=()):
    """Exact weighted two-column improvement after profiling nuisance terms."""
    epoch=float(np.mean(t));x=design(t,groups,known,epoch);a=x/error[:,None]
    q,_=np.linalg.qr(a,mode='reduced'); yw=y/error; residual=yw-q@(q.T@yw)
    powers=[]
    for f in np.array_split(np.asarray(frequencies),max(1,int(np.ceil(len(frequencies)/1024)))):
        angle=2*np.pi*(t[:,None]-epoch)*f
        s=np.sin(angle)/error[:,None];c=np.cos(angle)/error[:,None]
        s-=q@(q.T@s);c-=q@(q.T@c)
        ss=np.sum(s*s,axis=0);cc=np.sum(c*c,axis=0);sc=np.sum(s*c,axis=0)
        sy=residual@s;cy=residual@c;det=ss*cc-sc*sc
        power=np.divide(cc*sy*sy+ss*cy*cy-2*sc*sy*cy,det,out=np.full_like(det,np.nan),where=det>1e-15)
        powers.extend(power)
    return np.array(powers)


def refine(t,y,error,groups,periods,fraction=.03):
    periods=np.array(periods,float);epoch=float(np.mean(t))
    result=least_squares(lambda p:fit(t,y,error,groups,p,epoch)['residual'],periods,
                         bounds=(periods*(1-fraction),periods*(1+fraction)),x_scale='jac',max_nfev=200)
    if not result.success:raise ValueError(result.message)
    return fit(t,y,error,groups,result.x,epoch)
