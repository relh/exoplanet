"""Conditional localization controls using on-target dips in observed pixels.

The target-dominated median image is an approximate empirical PSF, not an
independently calibrated PRF. Phase controls share data, preserve only the
observed systematics, and do not yield a survey FAP or astrometric confidence.
"""
import argparse,json,shutil
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import shift as shift_image
from .pixel_vet import difference_events,centroid
from .transit_model import integrated_box,exposure_times
from .pipeline import save_json,sha,now
from .integrity import verify_hdus


def localization_controls(t,flux,error,quality,best,target,draws=49,source_offset=None):
    t=np.asarray(t);flux=np.asarray(flux);quality=np.asarray(quality)
    phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
    yy,xx=np.indices(flux.shape[1:]);radius=np.hypot(xx-target[0],yy-target[1])
    median=np.nanmedian(flux[(quality==0)&(abs(phase)>best['duration'])],axis=0)
    background=np.nanmedian(median[(radius>3)&(radius<5)])
    template=np.where(radius<=3,np.maximum(median-background,0),0)
    if not np.isfinite(template).all() or template.sum()<=0:raise ValueError('Invalid target template')
    offset=np.zeros(2) if source_offset is None else np.asarray(source_offset,float)
    if offset.shape!=(2,) or not np.isfinite(offset).all():raise ValueError('Invalid source displacement')
    if np.any(offset):
        region=(abs(xx-target[0])<=2)&(abs(yy-target[1])<=2)
        normalization=template[region].sum()
        template=np.maximum(shift_image(template,(offset[1],offset[0]),order=3,mode='constant',cval=0),0)
        if template[region].sum()<=0:raise ValueError('Displaced template outside measurement aperture')
        template*=normalization/template[region].sum()
    observed,sigma,events,numbers=difference_events(t,flux,error,quality,best)
    observed_center=centroid(observed,target)
    exposure=exposure_times(t)
    control_quality=quality.copy();control_quality[abs(phase)<best['duration']]=1
    entries=[];maps=[]
    for shift in np.arange(1,draws+1)*best['period']/(draws+1):
        if min(shift,best['period']-shift)<2*best['duration']:continue
        shifted={**best,'transit_time':best['transit_time']+shift}
        entry={'shift_days':float(shift),'status':'error'}
        try:
            shape=integrated_box(t,shifted['period'],shifted['transit_time'],shifted['duration'],exposure)
            injected=flux-best['depth']*shape[:,None,None]*template[None,:,:]
            difference,_,_,cycles=difference_events(t,injected,error,control_quality,shifted)
            position=centroid(difference,target)
            entry.update(status='measured',centroid_xy=position.tolist(),n_events=len(cycles),map_index=len(maps))
            maps.append(difference)
        except ValueError as exc:entry['error']=str(exc)
        entries.append(entry)
    centers=np.array([r['centroid_xy'] for r in entries if r['status']=='measured'])
    if len(centers)<5:raise ValueError('Fewer than five successful controls')
    center=np.median(centers,axis=0);radii=np.linalg.norm(centers-center,axis=1)
    displacement=float(np.linalg.norm(observed_center-center))
    result={'observed_centroid_xy':observed_center.tolist(),'header_target_xy':np.asarray(target).tolist(),
            'template_centroid_xy':centroid(template,target).tolist(),
            'observed_n_events':len(events),'observed_event_numbers':numbers,
            'source_offset_pixels':offset.tolist(),
            'source_template_note':'Median target-dominated empirical image; optionally translated to neighbor and normalized to preserve template flux in fixed measurement aperture. Assumes common PSF shape; not calibrated PRF.',
            'control_median_xy':center.tolist(),'observed_offset_from_control_median_pixels':displacement,
            'control_radius_quantiles_pixels':dict(zip(['50','90','95','100'],np.quantile(radii,[.5,.9,.95,1]).tolist())),
            'n_controls':len(centers),'n_controls_at_least_observed_offset':int(np.sum(radii>=displacement)),
            'n_errors':sum(r['status']=='error' for r in entries),'controls':entries,
            'limitations':__doc__}
    return result,{'observed':observed,'formal_error':sigma,'template':template,'median':median,
                   'control_differences':np.array(maps)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tic',type=int,required=True);p.add_argument('--sector',type=int,required=True)
    p.add_argument('--frozen',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--neighbor-tic',type=int);p.add_argument('--neighbors',type=Path)
    a=p.parse_args()
    if (a.neighbor_tic is None)!=(a.neighbors is None):p.error('Provide both neighbor TIC and catalog')
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'source').mkdir()
    for path in Path(__file__).parent.glob('*.py'):shutil.copyfile(path,a.output/'source'/path.name)
    path=Path(f'data/pixels/{a.tic}-s{a.sector:04d}.fits')
    run={'status':'running','started_utc':now(),'tic':a.tic,'sector':a.sector,'frozen_sha256':sha(a.frozen),
         'pixel_sha256':sha(path),'source_sha256':{f.name:sha(f) for f in (a.output/'source').iterdir()},
         'policy':'49 fixed phase offsets, excluding separation <2 fitted durations; original-event cadences within one duration masked in controls. Empirical target template radius 3 pixels with annulus background; fixed target-centered moment halfwidth 2 pixels for observed and controls. No global-maximum selection. Inject original fitted depth with finite-exposure box.','holdout_policy':'Already-opened pixel file only; no download or new holdout'}
    if a.neighbors:
        run.update(neighbor_tic=a.neighbor_tic,neighbor_catalog_sha256=sha(a.neighbors),
                   alternate_source_policy='Translate empirical target PSF by catalog neighbor-target separation, preserve flux in measurement aperture. Catalog proper motions not propagated; common PSF shape assumed.')
    save_json(a.output/'run.json',run)
    with fits.open(path) as hdus:
        run['integrity']=verify_hdus(path,hdus);d=hdus[1].data
        assert int(hdus[0].header['TICID'])==a.tic and int(hdus[0].header['SECTOR'])==a.sector
        t=np.array(d['TIME'],float);keep=np.isfinite(t);wcs=WCS(hdus[2].header)
        target=np.array(wcs.world_to_pixel_values(hdus[0].header['RA_OBJ'],hdus[0].header['DEC_OBJ']))
        source_offset=None
        if a.neighbors:
            neighbor=next(r for r in json.loads(a.neighbors.read_text()) if int(r['ID'])==a.neighbor_tic)
            source_offset=np.array(wcs.world_to_pixel_values(neighbor['ra'],neighbor['dec']))-target
        result,maps=localization_controls(t[keep],np.array(d['FLUX'][keep],float),
            np.array(d['FLUX_ERR'][keep],float),d['QUALITY'][keep],json.loads(a.frozen.read_text())['best'],target,source_offset=source_offset)
        result['observed_sky']=list(map(float,wcs.pixel_to_world_values(*result['observed_centroid_xy'])))
        result['control_median_sky']=list(map(float,wcs.pixel_to_world_values(*result['control_median_xy'])))
    save_json(a.output/'result.json',result);np.savez_compressed(a.output/'maps.npz',**maps)
    run.update(status='complete',finished_utc=now());save_json(a.output/'run.json',run)
    print(a.sector,result['observed_offset_from_control_median_pixels'],result['control_radius_quantiles_pixels'],result['n_controls_at_least_observed_offset'],result['n_controls'],flush=True)

if __name__=='__main__':main()
