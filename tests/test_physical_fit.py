import numpy as np
from exoplanet.physical_fit import transit_flux,fit_circular


def test_exposure_integrated_planet_recovered_with_local_trends():
    rng=np.random.default_rng(3901)
    period=2.37;epoch=.73;k=.045;a=8.5;impact=.35
    t=np.arange(0,35,1/48);exposure=np.full(len(t),1/48)
    y=transit_flux(t,period,epoch,k,a,impact,exposure,supersample=51)
    y+=.0003*np.sin(t/4)+rng.normal(0,80e-6,len(t));dy=np.full(len(t),80e-6)
    result=fit_circular(t,y,dy,{'period':period+.0001,'transit_time':epoch+.002,
                               'duration':.08,'depth':k*k},axis_guess=9.)
    assert result['optimization_success'] and not result['boundary_hit']
    assert abs(result['best']['period']-period)<.0003
    assert abs(result['best']['radius_ratio']/k-1)<.08
    assert abs(result['best']['scaled_axis']/a-1)<.15
    assert result['n_event_windows']>=10


def test_long_exposures_smear_a_short_grazing_transit():
    t=np.array([0.]);kw=dict(period=1.2,epoch=0.,radius_ratio=.03,scaled_axis=12.,impact=.98)
    short=transit_flux(t,exposure=1e-6,**kw)[0]
    long=transit_flux(t,exposure=.08,supersample=51,**kw)[0]
    assert 0<1-long<.5*(1-short)
