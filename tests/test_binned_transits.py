import numpy as np
import pytest
from exoplanet.qlp_campaign import bin_curve
from exoplanet.transit_model import integrated_box
from exoplanet.search import flatten
from exoplanet.campaign import joint_scan


@pytest.mark.parametrize('period,duration',[(.83,.04),(5.21,.09)])
def test_finite_exposure_transit_survives_ten_minute_binning(period,duration):
    rng=np.random.default_rng(20261010)
    t=np.arange(0,45,200/86400)
    t=t[~((t>20)&(t<21))]
    e=np.full(len(t),.0005)
    y=(1+.002*np.sin(2*np.pi*t/12))*(1-.001*integrated_box(t,period,.29,duration,200/86400))+rng.normal(0,e)
    tb,yb,eb=bin_curve(t,y,e,width=10/1440)
    tc,yc,ec=flatten(tb,yb,eb)
    best=joint_scan(tc,yc,ec)[2]
    assert abs(best['period']/period-1)<.002
    assert abs(best['depth']/.001-1)<.2
    assert best['depth_snr']>10
