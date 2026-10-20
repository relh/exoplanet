import numpy as np
from exoplanet.injection_grid import integrated_box


def test_exact_box_integration_preserves_area_and_wraps_period():
    t=np.arange(-1,1,.02)+.01
    box=integrated_box(t,3,0,.09,.02)
    assert np.isclose(box.sum()*.02,.09)
    assert np.allclose(box,integrated_box(t+3,3,0,.09,.02))
    assert np.isclose(integrated_box(np.array([0]),3,0,.01,.02)[0],.5)
    assert np.isclose(integrated_box(np.array([.04]),3,0,.09,.02)[0],.75)
