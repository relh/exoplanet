from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.prf_fit import fit_templates
p=Path(__file__).parent;r=json.loads((p/'fits.json').read_text());fig,axes=plt.subplots(2,4,figsize=(14,7),constrained_layout=True);idx=0
for s in r['sectors']:
 z=np.load(p/f"s{s['sector']}-images.npz");pos=np.array(s['positions']['402358350'])+s['alignment'];yy,xx=np.indices(z['difference'].shape);dist=np.hypot(xx-pos[0],yy-pos[1])
 for rad in [2.5,3.5]:
  e=np.where(dist<=rad,z['error'],np.inf);mo=fit_templates(z['difference'],e,[z['gradx'],z['grady']]);full=fit_templates(z['difference'],e,[z['template_402358350'],z['gradx'],z['grady']]);lim=np.max(abs(z['difference'][dist<=rad]));res=(z['difference']-full['model'])/z['error']
  for ax,im,title in zip(axes[idx],[z['difference'],mo['model'],full['model'],res],['Observed','Motion + plane','Target + motion + plane','Residual / formal error']):
   vmax=5 if title.startswith('Residual') else lim;show=np.where(dist<=rad,im,np.nan);m=ax.imshow(show,origin='lower',cmap='RdBu_r',vmin=-vmax,vmax=vmax);ax.plot(*pos,'x',color='black');ax.set_xlim(pos[0]-rad-.5,pos[0]+rad+.5);ax.set_ylim(pos[1]-rad-.5,pos[1]+rad+.5);ax.set_title(f"S{s['sector']}, r={rad}: {title}",fontsize=9);fig.colorbar(m,ax=ax,shrink=.7)
  idx+=1
fig.suptitle('TIC 402358350: posthoc local motion sensitivity; models are not validated source assignments');fig.savefig(p/'local-models.png',dpi=130)
