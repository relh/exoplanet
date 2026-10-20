import numpy as np
import pytest
from exoplanet.rv_activity import fit_activity,predict_activity


def test_activity_fit_predicts_unseen_data_without_rescaling():
    rng=np.random.default_rng(829);t=np.sort(rng.uniform(0,240,350))+2450000
    a=np.column_stack((rng.normal(size=len(t)),np.sin(t/9)))
    y=7+.004*(t-2450000)+3*np.sin(2*np.pi*(t-2450000)/4.73)+2*a[:,0]-a[:,1]
    train=np.arange(len(t))<250;e=np.ones(len(t))*.3
    sol=fit_activity(t[train],y[train],e[train],a[train],[4.729],fraction=np.array([.001]))
    assert abs(sol['periods'][0]-4.73)<1e-5
    np.testing.assert_allclose(predict_activity(sol,t[~train],a[~train]),y[~train],atol=1e-5)
    assert abs(sol['amplitudes'][0]-3)<1e-5


def test_activity_only_model_and_invalid_predictors():
    t=np.arange(80,dtype=float);a=np.sin(t*.73)[:,None];y=3+.02*t+4*a[:,0]
    sol=fit_activity(t,y,np.ones(len(t)),a,[])
    np.testing.assert_allclose(predict_activity(sol,t,a),y,atol=1e-10)
    with pytest.raises(ValueError,match='Constant'):
        fit_activity(t,y,np.ones(len(t)),np.ones_like(a),[])
