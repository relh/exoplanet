import numpy as np
import pytest
from exoplanet.search import flatten, scan, diagnostics, triage


def fake(depth=.003):
    rng = np.random.default_rng(44)
    t = np.arange(0, 27, 1/48)
    t = t[(t < 12.8) | (t > 14)]
    phase = (t - 1.4 + 3.56/2) % 3.56 - 3.56/2
    flux = (1 + .002 * np.sin(t * .4)) * (1 - depth * (abs(phase) < .09/2))
    flux += rng.normal(0, .0002, len(t))
    return t, flux, np.full(len(t), .0002)


def test_injected_transit_recovered_through_detrending():
    t, y, dy = flatten(*fake())
    best = scan(t, y, dy)[2]
    assert abs(best['period'] - 3.56) < .015
    assert .0018 < best['depth'] < .004
    diag = diagnostics(t, y, dy, best)
    assert diag['supported_events'] >= 4
    assert diag['inverted_power_ratio'] < .8
    assert not triage(best, diag)


def test_noise_is_not_promoted():
    t, y, dy = flatten(*fake(depth=0))
    best = scan(t, y, dy)[2]
    assert triage(best, diagnostics(t, y, dy, best))


def test_gap_is_not_bridged():
    t, y, dy = flatten(*fake())
    assert not np.any((t > 12.05) & (t < 14.75))
    assert np.all(np.diff(t) > 0)


def test_short_data_rejected():
    with pytest.raises(ValueError):
        flatten(np.arange(20), np.ones(20), np.ones(20)*.01)


def test_sinusoidal_variable_is_flagged():
    rng = np.random.default_rng(5)
    t = np.arange(0, 27, 1/48)
    f = 1 + .003*np.sin(2*np.pi*t/.38) + rng.normal(0, .0002, len(t))
    t, y, dy = flatten(t, f, np.full(len(t), .0002))
    best = scan(t, y, dy)[2]
    assert 'sinusoidal_variability_preferred' in triage(best, diagnostics(t, y, dy, best))


def test_fits_big_endian_arrays_are_supported():
    arrays=[a.astype('>f8') for a in fake()]
    t,y,dy=flatten(*arrays)
    assert len(t)>200 and np.isfinite(y).all()
