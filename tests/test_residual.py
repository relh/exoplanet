import numpy as np
from exoplanet.search import keep_outside_signals
from exoplanet.campaign import joint_scan


def test_masking_dominant_signal_reveals_second_transit_without_modifying_flux():
    rng=np.random.default_rng(198)
    t=np.r_[np.arange(0,25,1/48),np.arange(28,54,1/48)]
    y=1-.008*(abs((t-.73+3.17/2)%3.17-3.17/2)<.06)
    y-=.001*(abs((t-1.13+7.43/2)%7.43-7.43/2)<.04)
    y+=rng.normal(0,.0003,len(t));dy=np.full(len(t),.0003);saved=y.copy()
    best=joint_scan(t,y,dy)[2]
    assert abs(best['period']-3.17)<.01
    mask=keep_outside_signals(t,[{**best,'halfwidth_days':best['duration']}])
    recovered=joint_scan(t[mask],y[mask],dy[mask])[2]
    assert abs(recovered['period']-7.43)<.01
    assert mask.mean()>.8
    assert np.array_equal(y,saved)
