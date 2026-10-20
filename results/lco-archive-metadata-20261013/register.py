"""Exploratory local registration of opened baseline images; no transit fit."""
import pathlib,json,hashlib,csv
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
from astropy.wcs import WCS
R=pathlib.Path('results/lco-archive-metadata-20261013');D=pathlib.Path('data/lco-archive-metadata-20261013');cp=pathlib.Path('results/triceratops-20261013/80387959-stars.csv');scene=list(csv.DictReader(cp.open()));scene=[r for r in scene if float(r['Tmag'])<17];old=json.load(open(R/'image-feasibility.json'));out=[]
for before in old['results']:
 with fits.open(before['file']) as f:
  im=f['SCI'].data;mask=f['BPM'].data;h=f['SCI'].header;w=WCS(h);cat=f['CAT'].data;obs=np.column_stack([cat['x'],cat['y']]);valid=np.isfinite(obs).all(axis=1)&np.isfinite(cat['fwhm']);obs=obs[valid];cat=cat[valid];pred=np.column_stack(w.all_world2pix([float(r['ra']) for r in scene],[float(r['dec']) for r in scene],0));tree=cKDTree(obs);ds,inds=tree.query(pred,k=15);diffs=(obs[inds]-pred[:,None,:])[ds<100];hist,xe,ye=np.histogram2d(diffs[:,0],diffs[:,1],bins=np.arange(-100,102,2));peak=np.unravel_index(np.argmax(hist),hist.shape);shift=np.array([xe[peak[0]]+1,ye[peak[1]]+1]);dist,idx=tree.query(pred+shift);good=dist<4
  # affine fit to consensus matches; each physical source used once
  selected=np.where(good)[0];_,uniq=np.unique(idx[selected],return_index=True);selected=selected[uniq];train=selected[np.arange(len(selected))%3!=0];test=selected[np.arange(len(selected))%3==0];a=np.column_stack([pred,np.ones(len(pred))]);coef=np.linalg.lstsq(a[train],obs[idx[train]],rcond=None)[0];res=np.linalg.norm(a@coef-obs[idx],axis=1);rr=[]
  for s in before['sources']:
   p=np.array([s['predicted_x0'],s['predicted_y0'],1.]);x,y=p@coef;dist,ii=tree.query([x,y]);cx,cy=obs[ii];xx,yy=np.meshgrid(np.arange(round(x)-6,round(x)+7),np.arange(round(y)-6,round(y)+7));sel=(xx-x)**2+(yy-y)**2<36;values=im[yy,xx][sel];bpm=mask[yy,xx][sel];rr.append({'tic':s['tic'],'registered_x0':float(x),'registered_y0':float(y),'nearest_detection_arcsec':float(dist*before['scale_arcsec_pixel']),'catalog_fwhm_arcsec':float(cat[ii]['fwhm']*before['scale_arcsec_pixel']),'catalog_flag':int(cat[ii]['flag']),'peak_6px_aperture':float(values.max()),'pixels_above_maxlin':int((values>=h['MAXLIN']).sum()),'pixels_above_saturate':int((values>=h['SATURATE']).sum()),'bad_mask_pixels':int((bpm!=0).sum()),'aperture_pixels':int(sel.sum())})
  out.append({'file':before['file'],'initial_translation_pixels':shift.tolist(),'consensus_stars':len(selected),'train_stars':len(train),'heldout_registration_stars':len(test),'train_rms_pixels':float(np.sqrt(np.mean(res[train]**2))),'heldout_rms_pixels':float(np.sqrt(np.mean(res[test]**2))),'affine_coefficients':coef.tolist(),'sources':rr})
(R/'registered-feasibility.json').write_text(json.dumps({'scope':'Exploratory registration within two authorized baselineframes, not photometric or planetary holdout test','scene_path':str(cp),'scene_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'results':out},indent=2)+'\n')
for r in out:print(r)
