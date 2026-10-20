"""Local-baseline difference images for a frozen transit ephemeris.

Image moments are a localization diagnostic, not a calibrated PRF fit or formal
false-positive probability. Per-event resampling estimates repeatability only.
"""
import argparse,json
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from .pipeline import fetch,save_json,sha,now
from .campaign import lightcurve_url
from .integrity import verify_hdus


def difference_events(t,flux,error,quality,best):
    p,e,d=(best[k] for k in ['period','transit_time','duration'])
    phase=(t-e+p/2)%p-p/2;event=np.rint((t-e)/p).astype(int)
    valid=(quality==0)&np.isfinite(t)
    differences=[];variances=[];numbers=[]
    for n in np.unique(event[valid&(abs(phase)<d/2)]):
        inside=valid&(event==n)&(abs(phase)<d/2)
        outside=valid&(event==n)&(abs(phase)>d)&(abs(phase)<3*d)
        if inside.sum()<2 or outside.sum()<5:continue
        # Symmetric local baseline; inspect per-event maps for motion/background.
        diff=np.nanmean(flux[outside],axis=0)-np.nanmean(flux[inside],axis=0)
        var=np.nansum(error[outside]**2,axis=0)/outside.sum()**2+np.nansum(error[inside]**2,axis=0)/inside.sum()**2
        differences.append(diff);variances.append(var);numbers.append(int(n))
    if len(differences)<2:raise ValueError('Fewer than two image events')
    differences=np.array(differences);variances=np.array(variances)
    w=np.divide(1,variances,out=np.zeros_like(variances),where=variances>0)
    total=np.sum(w,axis=0)
    average=np.divide(np.sum(w*differences,axis=0),total,out=np.zeros_like(total),where=total>0)
    sigma=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0))
    return average,sigma,differences,numbers


def centroid(image,center,halfwidth=2):
    yy,xx=np.indices(image.shape)
    region=(abs(xx-center[0])<=halfwidth)&(abs(yy-center[1])<=halfwidth)
    background=np.nanmedian(image[~region]) if (~region).any() else 0
    weight=np.where(region,np.maximum(image-background,0),0)
    if weight.sum()<=0:raise ValueError('No positive difference flux')
    return np.array([(weight*xx).sum(),(weight*yy).sum()])/weight.sum()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tic',type=int,required=True);parser.add_argument('--sector',type=int,required=True)
    parser.add_argument('--frozen',type=Path,required=True);parser.add_argument('--neighbors',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    frozen=json.loads(a.frozen.read_text());best=frozen['best']
    path=Path(f'data/pixels/{a.tic}-s{a.sector:04d}.fits')
    source=fetch(lightcurve_url(a.tic,a.sector).replace('_lc.fits','_tp.fits'),path)
    with fits.open(path) as h:
        integrity=verify_hdus(path,h);d=h[1].data;wcs=WCS(h[2].header)
        time=np.array(d['TIME'],dtype=float);finite=np.isfinite(time)
        time=time[finite];flux=np.array(d['FLUX'][finite],dtype=float);err=np.array(d['FLUX_ERR'][finite],dtype=float)
        quality=d['QUALITY'][finite]
        diff,sigma,events,number=difference_events(time,flux,err,quality,best)
        image=np.nanmedian(flux[quality==0],axis=0)
        target=np.array(wcs.world_to_pixel_values(h[0].header['RA_OBJ'],h[0].header['DEC_OBJ']))
        # Photometric target is overwhelmingly the brightest source in this stamp.
        bright_y,bright_x=np.unravel_index(np.nanargmax(image),image.shape)
        target_moment=centroid(image,(bright_x,bright_y))
        py,px=np.unravel_index(np.nanargmax(diff/sigma),diff.shape)
        center=centroid(diff,(px,py))
        per_event=[centroid(im,(px,py)).tolist() for im in events]
        ra,dec=wcs.pixel_to_world_values(*center)
        neighbors=[]
        if a.neighbors:
            for star in json.loads(a.neighbors.read_text()):
                sx,sy=wcs.world_to_pixel_values(star['ra'],star['dec'])
                neighbors.append({'tic':star['ID'],'Tmag':star['Tmag'],'x':float(sx),'y':float(sy),
                                  'separation_pixels':float(np.hypot(sx-center[0],sy-center[1]))})
        result={'created_utc':now(),'tic':a.tic,'sector':a.sector,'source':source,'integrity':integrity,
            'frozen_sha256':sha(a.frozen),'n_events':len(events),'event_numbers':number,
            'header_target_xy':target.tolist(),'bright_source_moment_xy':target_moment.tolist(),
            'difference_peak_xy':[int(px),int(py)],'difference_moment_xy':center.tolist(),
            'difference_peak_snr':float((diff/sigma)[py,px]),
            'difference_sky':{'ra':float(ra),'dec':float(dec)},
            'offset_from_bright_source_pixels':float(np.linalg.norm(center-target_moment)),
            'per_event_moments':per_event,'neighbors_by_distance':sorted(neighbors,key=lambda n:n['separation_pixels']),
            'limitations':'Local-baseline difference moments, no PRF fit; not calibrated astrometric uncertainties. TIC neighbor positions not propagated for proper motion; target image moment provided separately.'}
        save_json(a.output/'localization.json',result)
        np.savez_compressed(a.output/'images.npz',median=image,difference=diff,error=sigma,event_differences=events)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(1,3,figsize=(14,4),constrained_layout=True)
        for ax,data,title in zip(axes,[np.log10(np.maximum(image,1)),diff,diff/sigma],['Log median flux','Out − in flux','Difference / formal error']):
            im=ax.imshow(data,origin='lower',cmap='viridis');fig.colorbar(im,ax=ax,shrink=.8)
            ax.plot(*target_moment,'x',color='red',ms=10,label='Bright source')
            ax.plot(*center,'+',color='white',ms=12,label='Difference moment')
            ax.set_title(title)
            for star in neighbors:
                if -.5<star['x']<image.shape[1]-.5 and -.5<star['y']<image.shape[0]-.5 and star['Tmag'] and star['Tmag']<15:
                    ax.plot(star['x'],star['y'],'o',mfc='none',mec='orange',ms=5)
                    if ax is axes[1]:ax.annotate(str(star['tic']),(star['x'],star['y']),color='orange',fontsize=6)
        axes[0].legend(fontsize=7);fig.suptitle(f'TIC {a.tic}, Sector {a.sector}: {len(events)} events; diagnostic localization')
        fig.savefig(a.output/'difference.png',dpi=140);plt.close(fig)
    print(json.dumps({k:result[k] for k in ['tic','n_events','offset_from_bright_source_pixels','difference_peak_snr','difference_sky']}),flush=True)

if __name__=='__main__':main()
