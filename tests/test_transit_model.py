import numpy as np
from exoplanet.transit_model import integrated_box,fit_events


def simulate(odd_depth=None):
    rng=np.random.default_rng(118)
    t=np.r_[np.arange(0,23,1/48),np.arange(28,51,1/48)]
    p=1.37;epoch=.427;duration=.12
    events=np.rint((t-epoch)/p).astype(int)
    depth=np.where(events%2==0,.00075,odd_depth or .00075)
    y=1-depth*integrated_box(t,p,epoch,duration,1/48)+rng.normal(0,.00009,len(t))
    return t,y,np.full(len(t),.00009),{'period':1.3698,'transit_time':epoch-.007,'duration':.132}


def test_refinement_preserves_uniform_depth_at_finite_cadence():
    t,y,dy,seed=simulate();r=fit_events(t,y,dy,seed)
    assert r['optimization_success'] and not r['boundary_hit']
    assert abs(r['best']['period']-1.37)<.0002
    assert abs(r['best']['depth']-.00075)<.00005
    assert r['odd_even_sigma']<3
    assert r['event_consistency']['conditional_chi2_sf']>.001


def test_refinement_retains_genuine_alternating_eclipses():
    t,y,dy,seed=simulate(.0015);r=fit_events(t,y,dy,seed)
    assert r['odd_even_sigma']>15
    assert r['event_consistency']['conditional_chi2_sf']<.001


def test_gap_truncated_window_does_not_abort_other_events():
    t,y,dy,seed=simulate()
    t=np.r_[t,54.68,54.70];y=np.r_[y,1,1];dy=np.r_[dy,.00009,.00009]
    r=fit_events(t,y,dy,seed)
    assert r['n_events']>=25
    assert abs(r['best']['depth']-.00075)<.00005
