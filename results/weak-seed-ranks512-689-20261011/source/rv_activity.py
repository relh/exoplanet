"""Single-instrument circular RV fits with contemporaneous linear activity terms.

Training-only scaling is preserved for prediction. This does not model activity
lags, correlated noise, indicator measurement error, or eccentric orbits.
"""
import numpy as np
from scipy.optimize import least_squares
from .rv_search import design


def predict_activity(solution, t, activity):
    t=np.asarray(t,float);activity=np.asarray(activity,float)
    if activity.shape!=(len(t),len(solution['activity_mean'])) or not np.all(np.isfinite(activity)):
        raise ValueError('Invalid activity predictors')
    base=design(t,np.zeros(len(t),int),solution['periods'],solution['epoch'])
    x=np.column_stack((base,(activity-solution['activity_mean'])/solution['activity_scale']))
    return x@solution['coefficients']


def fit_activity(t,y,error,activity,periods,fraction=.001):
    t,y,error,activity,periods=map(lambda a:np.asarray(a,float),(t,y,error,activity,periods))
    if t.ndim!=1 or y.shape!=t.shape or error.shape!=t.shape or activity.ndim!=2 or len(activity)!=len(t):
        raise ValueError('Mismatched input shapes')
    if not all(np.all(np.isfinite(a)) for a in [t,y,error,activity,periods]) or np.any(error<=0) or np.any(periods<=0):
        raise ValueError('Nonfinite or nonpositive inputs')
    fraction=np.asarray(fraction,float)
    if fraction.ndim>1 or (fraction.ndim==1 and fraction.shape!=periods.shape) or not np.all(np.isfinite(fraction)) or np.any((fraction<=0)|(fraction>=1)):
        raise ValueError('Invalid period neighborhood')
    mean=activity.mean(axis=0);scale=activity.std(axis=0)
    if np.any(scale<=0):raise ValueError('Constant activity predictor')
    z=(activity-mean)/scale;epoch=float(t.mean())
    def solve(p):
        x=np.column_stack((design(t,np.zeros(len(t),int),p,epoch),z));a=x/error[:,None]
        if len(t)<=a.shape[1]:raise ValueError('Insufficient observations')
        c,_,rank,_=np.linalg.lstsq(a,y/error,rcond=None)
        if rank<a.shape[1]:raise ValueError('Rank-deficient model')
        return (y-x@c)/error,c,float(np.linalg.cond(a))
    if len(periods):
        opt=least_squares(lambda p:solve(p)[0],periods,bounds=(periods*(1-fraction),periods*(1+fraction)),x_scale='jac',max_nfev=300)
        if not opt.success:raise ValueError(opt.message)
        periods=opt.x
    residual,c,condition=solve(periods)
    return dict(periods=periods,epoch=epoch,activity_mean=mean,activity_scale=scale,coefficients=c,
                chi2=float(residual@residual),condition_number=condition,
                amplitudes=np.hypot(c[2:2+2*len(periods):2],c[3:2+2*len(periods):2]))
