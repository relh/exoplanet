import numpy as np
from exoplanet.campaign import joint_scan, distinct_peaks, lightcurve_url
from exoplanet.targeting import training_sectors


def test_training_never_uses_holdout():
    assert training_sectors([2,3,4,29,30,31,69,70]) == [2,3,4]
    assert training_sectors([2,29,69]) == []
    assert training_sectors([54,55,56,57]) == [54,55]


def test_multisector_injection():
    rng=np.random.default_rng(18)
    t=np.r_[np.arange(0,24,1/48),np.arange(28,52,1/48)]
    phase=(t-1.2+4.73/2)%4.73-4.73/2
    y=1-.0015*(abs(phase)<.06/2)+rng.normal(0,.0003,len(t))
    _, power, best=joint_scan(t,y,np.full(len(t),.0003))
    assert abs(best['period']-4.73)<.01
    peaks=distinct_peaks(power)
    assert len(peaks)==3
    assert all(abs(peaks[i]['period']/peaks[j]['period']-1)>.019 for i in range(3) for j in range(i))


def test_lightcurve_archive_path():
    assert 's0014/target/0000/0002/7274/7181/' in lightcurve_url(272747181,14)


def test_fixed_holdout_does_not_shift_to_fit_wrong_phase():
    from exoplanet.followup import fixed_measure
    rng=np.random.default_rng(77)
    t=np.arange(800,827,1/48)
    phase=(t-1.2+3.5/2)%3.5-3.5/2
    y=1-.003*(abs(phase)<.1/2)+rng.normal(0,.0002,len(t))
    dy=np.full(len(t),.0002)
    matched=fixed_measure(t,y,dy,3.5,1.2,.1)
    wrong=fixed_measure(t,y,dy,3.5,1.2+1,.1)
    assert matched['total']['snr']>20
    assert abs(wrong['total']['snr'])<4


def test_prediction_uncertainty_grows_with_baseline():
    from exoplanet.followup import prediction_spread
    best={'period':3.5,'transit_time':1.2}
    ranges={'profile_timing_pairs':[[3.499,1.2],[3.501,1.2]],'conditional_epoch_floor_days':.001}
    assert prediction_spread(np.array([1000,1027]),best,ranges)>prediction_spread(np.array([10,27]),best,ranges)


def test_expanded_training_refines_period_without_shrinking_seed_interval():
    from exoplanet.followup import refine_training,prediction_spread
    rng=np.random.default_rng(101)
    t=np.r_[np.arange(0,24,1/48),np.arange(730,780,1/48)]
    period=3.48813;epoch=1.2;duration=.09
    phase=(t-epoch+period/2)%period-period/2
    y=1-.002*(abs(phase)<duration/2)+rng.normal(0,.0003,len(t))
    seed={'period':3.4885,'duration':duration}
    best,ranges=refine_training(t,y,np.full(len(t),.0003),seed,seed_baseline=50)
    assert abs(best['period']-period)<.0001
    assert prediction_spread(np.array([1500,1527]),best,ranges)<duration/2


def test_qlp_binning_preserves_integrated_dip_and_gaps():
    from exoplanet.qlp_campaign import bin_curve
    t=np.r_[np.arange(0,2,1/720),np.arange(3,5,1/720)]
    y=np.ones(len(t));y[(t>.9)&(t<1.0)]-=.003
    bt,by,be=bin_curve(t,y,np.full(len(t),.001))
    assert not np.any((bt>2)&(bt<3))
    # Interior bins have five equal samples; the integrated missing flux survives.
    assert abs((1-by).sum()*5-(1-y).sum())<.004
    assert np.median(be)<.0005


def test_extended_baseline_injection_and_empty_qlp():
    import pytest
    from exoplanet.qlp_campaign import bin_curve
    with pytest.raises(ValueError,match='No finite positive'):
        bin_curve(np.array([]),np.array([]),np.array([]))
    rng=np.random.default_rng(912)
    t=np.r_[np.arange(0,49,1/48),np.arange(56,108,1/48)]
    phase=(t-1.2+4.73/2)%4.73-4.73/2
    y=1-.0015*(abs(phase)<.06/2)+rng.normal(0,.0003,len(t))
    dy=np.full(len(t),.0003)
    with pytest.raises(ValueError,match='baseline'):
        joint_scan(t,y,dy)
    best=joint_scan(t,y,dy,max_baseline=120)[2]
    assert abs(best['period']-4.73)<.002


def test_empirical_qlp_errors_recover_noise_with_gaps_and_sparse_dips():
    from exoplanet.qlp_campaign import empirical_errors
    rng=np.random.default_rng(950)
    t=np.r_[np.arange(0,5,1/720),np.arange(7,12,1/720)]
    y=1+rng.normal(0,.0008,len(t));y[(t%3)<.05]-=.004
    sigma,meta=empirical_errors(t,y)
    assert abs(sigma/.0008-1)<.08
    assert meta['n_pairs']==len(t)-2
