import numpy as np
import pytest
from exoplanet.pixel_vet import difference_events,individual_difference_events,centroid


def test_single_event_neighbor_injection_keeps_aggregate_gate():
    rng=np.random.default_rng(79111355)
    t=np.arange(-.65,.65,.005);yy,xx=np.indices((11,11))
    target=10000*np.exp(-((xx-3)**2+(yy-5)**2)/1.5)
    neighbor=800*np.exp(-((xx-7)**2+(yy-6)**2)/1.5)
    inside=abs(t)<.1
    cube=target[None]+neighbor[None]*(1-.2*inside[:,None,None])+rng.normal(0,2,(len(t),11,11))
    error=np.full_like(cube,2);quality=np.zeros(len(t),int)
    best={'period':18.84,'transit_time':0.,'duration':.2}
    maps,variances,numbers=individual_difference_events(t,cube,error,quality,best)
    assert numbers==[0]
    py,px=np.unravel_index(np.argmax(maps[0]/np.sqrt(variances[0])),maps[0].shape)
    assert np.linalg.norm(centroid(maps[0],(px,py))-[7,6])<.1
    assert abs(maps[0].sum()/(.2*neighbor.sum())-1)<.03
    with pytest.raises(ValueError,match='Fewer than two image events'):
        difference_events(t,cube,error,quality,best)
    quality[inside]=4096
    assert individual_difference_events(t,cube,error,quality,best)[2]==[]


def test_background_eclipse_localizes_away_from_bright_star():
    rng=np.random.default_rng(86)
    t=np.arange(0,27,1/48);yy,xx=np.indices((11,13))
    primary=10000*np.exp(-((xx-4)**2+(yy-5)**2)/1.5)
    neighbor=600*np.exp(-((xx-8)**2+(yy-7)**2)/1.5)
    best={'period':3.488,'transit_time':1.2,'duration':.12}
    mask=abs((t-best['transit_time']+best['period']/2)%best['period']-best['period']/2)<best['duration']/2
    images=primary[None]+neighbor[None]*(1-.25*mask[:,None,None])+rng.normal(0,3,(len(t),11,13))
    error=np.full_like(images,3);quality=np.zeros(len(t),dtype=int)
    difference,sigma,events,number=difference_events(t,images,error,quality,best)
    py,px=np.unravel_index(np.argmax(difference/sigma),difference.shape)
    center=centroid(difference,(px,py))
    assert len(events)>=6
    assert np.linalg.norm(center-np.array([8,7]))<.2
    assert np.linalg.norm(center-np.array([4,5]))>4


def test_outer_background_subtraction_preserves_injected_eclipse():
    """Exercise the TESScut diagnostic with background varying at transit phase."""
    rng=np.random.default_rng(421)
    t=np.arange(0,24,1/144);yy,xx=np.indices((11,11));target=np.array([5.,5.])
    star=3000*np.exp(-((xx-5)**2+(yy-5)**2)/(2*.6**2))
    best={'period':4.19,'transit_time':.8,'duration':.09}
    inside=abs((t-.8+4.19/2)%4.19-4.19/2)<.09/2
    background=300+60*np.sin(t*.7)+25*inside
    noise=rng.normal(0,.4,(len(t),11,11))
    cube=star[None]*(1-.003*inside[:,None,None])+background[:,None,None]+noise
    outer=np.hypot(xx-target[0],yy-target[1])>4
    corrected=cube-np.median(cube[:,outer],axis=1)[:,None,None]
    diff,_,events,_=difference_events(t,corrected,np.full_like(cube,.4),np.zeros(len(t),int),best)
    assert len(events)>=5
    assert np.linalg.norm(centroid(diff,target)-target)<.08
    core=np.hypot(xx-5,yy-5)<2
    assert abs(diff[core].sum()/(.003*star[core].sum())-1)<.03
