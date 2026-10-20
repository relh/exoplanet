import numpy as np
from exoplanet.secondary import scan_secondary
from exoplanet.transit_model import integrated_box


def curves(secondary_depth=0,single=False):
    rng=np.random.default_rng(441)
    t=np.arange(0,45,10/1440);e=np.full(len(t),.0004)
    b=dict(period=6.37,transit_time=.7,duration=.15,depth=.004)
    y=1-b['depth']*integrated_box(t,b['period'],b['transit_time'],b['duration'],10/1440)+rng.normal(0,e)
    signal=integrated_box(t,b['period'],b['transit_time']+.472*b['period'],.15,10/1440)
    if single:signal*=t<6.37
    y-=secondary_depth*signal
    return t,y,e,b


def test_displaced_secondary_recovered():
    r=scan_secondary(*curves(.002))
    assert abs(r['best_dip']['phase']-.472)<.01
    assert abs(r['best_dip']['depth']/.002-1)<.15
    assert r['selected_dip_events']['supported_events']>=5


def test_primary_does_not_leak_into_secondary_search():
    r=scan_secondary(*curves())
    assert r['best_dip']['snr']<5
    assert r['depth_ratio_to_primary']<.1


def test_one_off_dip_does_not_gain_repeated_event_support():
    r=scan_secondary(*curves(.008,single=True))
    assert r['selected_dip_events']['supported_events']<3
