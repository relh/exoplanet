import numpy as np
from exoplanet.rv_search import fit,scan,refine


def test_irregular_sampling_offset_and_two_planets():
    rng=np.random.default_rng(10)
    t=np.sort(rng.uniform(0,700,240));g=(t>400).astype(int);err=np.full(len(t),.4)
    y=25*g+.003*t+4*np.sin(2*np.pi*t/2.61)+3*np.cos(2*np.pi*t/11.13)
    f=np.linspace(1/20,1/2,15000);power=scan(t,y,err,g,f)
    assert abs(1/f[np.argmax(power)]-2.61)<.003
    fitted=refine(t,y,err,g,[2.61,11.13])
    np.testing.assert_allclose(fitted['periods'],[2.61,11.13],atol=1e-5)
    np.testing.assert_allclose(fitted['amplitudes'],[4,3],atol=1e-4)
    # Profiled scan must equal full simultaneous least squares, including offset.
    base=fit(t,y,err,g,[])['chi2']
    for idx in [3,251,999]:
        direct=base-fit(t,y,err,g,[1/f[idx]])['chi2']
        np.testing.assert_allclose(power[idx],direct,rtol=1e-8)


def test_prediction_preserves_instrument_identity():
    import pytest
    from exoplanet.rv_search import predict
    t=np.arange(30,dtype=float);g=np.repeat([3,7],15)
    y=20*(g==7)+.05*t+2*np.sin(2*np.pi*t/3.7)
    solution=fit(t,y,np.ones(30),g,[3.7])
    for label in [3,7]:
        m=g==label
        np.testing.assert_allclose(predict(solution,t[m],g[m]),y[m],atol=1e-10)
    with pytest.raises(ValueError,match='Unseen instrument'):
        predict(solution,np.array([40.]),np.array([9]))


def test_nightly_jitter_is_not_averaged_away(tmp_path):
    from exoplanet.rv_campaign import nightly
    path=tmp_path/'rv.csv'
    path.write_text('BJD,RV_mlc_nzp,e_RV_mlc_nzp,f_RV\n'+
                    ''.join(f'2456000.1,{3.0},1,0\n' for _ in range(100))+
                    '2456000.2,999,1,1\n2456001.1,4,-1,0\n2456002.1,5,1,0\n')
    t,y,e,g=nightly(path,jitter=2)
    assert len(t)==2
    np.testing.assert_allclose(y,[3,5])
    assert 2<e[0]<2.01
    assert e[1]>e[0]


def test_masks_on_same_night_are_separate_configurations(tmp_path):
    from exoplanet.rv_campaign import nightly
    p=tmp_path/'rv.csv'
    p.write_text('BJD,RV_mlc_nzp,e_RV_mlc_nzp,f_RV,MASK\n'
                 '2456000.1,3,1,0,K5\n2456000.2,53,1,0,G2\n'
                 '2456001.1,4,1,0,K5\n')
    t,y,e,g=nightly(p,separate_masks=True)
    assert len(t)==3
    np.testing.assert_allclose(y[g=='pre:K5'],[3,4])
    np.testing.assert_allclose(y[g=='pre:G2'],[53])
