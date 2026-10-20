import pathlib,json,hashlib
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=pathlib.Path('results/lco-archive-metadata-20261013');D=pathlib.Path('data/lco-archive-metadata-20261013');t=json.load(open('results/followup-planning-20261013/targets.json'))['targets'][0];c=t['coordinates'];sources=[{'tic':t['tic'],'ra':c['ra_j2016_deg'],'dec':c['dec_j2016_deg'],'epoch':'J2016 (proper motion subarcsec by2023)'}]+[{'tic':n['neighbor_tic'],'ra':n['catalog_ra_deg'],'dec':n['catalog_dec_deg'],'epoch':'catalog epoch uncertain'} for n in t['priority_neighbors']];results=[]
fig,axes=plt.subplots(2,1,figsize=(9,10),layout='constrained')
for ax,fpath in zip(axes,sorted(D.glob('*.fits.fz'))):
 with fits.open(fpath) as f:
  image=f['SCI'].data;mask=f['BPM'].data;cat=f['CAT'].data;h=f['SCI'].header;w=WCS(h);scale=np.sqrt(abs(np.linalg.det(w.pixel_scale_matrix)))*3600;rr=[]
  for s in sources:
   x,y=w.all_world2pix(s['ra'],s['dec'],0);x=float(x);y=float(y);active=bool(15<x<image.shape[1]-15 and 15<y<image.shape[0]-15);d=np.hypot(cat['x']-x,cat['y']-y);i=int(d.argmin());cx=float(cat['x'][i]);cy=float(cat['y'][i]);cxp,cyp=np.meshgrid(np.arange(int(cx)-10,int(cx)+11),np.arange(int(cy)-10,int(cy)+11));inside=(cxp-cx)**2+(cyp-cy)**2<=6**2;vals=image[cyp,cxp][inside];mm=mask[cyp,cxp][inside];row={**s,'predicted_x0':x,'predicted_y0':y,'inside_science_bounds':active,'nearest_catalog_offset_arcsec':float(d[i]*scale),'catalog_x':cx,'catalog_y':cy,'catalog_fwhm_pixels':float(cat['fwhm'][i]),'catalog_fwhm_arcsec':float(cat['fwhm'][i]*scale),'catalog_flag':int(cat['flag'][i]),'aperture_radius_pixels':6,'aperture_peak':float(np.nanmax(vals)),'pixels_above_maxlin':int((vals>=h['MAXLIN']).sum()),'pixels_above_saturate':int((vals>=h['SATURATE']).sum()),'bad_mask_pixels':int((mm!=0).sum()),'aperture_pixels':int(inside.sum())};rr.append(row)
  results.append({'file':str(fpath),'sha256':hashlib.sha256(fpath.read_bytes()).hexdigest(),'date_obs':h['DATE-OBS'],'scale_arcsec_pixel':scale,'header_maxlin':h['MAXLIN'],'header_saturate':h['SATURATE'],'sources':rr})
  tx,ty=rr[0]['predicted_x0'],rr[0]['predicted_y0'];xlo,xhi=int(tx)-150,int(tx)+150;ylo,yhi=int(ty)-150,int(ty)+150;crop=image[ylo:yhi,xlo:xhi];ax.imshow(np.arcsinh((crop-np.nanmedian(crop))/500),origin='lower',extent=(xlo,xhi,ylo,yhi),cmap='gray',vmin=0,vmax=5)
  for r in rr:
   x,y=r['predicted_x0'],r['predicted_y0'];ax.scatter(x,y,s=90,facecolors='none',edgecolors='tab:orange');ax.text(x+7,y+7,str(r['tic']),color='tab:orange',fontsize=8)
  ax.set_xlim(xlo,xhi);ax.set_ylim(ylo,yhi);ax.set_title(fpath.name+' — out-of-event');ax.set_xlabel('Science pixel x (zero based)');ax.set_ylabel('Science pixel y (zero based)')
(R/'image-feasibility.json').write_text(json.dumps({'scope':'Baseline image geometry and saturation only; no event-depth sensitivity or planetary evidence','catalog_position_note':'BANZAI catalogue matching is nearest pixel source; offsets reported, no blind certainty of identity. Catalogue fwhm is measured image width, saturation may distort it.','results':results},indent=2)+'\n');fig.savefig(R/'baseline-images.png',dpi=150)
for r in results:
 print(r['file']);print([(s['tic'],round(s['nearest_catalog_offset_arcsec'],2),round(s['catalog_fwhm_arcsec'],2),s['pixels_above_maxlin'],s['bad_mask_pixels']) for s in r['sources']])
