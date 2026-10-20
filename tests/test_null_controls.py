import numpy as np
from exoplanet.null_controls import block_permutation


def test_blocks_preserve_pairs_gaps_and_local_correlations():
    t=np.r_[np.arange(0,10,.02),np.arange(20,30,.02)]
    ix=block_permutation(t,1,np.random.default_rng(15))
    assert np.array_equal(np.sort(ix),np.arange(len(t)))
    assert np.all(ix[:500]<500) and np.all(ix[500:]>=500)
    assert not np.array_equal(ix,np.arange(len(t)))
    assert np.mean(np.diff(ix)==1)>.95
    assert np.array_equal(ix,block_permutation(t,1,np.random.default_rng(15)))
