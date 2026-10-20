"""Posthoc masked-plane sensitivity diagnostic using the existing fitter."""
from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
p=Path('results/spoc-pixels-149919534-s75-20261011/analysis');a=json.loads((p/'localization.json').read_text());maps=np.load(p/'images.npz')['event_differences'];target=np.array(a['header_target_xy']);sources=[r for r in a['neighbors_by_distance'] if r['Tmag'] is not None and r['Tmag']<17];radii=[1.5,2.0]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p/n):sha(p/n) for n in ['localization.json','images.npz']},'sources':sources,'radii':radii,'method':'Unweighted planar background fit on pixels outside all T<17 catalog sources; source mask radii1.5/2 pixels. Existing fit_templates with zero templates. No tuning on resulting target residual; same already-opened S75 processed events. No PRF or motion fit; no significance claim.'})
y,x=np.indices(maps[0].shape,dtype=float)
def subtract(im,positions,radius):
 keep=np.isfinite(im)
 for px,py in positions:keep &= (x-px)**2+(y-py)**2>radius**2
 err=np.where(keep,1.,np.nan);fit=fit_templates(im,err,[])
 return im-fit['model'],fit,int(keep.sum())
# Deterministic positive/negative compact-source controls plus a pure plane.
pos=[(3.,3.),(7.,7.)];plane=10+.3*x-.2*y;signal=np.zeros_like(plane);signal[3,3]=4;signal[7,7]=-3;checks=[]
for radius in radii:
 for label,im,truth in [('plane_only',plane,np.zeros_like(plane)),('positive_and_negative_sources',plane+signal,signal)]:
  residual,fit,n=subtract(im,pos,radius);err=float(abs(residual-truth).max());assert err<1e-10
  checks.append({'case':label,'radius':radius,'max_absolute_error':err,'background_pixels':n})
save_json(out/'synthetic.json',{'checks':checks,'limits':'Exact planar/compact-source plumbing control only. Does not model extended PSF wings, crowded sources, correlated errors, nonlinear background or motion.'})
fig,axes=plt.subplots(2,3,figsize=(13,8),constrained_layout=True);rows=[];arrays={}
for j,(n,im) in enumerate(zip(a['event_numbers'],maps)):
 row={'event':n,'fits':[]};z=axes[j,0].imshow(im,origin='lower');fig.colorbar(z,ax=axes[j,0]);axes[j,0].set_title(f'Event{n}: original')
 for k,radius in enumerate(radii):
  residual,fit,count=subtract(im,[(r['x'],r['y']) for r in sources],radius);arrays[f'event{n}_radius{radius}']=residual;ax=axes[j,k+1];z=ax.imshow(residual,origin='lower');fig.colorbar(z,ax=ax);ax.set_title(f'Event{n}: mask radius{radius}')
  measures=[]
  for tic in [149919534,149919536,149919530]:
   src=next(r for r in sources if r['tic']==tic);ap=(x-src['x'])**2+(y-src['y'])**2<=1.5**2;measures.append({'tic':tic,'sum':float(residual[ap].sum()),'pixels':int(ap.sum())})
  row['fits'].append({'radius':radius,'background_pixels':count,'coefficients':fit['coefficients'].tolist(),'background_rms':float(np.sqrt(np.mean(fit['residual']**2))),'aperture_sums':measures})
 for ax in axes[j]:
  ax.plot(*target,'rx')
  for src in sources:
   if src['tic'] in [149919536,149919530]:ax.plot(src['x'],src['y'],'o',mfc='none',mec='orange')
 rows.append(row)
fig.savefig(out/'comparison.png',dpi=140);np.savez_compressed(out/'residuals.npz',**arrays)
save_json(out/'results.json',{'rows':rows,'plot_sha256':sha(out/'comparison.png'),'arrays_sha256':sha(out/'residuals.npz'),'limits':'Aperture sums are raw residual flux, not depths or calibrated detection statistics; overlapping blends and background-fit uncertainty remain. Robustness to two masks does not prove transit or unique host.'});print(rows)
