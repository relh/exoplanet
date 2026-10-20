import numpy as np
from exoplanet.prf_fit import fit_templates, fit_shift


def gaussian(x, y, shape):
    yy, xx = np.indices(shape)
    return np.exp(-((xx-x)**2+(yy-y)**2)/(2*.8**2))/(2*np.pi*.8**2)


def test_blended_scene_alignment_and_eclipse_host():
    shape = (11, 11)
    positions = np.array([[5., 5.], [5.7, 4.6], [2.5, 7.]])
    shift = np.array([.17, -.12])
    yy, xx = np.indices(shape)
    scene = sum(a*gaussian(*(p+shift), shape) for a,p in zip([10000,600,1100],positions)) + 20 + 2*xx - yy
    alignment = fit_shift(scene, np.ones(shape), positions, gaussian)
    np.testing.assert_allclose(alignment['shift'], shift, atol=1e-5)
    for host in [0, 1]:
        difference = 50*gaussian(*(positions[host]+shift), shape) + 3 + .4*xx + .2*yy
        templates = [gaussian(*(p+alignment['shift']), shape) for p in positions]
        fits = [fit_templates(difference, np.ones(shape), [t]) for t in templates]
        assert np.argmin([f['chi2'] for f in fits]) == host
        np.testing.assert_allclose(fits[host]['coefficients'][0], 50, atol=1e-4)
