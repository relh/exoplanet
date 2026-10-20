from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.prf_fit import fit_templates
out=Path(__file__).parent;r=json.loads((out/'fits.json').read_text());tic=str(r['tic']);fig,axes=plt.subplots(len(r['sectors']),4,figsize=(14,3.5*len(r['sectors'])),squeeze=False,constrained_layout=True)
for ax,row in zip(axes,r['sectors']):
 z=np.load(out/f"s{row['sector']}-images.npz");win=row['hypotheses'][0]['tic'];target=fit_templates(z['difference'],z['error'],[z['template_'+tic]]);best=fit_templates(z['difference'],z['error'],[z['template_'+win]]);lim=np.max(abs(z['difference']));pos=np.array(row['positions'][tic])+row['alignment'];wpos=np.array(row['positions'][win])+row['alignment']
 for a,im,title in zip(ax,[z['difference'],target['model'],best['model'],(z['difference']-best['model'])/z['error']],[f"S{row['sector']} observed",f'Target {tic}',f'Best {win}','Best residual / formal error']):
  v=5 if 'residual' in title else lim;m=a.imshow(im,origin='lower',cmap='RdBu_r',vmin=-v,vmax=v);a.plot(*pos,'x',c='black');a.plot(*wpos,'+',c='lime');a.set_title(title,fontsize=10);fig.colorbar(m,ax=a,shrink=.7)
fig.suptitle('Conditional PRF comparison: black target, green preferred source; no host probabilities');fig.savefig(out/'prf-comparison.png',dpi=140)
