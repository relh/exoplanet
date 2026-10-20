import numpy as np
from exoplanet.pixel_injection import localization_controls
from exoplanet.transit_model import integrated_box


def test_pixel_controls_separate_on_target_and_displaced_dimming():
    rng=np.random.default_rng(627)
    t=np.arange(0,22,1/48);yy,xx=np.indices((11,11));target=np.array([5.,5.])
    star=5000*np.exp(-((xx-5)**2+(yy-5)**2)/(2*.8**2))
    neighbor=5000*np.exp(-((xx-6)**2+(yy-5)**2)/(2*.8**2))
    base=star+.01*neighbor+100
    noise=rng.normal(0,3,(len(t),11,11));error=np.full_like(noise,3.);quality=np.zeros(len(t),int)
    best={'period':2.37,'transit_time':.73,'duration':.12,'depth':.005}
    shape=integrated_box(t,best['period'],best['transit_time'],best['duration'],1/48)
    results=[]
    for source in [star,neighbor]:
        flux=base[None,:,:]+noise-best['depth']*shape[:,None,None]*source
        saved=flux.copy();result,_=localization_controls(t,flux,error,quality,best,target,draws=19)
        assert np.array_equal(flux,saved)
        assert result['n_controls']>=10 and result['n_errors']==0
        results.append(result)
    assert results[0]['observed_offset_from_control_median_pixels']<.1
    assert results[1]['observed_offset_from_control_median_pixels']>.5
    assert results[1]['n_controls_at_least_observed_offset']==0
    neighbor_result,_=localization_controls(t,flux,error,quality,best,target,draws=19,source_offset=[1,0])
    assert neighbor_result['observed_offset_from_control_median_pixels']<.1
