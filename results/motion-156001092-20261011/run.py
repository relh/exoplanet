from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path('results/spoc-pixels-156001092-s69-20261011/analysis');a=json.loads((p/'localization.json').read_text());z=np.load(p/'images.npz');print(z.files,flush=True)
# Median image is archived by the original pixel pipeline.
median=z['median'];maps=z['event_differences'];gy,gx=np.gradient(median);y,x=np.indices(median.shape);tx,ty=a['header_target_xy'];radii=[2.,2.5];sources=a['neighbors_by_distance']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'fit_module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p/n):sha(p/n) for n in ['images.npz','localization.json']},'radii':radii,'method':'Existing linear fit_templates with fixed gradients of archived processed median image plus plane, unweighted. Mask target circle only; other stars constrain common displacement. First-order image-shift diagnostic, not PRF or physical attitude fit. Compare nested plane-only fit on identical pixels. No optimization of masks after viewing.'})
def fit(im,radius,motion):
 keep=np.isfinite(im)&((x-tx)**2+(y-ty)**2>radius**2);err=np.where(keep,1.,np.nan)
 f=fit_templates(im,err,[gx,gy] if motion else []);return im-f['model'],f,int(keep.sum())
# Non-compact Gaussian injection deliberately has wings outside the exclusion mask.
g=np.exp(-((x-tx)**2+(y-ty)**2)/(2*.8**2));g/=g.sum();controls=[]
for radius in radii:
 plane=2+.03*x-.04*y;im=plane+.002*gx-.003*gy
 for amp in [0.,3.]:
  residual,f,n=fit(im+amp*g,radius,True);total=float(residual.sum());controls.append({'radius':radius,'amplitude':amp,'residual_sum':total,'recovered_fraction':None if amp==0 else total/amp,'max_null_residual':float(abs(residual).max()) if amp==0 else None})
  if amp==0:assert abs(residual).max()<1e-9
  else:assert .5<total/amp<1.5
save_json(out/'synthetic.json',{'controls':controls,'limits':'Gaussian injection and exact derivative nuisance controls test implementation/attenuation for one shape only; not mission PRF mismatch, nonlinear motion, correlated noise or host confidence.'})
fig,axes=plt.subplots(2,3,figsize=(13,8),constrained_layout=True);rows=[];arrays={}
for j,(n,im) in enumerate(zip(a['event_numbers'],maps)):
 ax=axes[j,0];c=ax.imshow(im,origin='lower');fig.colorbar(c,ax=ax);ax.set_title(f'Event{n}: original');row={'event':n,'fits':[]}
 for k,radius in enumerate(radii):
  residual,f,count=fit(im,radius,True);_,pf,_=fit(im,radius,False);assert f['chi2']<=pf['chi2']+1e-10
  sums={}
  for tic in [156001092,156001093,156001088]:
   s=next(s for s in sources if s['tic']==tic);ap=(x-s['x'])**2+(y-s['y'])**2<=1.5**2;sums[str(tic)]=float(residual[ap].sum())
  row['fits'].append({'radius':radius,'fit_pixels':count,'gradient_coefficients':f['coefficients'][:2].tolist(),'plane_rss':pf['chi2'],'motion_rss':f['chi2'],'aperture_sums':sums})
  arrays[f'event{n}_radius{radius}']=residual;ax=axes[j,k+1];c=ax.imshow(residual,origin='lower');fig.colorbar(c,ax=ax);ax.set_title(f'Event{n}: motion, mask{radius}')
 for ax in axes[j]:ax.plot(tx,ty,'rx')
 rows.append(row)
fig.savefig(out/'comparison.png',dpi=140);np.savez_compressed(out/'residuals.npz',**arrays)
save_json(out/'results.json',{'rows':rows,'plot_sha256':sha(out/'comparison.png'),'arrays_sha256':sha(out/'residuals.npz'),'limits':'Residual sums are flux, not depth/SNR. Nested RSS decrease is expected and is not significance. Median gradients include processing artifacts and background; coefficients are not calibrated physical shifts.'});print(rows)
