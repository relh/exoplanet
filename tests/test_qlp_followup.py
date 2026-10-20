import json
from pathlib import Path
import numpy as np
import pytest
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.transit_model import integrated_box
from exoplanet import qlp_followup


@pytest.mark.parametrize('held_case',['signal','absent','unusable'])
def test_native_qlp_frozen_predictions_and_data_failure(tmp_path,monkeypatch,held_case):
    root=tmp_path/'data';(root/'qlp').mkdir(parents=True)
    period=2.713;epoch=.71;duration=.1;depth=.003
    rng=np.random.default_rng(331)
    target={'tic':123,'training_sectors':[1,2],'heldout_sectors':[30],
            'qlp_products':{str(s):{'dataURL':f'synthetic-sector-{s}'} for s in [1,2,30]}}
    for sector,start in [(1,0),(2,27),(30,730)]:
        t=np.arange(start,start+24,200/86400);e=np.full(len(t),.0003)
        signal=integrated_box(t,period,epoch,duration,200/86400)
        y=1-depth*signal+rng.normal(0,e)
        if sector==30 and held_case=='absent':y+=depth*signal
        if sector==30 and held_case=='unusable':y[:]=np.nan
        columns=[fits.Column(name=k,format=fmt,array=a) for k,fmt,a in
                 [('TIME','D',t),('DET_FLUX','D',y),('DET_FLUX_ERR','D',e),('QUALITY','J',np.zeros(len(t),dtype=int))]]
        h0=fits.PrimaryHDU();h0.header['TICID']=123;h0.header['SECTOR']=sector
        h1=fits.BinTableHDU.from_columns(columns);h1.header['BJDREFI']=2457000
        path=root/'qlp'/f'123-s{sector:04d}.fits'
        fits.HDUList([h0,h1]).writeto(path,checksum=True)
        save_json(path.with_suffix('.fits.json'),{'sha256':sha(path),'url':f'synthetic://{sector}'})
    discovery=tmp_path/'discovery.json';out=tmp_path/'followup'
    save_json(discovery,{'target':target,'clean_baseline_days':51,
              'screened_peaks':[{'best':{'period':period+.0001,'duration':duration,'transit_time':epoch,
                                        'depth':depth,'depth_snr':30}}]})
    real_loader=qlp_followup.load_qlp;calls=[]
    def checked_loader(t,root,**kwargs):
        calls.append(list(t['training_sectors']))
        if t['training_sectors']==[30]:assert (out/'frozen.json').exists()
        assert kwargs['bin_minutes']==0
        return real_loader(t,root,**kwargs)
    monkeypatch.setattr(qlp_followup,'load_qlp',checked_loader)
    checks=qlp_followup.follow_qlp(discovery,out,root,max_sectors=1)
    assert calls==[[1,2],[30]]
    frozen=json.loads((out/'frozen.json').read_text())
    assert frozen['heldout_previously_cached']=={'30':True}
    assert abs(frozen['best']['period']/period-1)<.0001
    if held_case=='unusable':
        assert checks[0]['status']=='error'
        assert 'conclusion' not in checks[0]
    else:
        assert checks[0]['timing_precise']
        expected='recovered_at_frozen_ephemeris_requires_further_vetting' if held_case=='signal' else 'not_recovered_despite_expected_sensitivity'
        assert checks[0]['conclusion']==expected


def test_qlp_mask_is_applied_after_detrending_and_preserves_retained_flux(tmp_path):
    from exoplanet.qlp_campaign import load_qlp
    from exoplanet.search import keep_outside_signals
    root=tmp_path/'data';(root/'qlp').mkdir(parents=True)
    t=np.arange(0,27,10/1440);e=np.full(len(t),.0003)
    rng=np.random.default_rng(13)
    y=1-.004*integrated_box(t,2.7,.4,.12,10/1440)+rng.normal(0,e)
    columns=[fits.Column(name=k,format=fmt,array=a) for k,fmt,a in
             [('TIME','D',t),('DET_FLUX','D',y),('DET_FLUX_ERR','D',e),('QUALITY','J',np.zeros(len(t),dtype=int))]]
    h0=fits.PrimaryHDU();h0.header['TICID']=123;h0.header['SECTOR']=1
    h1=fits.BinTableHDU.from_columns(columns);h1.header['BJDREFI']=2457000
    p=root/'qlp'/'123-s0001.fits';fits.HDUList([h0,h1]).writeto(p,checksum=True)
    save_json(p.with_suffix('.fits.json'),{'sha256':sha(p),'url':'synthetic://1'})
    target={'tic':123,'training_sectors':[1],'qlp_products':{'1':{'dataURL':'synthetic'}}}
    signal={'period':2.7,'transit_time':.4,'halfwidth_days':.12}
    for window in [1.5,2.5]:
        a,b,c,_=load_qlp(target,root,window=window)
        aa,bb,cc,meta=load_qlp(dict(target,masked_signals=[signal]),root,window=window)
        keep=keep_outside_signals(a,[signal]);assert .8<keep.mean()<1
        assert np.array_equal(aa,a[keep]) and np.array_equal(bb,b[keep]) and np.array_equal(cc,c[keep])
        assert meta[0]['n_clean_points']==int(keep.sum())
        assert meta[0]['n_pre_mask_clean_points']==len(a)
