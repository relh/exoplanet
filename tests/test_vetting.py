import numpy as np
from exoplanet.vetting import correlated_noise,event_consistency


def test_correlated_noise_distinguished_from_white():
    rng=np.random.default_rng(19)
    t=np.arange(0,50,1/48);dy=np.full(len(t),.001)
    white=1+rng.normal(0,.001,len(t))
    red=white+.004*np.sin(2*np.pi*t/.8)
    best={'period':3.56,'transit_time':1.2,'duration':.12,'depth_snr':12}
    a=correlated_noise(t,white,dy,best);b=correlated_noise(t,red,dy,best)
    assert a['beta']<1.5
    assert b['beta']>4 and b['adjusted_snr']<4


def test_inconsistent_events_not_mistaken_for_repeated_transits():
    equal=[{'depth':d,'error':.0001} for d in [.001,.0011,.0009,.001]]
    changing=[{'depth':d,'error':.0001} for d in [.001,.0001,.0001,.0001]]
    assert event_consistency(equal)['conditional_chi2_sf']>.1
    result=event_consistency(changing)
    assert result['conditional_chi2_sf']<.001
    assert result['max_positive_event_snr2_fraction']>.9


def test_hour_long_transit_noise_at_thirty_minute_cadence():
    rng=np.random.default_rng(23)
    t=np.arange(0,40,1/48);dy=np.full(len(t),.001)
    y=1+rng.normal(0,.001,len(t))
    best={'period':3.69,'transit_time':1.1,'duration':.04,'depth_snr':20}
    result=correlated_noise(t,y,dy,best)
    assert result['status']=='measured' and result['n_bins']>100
    assert result['beta']<1.5
